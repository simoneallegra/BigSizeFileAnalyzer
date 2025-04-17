from concurrent.futures import ThreadPoolExecutor, as_completed
import threading as th
import subprocess
from pathlib import Path
import time
import json
from typing import Tuple
import queue

project_path = Path(__file__).parent.parent # la cartella di progetto per lavorare con i path relativi
_tmp_path = Path(f'{project_path}/_tmp/') # cartella dove avverrà l'elaborazione dei chunks

# Mutex per la gestione della concorrenza delle variabili globali di output
mutex = th.Lock()
tot: int = 0

# Coda per la gestione della Shared Memory condivisa tra i thread per registrare le ricorrenze
output = queue.Queue()

def splitter(input_path : str, kbytes : int = 10000) -> None:
    """C++ subprocess per la divisione in chunk da n KB

    Args:
        input_path (str): path del file da dividere
        kbytes (int): numero di kbytes per ogni chunk (10Kb di default)
    """
    subprocess.run([f'{project_path}/cpp_files/file_splitter',
                    input_path,
                    _tmp_path,
                    str(kbytes)])
    
def searcher(path: str, word: str) -> None:
    """
        Esegue in codice in Go per la ricerca nei singoli chunk. Questo è gestito come thread e si apre un thread per ogni chunk
    Args:
        path (str): cartella dei file contenenti i chunks
        word (str): parola da ricercare per ogni chunk
    """
    global tot # global output
    
    process = subprocess.run([f'{project_path}/go_files/searcher', _tmp_path / path, word], capture_output = True, text = True)

    try:
        with mutex:
            res = process.stdout.split("---")
            tot = tot + int(res[0])
            list = json.loads(res[1])  

            if list is not None:
                chunk_nr = int(str(path).split("_")[1].split(".")[0])
                for elem in list:
                    t = (chunk_nr, elem)
                    output.put(t)
                    
    except Exception as e:
        print(f"Error nel searcher {e}")
        
def is_end_of_files() -> bool:
    """
        _
    Returns:
        bool: Restituisce True se l'ultimo file rimasto della cartella di analisi è 'EOF', False altrimenti 
    """
    files = [file for file in _tmp_path.iterdir() if file.is_file()]
    res = (len(files) == 1 and files[0].name == "EOF")
    if res:
        files[0].unlink()
    return res
    
def process_large_file(input_path: str, word) -> Tuple[int, list[Tuple[int, any]]]:
    """ Core principale di ricerca

    Args:
        input_path (str): percorso del file da analizzare
        word (_type_): parola da ricercare in tutto il file durante il processo

    Returns:
        Tuple[int, list[Tuple[int, any]]]: Torna il numero Totale di parole trovate considerando tutti i chunk analizzati
        e una lista dove ci sono le informazioni (n_chunk, riferimento_di_posizione) per ogni parola trovata 
    """
    global tot
    tot = 0
    # 1) Esegue un Thread per lo Splitter in Cpp
    splitter_thread = th.Thread(target=(lambda: splitter(input_path)))
    splitter_thread.start()
    
    # Salvo i nomi dei file analizzati
    file_analyzed = set()
    
    # Salvo i pools
    futures = []

    run = True
    
    with ThreadPoolExecutor() as threadPoolExecutor:
        """
        https://docs.python.org/3/library/concurrent.futures.html#:~:text=Changed%20in%20version%203.5%3A%20If,number%20of%20workers%20for%20ProcessPoolExecutor.
        """
        
        while run:
            files = [file for file in _tmp_path.iterdir() if file.is_file()]
            
            for file in files:
                
                if file.name == "EOF" and len(files) == 1: # Se è rimasto solo il file 'EOF'
                    file.unlink()
                    run = False
                    break
                
                elif file.name not in file_analyzed and "EOF" not in file.name: # Nuovo file da analizzare
                    file_analyzed.add(file.name)
                    futures.append(tuple(file.name, threadPoolExecutor.submit(searcher, file.name, word)))

    # Aspetta la fine di tutti i thread 
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Errore nel thread: {e}")

    output_list = list()
    while not output.empty():
        output_list.append(output.get())
    
    return tot, output_list

