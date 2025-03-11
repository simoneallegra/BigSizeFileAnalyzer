# Big Size File Analyzer Project

Questo progetto è un'analizzatore di file che utilizza componenti in C++, Go e Python per dividere, cercare e analizzare grandi file di testo.

## Architettura

L'architettura del programma è disponibile in formato Google Docs al seguente link:
https://docs.google.com/document/d/1ip9YVqkptYvKCTQZ8S6Oa2dQLRDdTUHYm-3XbUaG-cs/edit?usp=sharing

## Prerequisiti

Il software è stato creato e testato su un ambiente con le seguenti caratteristiche:

- Ubuntu 22.04 
- Python==3.10.12
- g++==11.4.0
- Go==go1.18.1
- pip==22.0.2

Per altre configurazioni non è garantito il funzionamento

## Installazione

1. Clona il repository del progetto:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Crea un ambiente virtuale Python e attivalo:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Installa le dipendenze Python:
    ```sh
    pip install -r python_files/requiriments.txt
    ```

4. Compila i file C++:
    ```sh
    cd cpp_files
    make
    cd ..
    ```

5. Compila i file Go:
    ```sh
    cd go_files
    ./build.sh
    cd ..
    ```

## Esecuzione

1. Avvia l'applicazione GUI:
    ```sh
    cd python_files
    python app.py
    ```

2. Utilizza l'interfaccia grafica per selezionare il file da analizzare e indicare la parola da cercare.

#### [Opzionale] Generazione files per tests

E' possibile generare file testuali di lunghezza variabile per eseguire diversi test sul software.

1. Avvia lo script python
    ```sh
    cd tests
    text_file_generator.py
    ```

2. Segui leistruzioni espresse da riga di comando

Questo script si appoggia ad una libreria per creare parole casuali <ins>in inglese</ins>

## Struttura del Progetto

- [cpp_files]: Contiene il codice sorgente C++ per dividere i file in chunk.
- [go_files]: Contiene il codice sorgente Go per cercare le parole nei chunk.
- [python_files]: Contiene il codice sorgente Python per la GUI e la logica principale.
- [tests]: Contiene file di test e script per generare file di test.

## Note

- Assicurati che la cartella [_tmp] esista nella directory principale del progetto, poiché verrà utilizzata per memorizzare i chunk temporanei durante l'analisi.

## Autori

- Simone Allegra