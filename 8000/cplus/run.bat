@echo off
chcp 65001 >nul
echo ========================================
echo INT8推理引擎 - 快速运行
echo ========================================
echo.

REM 检查可执行文件是否存在（支持两种可能的路径）
set EXE_PATH=
if exist "build\bin\inference_engine.exe" (
    set EXE_PATH=build\bin\inference_engine.exe
) else if exist "build\inference_engine.exe" (
    set EXE_PATH=build\inference_engine.exe
)

if "%EXE_PATH%"=="" (
    echo [错误] 可执行文件不存在
    echo 请先编译项目：
    echo   cmake --build build --config Release
    echo   或使用 Visual Studio 编译
    pause
    exit /b 1
)

REM 检查模型文件
if not exist "data\model_fp32.bin" (
    echo [错误] 模型文件不存在: data\model_fp32.bin
    echo 请先生成模型文件
    pause
    exit /b 1
)

REM 运行推理引擎
echo 运行INT8推理引擎...
echo.
%EXE_PATH%

echo.
echo ========================================
echo 运行完成！
echo ========================================
echo.
echo 输出文件位于 output\ 目录：
if exist "output\model_int8_e2e.bin" (
    echo   [OK] output\model_int8_e2e.bin
)
if exist "output\quant_stats_e2e.txt" (
    echo   [OK] output\quant_stats_e2e.txt
)
if exist "output\accuracy_log_e2e.txt" (
    echo   [OK] output\accuracy_log_e2e.txt
)
echo.
pause
