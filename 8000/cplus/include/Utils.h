#ifndef UTILS_H
#define UTILS_H

#include "Tensor.h"
#include <string>
#include <chrono>
#include <fstream>
#include <vector>

/**
 * @brief 工具函数集合
 */

namespace Utils {

/**
 * @brief 计时器类
 */
class Timer {
private:
    std::chrono::high_resolution_clock::time_point start_time_;
    std::chrono::high_resolution_clock::time_point end_time_;
    bool is_running_;

public:
    Timer();
    void start();
    void stop();
    double elapsed_ms() const;  // 返回毫秒
    double elapsed_us() const;   // 返回微秒
};

/**
 * @brief 计算MSE（均方误差）
 */
float compute_mse(const Tensor<float>& a, const Tensor<float>& b);

/**
 * @brief 计算MAE（平均绝对误差）
 */
float compute_mae(const Tensor<float>& a, const Tensor<float>& b);

/**
 * @brief 计算最大误差
 */
float compute_max_error(const Tensor<float>& a, const Tensor<float>& b);

/**
 * @brief 确保目录存在
 */
void ensure_directory(const std::string& dirpath);

/**
 * @brief 写入量化统计信息
 */
void write_quant_stats(const std::string& filepath,
                      const std::vector<std::string>& layer_names,
                      const std::vector<float>& scales);

/**
 * @brief 写入精度日志
 */
void write_accuracy_log(const std::string& filepath,
                       const Tensor<float>& fp32_output,
                       const Tensor<float>& int8_output,
                       size_t num_samples = 10);

/**
 * @brief 计算量化缩放因子
 */
float compute_scale(const Tensor<float>& tensor);

/**
 * @brief 量化单个浮点值到int8
 */
int8_t quantize_value(float value, float scale);

} // namespace Utils

#endif // UTILS_H
