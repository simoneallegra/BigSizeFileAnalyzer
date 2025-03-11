#include <iostream>
#include <fstream>
#include <stdexcept>
#include "FileSplitter.h"

namespace fs = std::filesystem;

int main(int argc, char* argv[]) {
    /**
     * Args: 
     *      * inputFilePath [String]: File da dividere 
     *      * outputDir [String]: Cartella per il salvataggio dei chunks
     *      * chunckSize [Int]: Dimensione massima di ogni chunk
     */

    try {
        
        std::string inputFilePath = argv[1];
        std::string outputDir = argv[2];
        size_t chunckSize = std::stoull(argv[3]);

        // Crea la directory di output se non esiste
        if (!fs::exists(outputDir)) {
            fs::create_directory(outputDir);
        }
        
        // Crea un oggetto FileSplitter
        FileSplitter splitter(inputFilePath, outputDir, chunckSize);
        
        splitter.split(); // Esegue lo split
        
        // Crea il file vuoto EOF per segnalare la fine dell'elaborazione
        std::cout << "End of File" << std::endl;
        std::ofstream file(outputDir + "/EOF");

    }
    catch (const std::exception& e) {

        // Gestione dell'eccezione generica
        std::cerr << "Error: " << e.what() << std::endl;
    }
    
    return 0;
}
