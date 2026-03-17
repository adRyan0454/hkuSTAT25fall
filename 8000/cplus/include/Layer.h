#ifndef LAYER_H
#define LAYER_H

#include "Tensor.h"
#include <fstream>
#include <string>

/**
 * @brief 神经网络层的抽象基类
 * 
 * 所有层都需要实现浮点前向传播和量化前向传播
 */
class Layer {
public:
    virtual ~Layer() = default;
    
    /**
     * @brief 浮点前向传播
     * @param input 浮点输入张量
     * @return 浮点输出张量
     */
    virtual Tensor<float> forward(const Tensor<float>& input) = 0;
    
    /** 
     * @brief 量化前向传播（INT8输入，INT8输出）
     * @param input 量化输入张量（int8_t）
     * @param in_scale 输入缩放因子
     * @param out_scale 输出缩放因子（引用，由层设置）
     * @return 量化输出张量（int8_t）
     */
    virtual Tensor<int8_t> forward_quantized(const Tensor<int8_t>& input, 
                                              float in_scale, 
                                              float& out_scale) = 0;
    
    /**
     * @brief 获取权重缩放因子（用于量化）
     * @return 权重缩放因子
     */
    virtual float get_weight_scale() const = 0;
    
    /**
     * @brief 获取输出缩放因子（用于量化）
     * @return 输出缩放因子
     */
    virtual float get_output_scale() const = 0;
    
    /**
     * @brief 从二进制流加载权重
     * @param fin 输入文件流
     */
    virtual void load_weights(std::ifstream& fin) = 0;
    
    /**
     * @brief 保存量化权重到文件
     * @param fout 输出文件流
     */
    virtual void save_quantized(std::ofstream& fout) const = 0;
    
    /**
     * @brief 执行权重量化
     */
    virtual void quantize_weights() = 0;
    
    /**
     * @brief 获取层名称
     * @return 层名称字符串
     */
    virtual std::string get_name() const = 0;
};

#endif // LAYER_H
