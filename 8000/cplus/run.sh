#!/bin/bash

echo "========================================"
echo "INT8 Quantization Engine - Run"
echo "========================================"
echo ""

# Find executable
if [ -f "build/bin/inference_engine" ]; then
    EXE_PATH="build/bin/inference_engine"
elif [ -f "build/inference_engine" ]; then
    EXE_PATH="build/inference_engine"
else
    echo "[ERROR] Executable not found!"
    echo ""
    echo "Please build the project first:"
    echo "  ./build.sh"
    exit 1
fi

# Check model file
if [ ! -f "data/model_fp32.bin" ]; then
    echo "[ERROR] Model file not found: data/model_fp32.bin"
    echo ""
    echo "Please ensure the model file exists"
    exit 1
fi

# Create output directory
mkdir -p output

# Run inference engine
echo "Running INT8 inference engine..."
echo ""
$EXE_PATH

echo ""
echo "========================================"
echo "Execution Complete!"
echo "========================================"
echo ""
echo "Output files in output/ directory:"
if [ -f "output/model_int8_e2e.bin" ]; then
    echo "  [OK] output/model_int8_e2e.bin"
fi
if [ -f "output/quant_stats_e2e.txt" ]; then
    echo "  [OK] output/quant_stats_e2e.txt"
fi
if [ -f "output/accuracy_log_e2e.txt" ]; then
    echo "  [OK] output/accuracy_log_e2e.txt"
fi
echo ""
