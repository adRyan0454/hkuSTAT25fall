#ifndef TENSOR_H
#define TENSOR_H

#include <vector>
#include <cstdint>
#include <cstddef>
#include <stdexcept>

/**
 * @brief 张量模板类，支持float和int8_t类型
 * 
 * 提供多维数组的基本操作，包括元素访问、算术运算、量化/反量化等
 */
template<typename T>
class Tensor {
private:
    std::vector<T> data_;           // 连续存储的数据
    std::vector<size_t> shape_;      // 形状信息
    size_t total_size_;              // 总元素数量

    // 计算线性索引
    size_t compute_index(const std::vector<size_t>& indices) const;

public:
    // 构造函数
    Tensor();
    Tensor(const std::vector<size_t>& shape);
    Tensor(const std::vector<size_t>& shape, const std::vector<T>& data);
    
    // 拷贝构造和赋值
    Tensor(const Tensor& other);
    Tensor& operator=(const Tensor& other);
    
    // 移动构造和赋值
    Tensor(Tensor&& other) noexcept;
    Tensor& operator=(Tensor&& other) noexcept;

    // 基本访问
    const std::vector<size_t>& shape() const { return shape_; }
    size_t size() const { return total_size_; }
    size_t dims() const { return shape_.size(); }
    
    // 数据访问
    T* data() { return data_.data(); }
    const T* data() const { return data_.data(); }
    
    // 元素访问
    T& operator()(const std::vector<size_t>& indices);
    const T& operator()(const std::vector<size_t>& indices) const;
    T& operator[](size_t index) { return data_[index]; }
    const T& operator[](size_t index) const { return data_[index]; }
    
    // 算术运算
    Tensor<T> operator+(const Tensor<T>& other) const;
    Tensor<T> operator-(const Tensor<T>& other) const;
    Tensor<T> operator*(const Tensor<T>& other) const;  // 逐元素乘法
    Tensor<T> operator*(T scalar) const;                // 标量乘法
    
    // 矩阵乘法（仅支持2D张量）
    Tensor<T> matmul(const Tensor<T>& other) const;
    
    // 重塑形状
    Tensor<T> reshape(const std::vector<size_t>& new_shape) const;
    
    // 量化相关（仅对float类型有效）
    void quantize(float scale, std::vector<int8_t>& out) const;
    static Tensor<float> dequantize(const std::vector<int8_t>& qdata, 
                                     float scale, 
                                     const std::vector<size_t>& shape);
    
    // 工具函数
    void fill(T value);
    T max() const;
    T min() const;
    T abs_max() const;  // 最大绝对值，用于计算缩放因子
    
    // 打印（用于调试）
    void print() const;
};

// 显式实例化声明
extern template class Tensor<float>;
extern template class Tensor<int8_t>;

#endif // TENSOR_H
