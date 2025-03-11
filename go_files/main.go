package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strings"
	"strconv"
	"path/filepath"
)

func main() {

	if len(os.Args) < 3 {
		log.Fatal("Too less arguments")
		return
	}

	
	path := os.Args[1]
	

	// ------------------------- Analysis ------------------------
	analyzer := FileAnalyzer{
		FilePath:   path,
		SearchTerm: os.Args[2],
	}

	err := analyzer.Analyze() // fileAnalyzer.go
	if err != nil {
		log.Fatal(err)
		return
	}

	// ----------------------------------------------------------
	finalPart := filepath.Base(path)
	if !strings.Contains(finalPart, "EOF") { // Se il file per cui è stato lanciato il thread dovesse essere EOF, lo rimuove senza effettuare analisi
		err := os.Remove(path)
		if err != nil {
			log.Fatal(err)
		}
	}
	
	jsonData, err := json.Marshal(analyzer.Positions) // Json Dump
	if err != nil {
		log.Fatal(err)
	}


	// Output (Conforme a quanto python si aspetta)
	fmt.Println(strconv.Itoa(analyzer.Occurrences) + "---" + string(jsonData))
}