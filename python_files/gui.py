from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel, QLineEdit

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import core


class AnalyzerThread(QThread):
    """
    Classe QThread per eseguire l'analisi senza interrompere la GUI
    """
    
    # Preimposta il segnale da inviare
    analysis_finished = pyqtSignal(str, str, list)

    def __init__(self, file_path: str, word: str):
        """Costruttore QThread

        Args:
            file_path (str): path del file da analizzare
            word (str): parola da ricercare
        """
        super().__init__()
        self.file_path = file_path
        self.word = word

    def run(self) -> None:
        """Esegue l'analisi con i parametri di path e word impostati
        """
        res = core.process_large_file(self.file_path, self.word)

        # Una volta terminato, invia il segnale con i risultati
        if res is not None:
            self.analysis_finished.emit("Analisi Terminata", f'Sono state trovate {res[0]} parole {self.word}', res[1])
        else:
            self.analysis_finished.emit("Errore durante l\'analisi", "Nessun risultato trovato.")

class FileAnalyzerApp(QWidget):
    """ GUI Class"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """ Struttura della GUI """
        self.setWindowTitle('Big Size File Analyzer')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        self.line_edit = QLineEdit(self)
        
        self.load_button = QPushButton('Load File', self)
        self.load_button.clicked.connect(self.load_file)

        self.analyze_button = QPushButton('Analyze', self)
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.analyze_file)
        
        self.text_area_label = QLabel("LOGs:", self)
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        
        self.result_area_label = QLabel("RESULTs:",self)
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        
        layout.addWidget(self.line_edit)
        layout.addWidget(self.load_button)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.text_area_label)
        layout.addWidget(self.text_area)
        layout.addWidget(self.result_area_label)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

        self.file_path = None

    def load_file(self) -> None:
        """Apertura della finestra di Dialog: imposta il self.path di analisi
        """
        
        file, _ = QFileDialog.getOpenFileName(self, 'Load File', '', 'Text Files (*.txt)',
                                              options = QFileDialog.Options())
        if file:
            self.file_path = file
            self.text_area.setText(f'File caricato: {file}')
            self.analyze_button.setEnabled(True)

    def analyze_file(self) -> None:
        """
        Avvio analisi: viene eseguito il main thread per la ricerca
        """
        word = self.line_edit.text()   
        
        if word == "":
            return
        
        self.text_area.setText(f'Analisi Avviata ...')
        self.result_area.setText(f'')
        self.analyze_button.setEnabled(False)
                
        # Thread di ricerca (se si gestisce tramite Qthread la GUI non si blocca)
        self.analysis_thread = AnalyzerThread(self.file_path, word)
        self.analysis_thread.analysis_finished.connect(self.update_results)
        self.analysis_thread.start()
        
    def update_results(self, log: str, result: str, data: list) -> None:
        """
        Riceve il segnale dal main thread quando termina con i risultati ottenuti per costruire l'output
        
        Args:
            log (str): Messaaggio per la text area LOGS
            result (str): Messaaggio per la text area RESULTS
            data (list): Lista dei dati per la creazione del grafico delle ricorrenze
        """
        
        self.text_area.setText(log)
        self.result_area.setText(result)
        self.analyze_button.setEnabled(True)
                
        # Calcolo della distribuzione dalla lista a dict:
        # per ogni chunk (dunque porzione di testo) sono contati quante parole sono state trovate
        count_dict = dict()
        for item in data:
            key = item[0]
            if key not in count_dict:
                count_dict[key] = 0
            count_dict[key] += 1
        
        if len(count_dict) != 0:
            
            # Ordinamento e riempimento dei chunk vuoti:
            # dove non vi sono stati trovati elementi si conterà 0            
            all_keys = range(0, max(count_dict))
            for key in all_keys:
                if key not in count_dict:
                    count_dict[key] = 0
            count_dict = dict(sorted(count_dict.items()))
            
            # Creazione del grafico
            keys = list(count_dict.keys())
            values = list(count_dict.values())
            
            plt.bar(keys, values)
            
            plt.xlabel('Testo')
            plt.xticks([]) # Rimozione valori nelle ascisse
            plt.ylabel('Ricorrenze')
            plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True)) # Cast a Int dei valori nelle ordinate
            plt.title('Distribuzione lungo il testo')
            
            # Apertura finestra del grafico risultato
            plt.show()
