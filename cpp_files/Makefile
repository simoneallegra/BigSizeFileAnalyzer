# Esequzione compilatore
#
# Commands:
# 	* 'make' -> compilation
# 	* 'make clean' -> remove previous compilation
#


CXX = g++                   
CXXFLAGS = -std=c++17 -Wall 
TARGET = file_splitter
SRC = driver.cpp FileSplitter.cpp Utils.cpp
OBJ = $(SRC:.cpp=.o)         
OUT_DIR = bin                

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) $(OBJ) -o $(TARGET)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

.PHONY: all clean
