#include "Utils.h"
#include <fstream>
#include <string>
#include <sstream>

// Utilizzato per l'analisi della memoria (per valutare il risparmo di memoria nel processo)
size_t getMemoryUsage() {
    std::ifstream file("/proc/self/status");
    std::string line;
    
    while (std::getline(file, line)) {
        if (line.find("VmRSS:") != std::string::npos) {
            std::istringstream iss(line);
            std::string label;
            size_t value;
            std::string unit;
            iss >> label >> value >> unit;
            return value;
        }
    }
    
    return 0;
}