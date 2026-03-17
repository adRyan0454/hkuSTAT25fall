#ifndef MODEL_H
#define MODEL_H

#include "Layer.h"
#include "LinearLayer.h"
#include <vector>
#include <memory>
#include <fstream>
#include <string>

/**
 * @brief 模型类，组合多个层
 * 
 * 管理模型的前向传播、量化、权重加载等功能
 */
class Model {
private:
    std::vector<std::unique_ptr<Layer>> layers_;
    std::string model_name_;
    
    // 量化相关
    std::vector<float> layer_scales_;  // 每层的缩放因子
    bool is_quantized_;

public:
    Model(const std::string& name = "Model");
    
    // 添加层
    void add_layer(std::unique_ptr<Layer> layer);
    
    // 加载权重
    void load_weights(const std::string& filepath);
    
    // 前向传播
    Tensor<float> forward(const Tensor<float>& input);
    Tensor<float> forward_quantized(const Tensor<float>& input);
    
    // 量化
    void quantize();
    
    // 保存量化模型
    void save_quantized(const std::string& filepath) const;
    
    // 获取信息
    size_t num_layers() const { return layers_.size(); }
    const std::string& get_name() const { return model_name_; }
    bool is_quantized() const { return is_quantized_; }
    
    // 获取层缩放因子（用于统计）
    const std::vector<float>& get_layer_scales() const { return layer_scales_; }
};

#endif // MODEL_H
