@echo off
chcp 65001 >nul
echo ========================================
echo INT8量化推理引擎 - 编译脚本
echo ========================================
echo.

REM 检查是否在Visual Studio开发者命令提示符环境中
where cl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] 找到MSVC编译器
    goto :compile_msvc
)

REM 检查是否有CMake
where cmake >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] 找到CMake
    goto :compile_cmake
)

REM 检查是否有MinGW g++
where g++ >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] 找到MinGW g++
    goto :compile_mingw
)

echo [错误] 未找到可用的编译器或CMake
echo.
echo 请选择以下方式之一：
echo 1. 安装CMake并添加到PATH
echo 2. 使用Visual Studio开发者命令提示符运行此脚本
echo 3. 安装MinGW-w64
echo.
pause
exit /b 1

:compile_msvc
echo.
echo ========================================
echo 使用MSVC编译器编译
echo ========================================
echo.

if not exist build mkdir build

cl /EHsc /std:c++17 /I include /O2 ^
    src\Tensor.cpp ^
    src\LinearLayer.cpp ^
    REM src\LayerNorm.cpp ^  & REM not used in current main.cpp flow
    REM src\GELU.cpp ^       & REM not used in current main.cpp flow
    src\Model.cpp ^
    src\Utils.cpp ^
    src\main.cpp ^
    /Fe:build\inference_engine.exe

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [成功] 编译完成！
    echo 可执行文件: build\inference_engine.exe
) else (
    echo.
    echo [错误] 编译失败
    pause
    exit /b 1
)
goto :end

:compile_cmake
echo.
echo ========================================
echo 使用CMake编译
echo ========================================
echo.

if not exist build mkdir build
cd build

cmake .. -DCMAKE_BUILD_TYPE=Release
if %ERRORLEVEL% NEQ 0 (
    echo [错误] CMake配置失败
    cd ..
    pause
    exit /b 1
)

cmake --build . --config Release
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 编译失败
    cd ..
    pause
    exit /b 1
)

cd ..
echo.
echo [成功] 编译完成！
if exist "build\bin\inference_engine.exe" (
    echo 可执行文件: build\bin\inference_engine.exe
) else if exist "build\inference_engine.exe" (
    echo 可执行文件: build\inference_engine.exe
)
goto :end

:compile_mingw
echo.
echo ========================================
echo 使用MinGW g++编译
echo ========================================
echo.

if not exist build mkdir build

g++ -std=c++17 -O2 -I include ^
    src\Tensor.cpp ^
    src\LinearLayer.cpp ^
    REM src\LayerNorm.cpp ^  & REM not used in current main.cpp flow
    REM src\GELU.cpp ^       & REM not used in current main.cpp flow
    src\Model.cpp ^
    src\Utils.cpp ^
    src\main.cpp ^
    -o build\inference_engine.exe

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [成功] 编译完成！
    echo 可执行文件: build\inference_engine.exe
) else (
    echo.
    echo [错误] 编译失败
    pause
    exit /b 1
)
goto :end

:end
echo.
echo ========================================
echo 编译完成！
echo ========================================
echo.
echo 下一步：运行 run.bat 或直接运行可执行文件
echo.
pause
