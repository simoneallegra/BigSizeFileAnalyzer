#include <string>
#include <filesystem>
#include <stdexcept>

namespace fs = std::filesystem;

class FileSplitter {
private:
    std::string inputFilePath; 
    std::string outputDir;      
    size_t chunkSize;
    std::ostringstream chunkBuffer;
    int fileCounter;           

public:

    /**
     * COSTRUTTORE 
     *
     * Args: 
     *      * inputFilePath [String]: File da dividere 
     *      * outputDir [String]: Cartella per il salvataggio dei chunks
     *      * chunckSize [Int]: Dimensione massima di ogni chunk
     */
    FileSplitter(const std::string& inputFile, const std::string& outputDirectory, size_t sizePerChunk = 1048576);
    
    void split();

};
