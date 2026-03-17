#ifndef LINEAR_LAYER_H
#define LINEAR_LAYER_H

#include "Layer.h"
#include <vector>
#include <cstdint>

/**
 * @brief 全连接层（线性层）
 * 
 * 实现 y = xW^T + b
 * 支持浮点和INT8量化推理
 */
class LinearLayer : public Layer {
private:
    std::string name_;                    // 层名称
    Tensor<float> weight_;                 // 权重矩阵 [out_features, in_features]
    Tensor<float> bias_;                  // 偏置向量 [out_features]
    Tensor<int8_t> weight_quantized_;     // 量化后的权重
    float weight_scale_;                  // 权重缩放因子
    float output_scale_;                  // 输出缩放因子
    bool is_quantized_;                   // 是否已量化
    
    // 计算权重的缩放因子
    float compute_weight_scale() const;

public:
    /**
     * @brief 构造函数
     * @param name 层名称
     * @param in_features 输入特征数
     * @param out_features 输出特征数
     * @param has_bias 是否有偏置
     */
    LinearLayer(const std::string& name, 
                size_t in_features, 
                size_t out_features, 
                bool has_bias = true);
    
    // Layer接口实现
    Tensor<float> forward(const Tensor<float>& input) override;
    Tensor<int8_t> forward_quantized(const Tensor<int8_t>& input, 
                                      float in_scale, 
                                      float& out_scale) override;
    float get_weight_scale() const override { return weight_scale_; }
    float get_output_scale() const override { return output_scale_; }
    void load_weights(std::ifstream& fin) override;
    void save_quantized(std::ofstream& fout) const override;
    void quantize_weights() override;
    std::string get_name() const override { return name_; }
    
    // 获取层信息
    size_t get_in_features() const;
    size_t get_out_features() const;
    bool has_bias() const;
};

#endif // LINEAR_LAYER_H
