#include "FileSplitter.h"
#include "Utils.h"

#include <iostream>
#include <fstream>
#include <filesystem>
#include <stdexcept>
#include <sstream>
#include <vector>
#include <cstring>

namespace fs = std::filesystem;

//    Class constructor
FileSplitter::FileSplitter(const std::string& inputFile, const std::string& outputDirectory, size_t sizePerChunk)
    : inputFilePath(inputFile), outputDir(outputDirectory), chunkSize(sizePerChunk) {
        
    fileCounter = 0;

    if (!fs::exists(inputFilePath)) {
        throw std::invalid_argument("Input File not Found!");
    }
}



void FileSplitter::split() {

    // Inizializzo e apro lo stream in lettura (come bynary per alleggerire)
    std::ifstream inputFile(inputFilePath, std::ios::binary);
    if (!inputFile.is_open()) {
        throw std::runtime_error("Impossibile aprire il file di input");
    }

    std::vector<char> buffer(chunkSize * 2); // Buffer esteso per gestire lo spazio rimanente
    size_t bufferSize = 0;

    size_t max_memory_used = 0;

    while (inputFile.read(buffer.data() + bufferSize, chunkSize) || inputFile.gcount() > 0) {


        size_t memory_used = getMemoryUsage(); // Valutazione utilizzo memoria
        if(memory_used > max_memory_used)
            max_memory_used = memory_used;

        bufferSize += inputFile.gcount(); // gcount restituisce il numero di caratteri letti
        
        // Prende come ultima posizione possibile uno spazio così da evitare parole troncate
        size_t lastSpacePos = bufferSize;
        for (size_t i = bufferSize; i > 0; --i) {
            if (buffer[i - 1] == ' ') {
                lastSpacePos = i;
                break;
            }
        }
        
        std::stringstream chunkFileName;
        chunkFileName << outputDir << "/chunk_" << fileCounter++ << ".bin"; // Path del nuovo chunk creato

        std::ofstream chunkFile(chunkFileName.str(), std::ios::binary);  // Apre l'i-esimo chunk in scrittura
        if (!chunkFile.is_open()) {
            throw std::runtime_error("Impossibile creare file di output");
        }
    
        chunkFile.write(buffer.data(), lastSpacePos);// Scrive sull'i-esimo chunk
        std::cout << "Creato file: " << chunkFileName.str() << " (" << lastSpacePos << " byte)" << std::endl;
        
        // Sposta il puntatore nella lettura dello stream fino alla parola da cui partirà il nuovo chunk
        std::memmove(buffer.data(), buffer.data() + lastSpacePos, bufferSize - lastSpacePos);
        bufferSize -= lastSpacePos;
    }
    
    // Massima memoria utilizzata durante l'esecuizione
    std::cout << "Massima memoria utilizzata: " << max_memory_used << " KB" << std::endl;

    inputFile.close();
}
