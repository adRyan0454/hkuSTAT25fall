#include "../include/LinearLayer.h"
#include <cmath>
#include <algorithm>
#include <cstring>
#include <stdexcept>

using namespace std;

LinearLayer::LinearLayer(const string& name, 
                         size_t in_features, 
                         size_t out_features, 
                         bool has_bias)
    : name_(name), 
      weight_({out_features, in_features}),
      weight_scale_(1.0f),
      output_scale_(1.0f),
      is_quantized_(false) {
    if (has_bias) {
        bias_ = Tensor<float>({out_features});
    }
}

float LinearLayer::compute_weight_scale() const {
    float max_abs = weight_.abs_max();
    if (max_abs == 0.0f) {
        return 1.0f;
    }
    // 对称量化：scale = max(abs(weight)) / 127.0
    return max_abs / 127.0f;
}

void LinearLayer::quantize_weights() {
    weight_scale_ = compute_weight_scale();
    
    // 量化权重
    vector<int8_t> quantized_data;
    weight_.quantize(weight_scale_, quantized_data);
    
    weight_quantized_ = Tensor<int8_t>(weight_.shape());
    memcpy(weight_quantized_.data(), quantized_data.data(), 
                quantized_data.size() * sizeof(int8_t));
    
    is_quantized_ = true;
}

Tensor<float> LinearLayer::forward(const Tensor<float>& input) {
    // 检查输入形状
    if (input.dims() != 2 || input.shape()[1] != weight_.shape()[1]) {
        throw runtime_error("LinearLayer: 输入形状不匹配");
    }
    
    // 矩阵乘法: output = input * weight^T
    // input: [batch, in_features], weight: [out_features, in_features]
    // 需要转置weight: [in_features, out_features]
    // 但我们的matmul是 input * weight，所以需要调整
    
    // 简化实现：手动计算 output = input * weight^T + bias
    size_t batch_size = input.shape()[0];
    size_t in_features = weight_.shape()[1];
    size_t out_features = weight_.shape()[0];
    
    Tensor<float> output({batch_size, out_features});
    
    for (size_t b = 0; b < batch_size; ++b) {
        for (size_t o = 0; o < out_features; ++o) {
            float sum = 0.0f;
            for (size_t i = 0; i < in_features; ++i) {
                sum += input[b * in_features + i] * weight_[o * in_features + i];
            }
            if (bias_.size() > 0) {
                sum += bias_[o];
            }
            output[b * out_features + o] = sum;
        }
    }
    
    return output;
}

Tensor<int8_t> LinearLayer::forward_quantized(const Tensor<int8_t>& input, 
                                               float in_scale, 
                                               float& out_scale) {
    if (!is_quantized_) {
        throw runtime_error("LinearLayer: 权重尚未量化");
    }
    
    // 检查输入形状
    if (input.dims() != 2 || input.shape()[1] != weight_quantized_.shape()[1]) {
        throw runtime_error("LinearLayer: 输入形状不匹配");
    }
    
    size_t batch_size = input.shape()[0];
    size_t in_features = weight_quantized_.shape()[1];
    size_t out_features = weight_quantized_.shape()[0];
    
    // 先计算浮点输出以确定输出范围
    Tensor<float> output_fp({batch_size, out_features});
    float combined_scale = weight_scale_ * in_scale;
    
    for (size_t b = 0; b < batch_size; ++b) {
        for (size_t o = 0; o < out_features; ++o) {
            int32_t sum = 0;
            for (size_t i = 0; i < in_features; ++i) {
                int8_t w = weight_quantized_[o * in_features + i];
                int8_t x = input[b * in_features + i];
                sum += static_cast<int32_t>(w) * static_cast<int32_t>(x);
            }
            
            // 反量化并添加偏置
            float result = static_cast<float>(sum) * combined_scale;
            if (bias_.size() > 0) {
                result += bias_[o];
            }
            output_fp[b * out_features + o] = result;
        }
    }
    
    // 计算输出缩放因子
    float max_abs = output_fp.abs_max();
    output_scale_ = (max_abs > 0.0f) ? (max_abs / 127.0f) : 1.0f;
    out_scale = output_scale_;
    
    // 量化输出
    vector<int8_t> output_quantized;
    output_fp.quantize(output_scale_, output_quantized);
    
    Tensor<int8_t> output({batch_size, out_features});
    memcpy(output.data(), output_quantized.data(), 
                output_quantized.size() * sizeof(int8_t));
    
    return output;
}

