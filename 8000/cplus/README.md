# INT8量化推理引擎

基于C++17实现的轻量级INT8量化推理引擎，支持小型Transformer模型的量化推理。

本项目针对 **TinyStories-1M** 模型，实现了完整的 INT8 量化推理流程，包括对称量化、层间 INT8 传递、精度评估等功能。

## 项目结构

```
cplus/
├── include/          # 头文件
│   ├── Tensor.h      # 张量模板类（支持float和int8_t）
│   ├── Layer.h       # 层抽象基类
│   ├── LinearLayer.h # 全连接层
│   ├── Model.h       # 模型类
│   └── Utils.h       # 工具函数（计时器、误差计算等）
├── src/              # 源文件
│   ├── Tensor.cpp
│   ├── LinearLayer.cpp
│   ├── Model.cpp
│   ├── Utils.cpp
│   └── main.cpp      # 主程序（端到端推理流程）
├── data/             # 模型数据目录
│   ├── model_fp32.bin # FP32模型权重文件（必需）
│   └── TinyStories-1M-main/ # TinyStories-1M原始模型文件
├── output/           # 输出目录（自动创建）
│   ├── model_int8_e2e.bin # 量化后的INT8模型
│   ├── quant_stats_e2e.txt # 每层的量化缩放因子
│   └── accuracy_log_e2e.txt # FP32与INT8输出的精度对比
├── build/            # 构建目录（自动创建）
├── CMakeLists.txt    # CMake构建文件
├── compile.bat       # Windows编译脚本
├── build.sh          # Linux/macOS编译脚本
├── run.bat           # Windows运行脚本
└── run.sh            # Linux/macOS运行脚本
```

## 编译方法

### 使用CMake（推荐）

```bash
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

### 使用Visual Studio

1. 打开Visual Studio
2. 选择"打开文件夹"，选择`cplus`目录
3. Visual Studio会自动检测CMakeLists.txt
4. 选择配置（Debug/Release）
5. 生成 -> 生成解决方案

### 手动编译（Windows）

```powershell
# 使用MSVC编译器
cl /EHsc /std:c++17 /I include src\*.cpp /Fe:inference_engine.exe
```

## 使用方法

### 1. 准备模型权重文件

首先需要将模型权重转换为项目要求的二进制格式，并保存到`data/model_fp32.bin`。

文件格式：

```
[4字节：层数]
[每层：层类型(4字节) + 维度信息 + 权重数据(float32)]
```

### 2. 运行程序

```bash
./inference_engine
```

或

```powershell
.\bin\Release\inference_engine.exe
```

### 3. 查看输出

程序会在`output/`目录下生成：

- `model_int8_e2e.bin`: 量化后的INT8模型
- `quant_stats_e2e.txt`: 每层的量化缩放因子统计
- `accuracy_log_e2e.txt`: FP32与INT8输出的逐元素精度对比

## 功能特性

- ✅ **自实现Tensor库**：支持`float`和`int8_t`两种类型的多维张量
- ✅ **对称INT8量化**：采用逐张量（per-tensor）对称量化方案
- ✅ **层间INT8传递**：推理过程中层与层之间传递INT8数据，提升效率
- ✅ **全连接层支持**：实现LinearLayer的FP32和INT8两种前向传播
- ✅ **端到端推理**：支持完整的FP32→INT8量化推理流程
- ✅ **精度评估**：自动计算MSE、MAE、最大误差等精度指标
- ✅ **性能对比**：对比FP32和INT8推理的耗时和加速比
- ✅ **模型压缩**：实现约4倍的模型大小压缩（FP32→INT8）
- ✅ **统计报告**：自动生成量化统计和精度日志文件

## 依赖

- C++17标准库
- 无第三方依赖

## 量化方案说明

本项目采用**对称、逐张量的INT8量化方案**：

- **量化公式**：`q = round(x / scale)`，其中 `scale = max_abs / 127.0`
- **反量化公式**：`x = q * scale`
- **推理流程**：
  1. 输入量化：FP32输入 → INT8输入
  2. 逐层处理：INT8权重 × INT8输入 → INT32累加 → 反量化 → 加偏置 → 重新量化为INT8
  3. 层间传递：层与层之间传递INT8数据
  4. 最终输出：最后一层INT8输出 → 反量化回FP32

## 目标模型

本项目针对 **TinyStories-1M** 模型：

- 8个Transformer块
- 每个块包含：4个Attention相关全连接层（Q/K/V/Out）+ 2个MLP相关全连接层（FC/Proj）
- 总计：**48个线性层**

## 注意事项

1. **模型权重文件**：需要将TinyStories-1M模型转换为项目要求的二进制格式，保存为`data/model_fp32.bin`

2. **文件格式**：

   ```
   [4字节：层数]
   [每层：层类型(4字节) + 名称长度和名称 + 维度信息 + 权重数据(float32) + 偏置标志和偏置]
   ```

3. **编译要求**：需要支持C++17标准的编译器

4. **当前实现**：为演示和教学目的，主要展示量化原理，矩阵乘法采用简单实现

## 输出文件说明

运行程序后，`output/`目录下会生成：

- **`model_int8_e2e.bin`**：量化后的INT8模型文件，可用于后续推理
- **`quant_stats_e2e.txt`**：每层的量化缩放因子，格式为"层名\t缩放因子"
- **`accuracy_log_e2e.txt`**：前10个样本的FP32与INT8输出对比，包括逐元素误差

## 技术细节

- **代码风格**：源文件使用`using namespace std;`，头文件保留`std::`前缀（符合C++最佳实践）
- **无第三方依赖**：仅使用C++17标准库
- **跨平台支持**：提供Windows（CMake/批处理）和Linux/macOS（CMake/Bash）构建脚本

## 许可证

本项目为课程作业项目。
