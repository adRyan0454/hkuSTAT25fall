#!/bin/bash

echo "========================================"
echo "INT8 Quantization Engine - Build Script"
echo "========================================"
echo ""

# Check for C++ compiler
if command -v g++ &> /dev/null; then
    COMPILER="g++"
    echo "[OK] Found g++ compiler"
elif command -v clang++ &> /dev/null; then
    COMPILER="clang++"
    echo "[OK] Found clang++ compiler"
else
    echo "[ERROR] No C++ compiler found!"
    echo ""
    echo "Please install g++ or clang++:"
    echo "  Ubuntu/Debian: sudo apt-get install g++"
    echo "  CentOS/RHEL:   sudo yum install gcc-c++"
    echo "  macOS:         xcode-select --install"
    exit 1
fi

# Check for CMake
USE_CMAKE=0
if command -v cmake &> /dev/null; then
    echo "[OK] Found CMake"
    USE_CMAKE=1
else
    echo "[INFO] CMake not found, will use direct compilation"
fi

echo ""

# Create build directory
mkdir -p build

# Choose build method
if [ $USE_CMAKE -eq 1 ]; then
    echo "========================================"
    echo "Building with CMake"
    echo "========================================"
    echo ""
    
    cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release
    if [ $? -ne 0 ]; then
        echo "[ERROR] CMake configuration failed"
        exit 1
    fi
    
    make
    if [ $? -ne 0 ]; then
        echo "[ERROR] Build failed"
        exit 1
    fi
    
    cd ..
    
    # Find executable
    if [ -f "build/bin/inference_engine" ]; then
        EXE_PATH="build/bin/inference_engine"
    elif [ -f "build/inference_engine" ]; then
        EXE_PATH="build/inference_engine"
    else
        echo "[ERROR] Executable not found"
        exit 1
    fi
else
    echo "========================================"
    echo "Building with $COMPILER"
    echo "========================================"
    echo ""
    
    $COMPILER -std=c++17 -O2 -I include \
        src/Tensor.cpp \
        src/LinearLayer.cpp \
        src/Model.cpp \
        src/Utils.cpp \
        src/main.cpp \
        -o build/inference_engine
    
    if [ $? -ne 0 ]; then
        echo "[ERROR] Build failed"
        exit 1
    fi
    
    EXE_PATH="build/inference_engine"
fi

echo ""
echo "========================================"
echo "Build Successful!"
echo "========================================"
echo ""
echo "Executable: $EXE_PATH"
echo "File size: $(du -h $EXE_PATH | cut -f1)"
echo ""
echo "Next steps:"
echo "1. Run: ./$EXE_PATH"
echo "2. Or use: ./run.sh"
echo ""