void LinearLayer::load_weights(std::ifstream& fin) {
    // 读取层类型（应该是1）
    int32_t layer_type;
    fin.read(reinterpret_cast<char*>(&layer_type), sizeof(int32_t));
    
    // 读取层名称
    uint32_t name_len;
    fin.read(reinterpret_cast<char*>(&name_len), sizeof(uint32_t));
    string file_name(name_len, '\0');
    fin.read(&file_name[0], name_len);
    
    // 读取维度
    uint32_t out_features, in_features;
    fin.read(reinterpret_cast<char*>(&out_features), sizeof(uint32_t));
    fin.read(reinterpret_cast<char*>(&in_features), sizeof(uint32_t));
    
    // 验证维度是否匹配
    if (out_features != weight_.shape()[0] || in_features != weight_.shape()[1]) {
        throw runtime_error("LinearLayer: 文件中的维度与层定义不匹配");
    }
    
    // 读取权重数据
    size_t weight_size = out_features * in_features;
    fin.read(reinterpret_cast<char*>(weight_.data()), 
             weight_size * sizeof(float));
    
    // 读取偏置标志
    bool has_bias_in_file;
    fin.read(reinterpret_cast<char*>(&has_bias_in_file), sizeof(bool));
    
    // 读取偏置（如果有）
    if (has_bias_in_file && bias_.size() > 0) {
        fin.read(reinterpret_cast<char*>(bias_.data()), 
                 out_features * sizeof(float));
    } else if (has_bias_in_file) {
        // 文件有偏置但层没有，跳过
        fin.seekg(out_features * sizeof(float), ios::cur);
    }
}

void LinearLayer::save_quantized(ofstream& fout) const {
    if (!is_quantized_) {
        throw runtime_error("LinearLayer: 权重尚未量化，无法保存");
    }
    
    // 写入层类型标识（1 = LinearLayer）
    int32_t layer_type = 1;
    fout.write(reinterpret_cast<const char*>(&layer_type), sizeof(int32_t));
    
    // 写入层名称长度和名称
    size_t name_len = name_.length();
    fout.write(reinterpret_cast<const char*>(&name_len), sizeof(size_t));
    fout.write(name_.c_str(), name_len);
    
    // 写入权重缩放因子
    fout.write(reinterpret_cast<const char*>(&weight_scale_), sizeof(float));
    
    // 写入权重形状和量化权重
    size_t out_features = weight_quantized_.shape()[0];
    size_t in_features = weight_quantized_.shape()[1];
    fout.write(reinterpret_cast<const char*>(&out_features), sizeof(size_t));
    fout.write(reinterpret_cast<const char*>(&in_features), sizeof(size_t));
    
    size_t weight_size = out_features * in_features;
    fout.write(reinterpret_cast<const char*>(weight_quantized_.data()), 
               weight_size * sizeof(int8_t));
    
    // 写入偏置（如果有，仍为float）
    bool has_bias = (bias_.size() > 0);
    fout.write(reinterpret_cast<const char*>(&has_bias), sizeof(bool));
    if (has_bias) {
        fout.write(reinterpret_cast<const char*>(bias_.data()), 
                   out_features * sizeof(float));
    }
}

size_t LinearLayer::get_in_features() const {
    return weight_.shape()[1];
}

size_t LinearLayer::get_out_features() const {
    return weight_.shape()[0];
}

bool LinearLayer::has_bias() const {
    return bias_.size() > 0;
}
