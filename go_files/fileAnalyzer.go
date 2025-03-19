package main

import (
	"bufio"
	"strings"
	"os"
)

type FileAnalyzer struct {
	FilePath    string
	SearchTerm  string
	Occurrences int
	Positions   []int
}

func NewFileAnalyzer(filePath, searchTerm string) *FileAnalyzer { // Costruttore FileAnalyzer legato alla struct sopra definita
	return &FileAnalyzer{
		FilePath:   filePath,
		SearchTerm: searchTerm,
	}
}

func (fa *FileAnalyzer) Analyze() error { // Metodo assegnato alla struct (error tipo di ritorno in caso di)

	file, err := os.Open(fa.FilePath)
	if err != nil {
		return err
	}
	defer file.Close() // Alla chiusrura della funzione Analyze chiuderà il file

	scanner := bufio.NewScanner(file) // Apre il file in scan mode

	// Scansiona il file riga per riga
	for scanner.Scan() {

		line := scanner.Text() // Recupera il testo letto

		linePosition := strings.Index(line, fa.SearchTerm) // Cerca il termine in tutto il testo
		if linePosition == -1{
			return nil // Se non ne trova termina
		}
		
		fa.Positions = append(fa.Positions, linePosition) // Salva il termine trovato e la relativa posizione
		nextPos := linePosition + len(fa.SearchTerm) // Sposta il puntatore per escludere la parola trovare e rieseguire l'analisi

		for linePosition != -1 {
			
			fa.Occurrences ++ // Incrementa il contatore di parole (lo fa per primo in quanto se siamo arrivati qui è già stata trovata una occorenza)
			nextPos = linePosition + len(fa.SearchTerm)
			

			// Nuova i-esima analisi
			if nextPos > len(line) - len(fa.SearchTerm) {
				break
			}

			line = line[ nextPos : ]

			linePosition = strings.Index(line, fa.SearchTerm)
			 // L'analisi termina quando nel testo rimanente non è trovata più una parola
			
			 if linePosition != -1{
				fa.Positions = append(fa.Positions, linePosition + len(fa.SearchTerm) + fa.Positions[len(fa.Positions) - 1])
			}
				
		}
	}

	return nil
}


