#include "../include/Model.h"
#include <iostream>
#include <cstring>
#include <stdexcept>

using namespace std;

Model::Model(const string& name) 
    : model_name_(name), is_quantized_(false) {}

void Model::add_layer(unique_ptr<Layer> layer) {
    layers_.push_back(move(layer));
}

void Model::load_weights(const string& filepath) {
    ifstream fin(filepath, ios::binary);
    if (!fin.is_open()) {
        throw runtime_error("无法打开模型文件: " + filepath);
    }
    
    // 读取文件头：层数
    int32_t num_layers;
    fin.read(reinterpret_cast<char*>(&num_layers), sizeof(int32_t));
    
    if (num_layers != static_cast<int32_t>(layers_.size())) {
        throw runtime_error("模型文件中的层数与模型定义不匹配");
    }
    
    // 依次加载每层的权重
    for (auto& layer : layers_) {
        layer->load_weights(fin);
    }
    
    fin.close();
    cout << "成功加载 " << num_layers << " 层权重\n";
}

Tensor<float> Model::forward(const Tensor<float>& input) {
    Tensor<float> output = input;
    
    for (auto& layer : layers_) {
        output = layer->forward(output);
    }
    
    return output;
}

Tensor<float> Model::forward_quantized(const Tensor<float>& input) {
    if (!is_quantized_) {
        throw runtime_error("模型尚未量化，无法执行量化推理");
    }
    
    if (layers_.empty()) {
        return input;
    }
    
    // 计算输入缩放因子
    float max_abs = input.abs_max();
    float input_scale = (max_abs > 0.0f) ? (max_abs / 127.0f) : 1.0f;
    
    // 量化输入
    vector<int8_t> input_quantized;
    input.quantize(input_scale, input_quantized);
    
    Tensor<int8_t> current_int8(input.shape());
    memcpy(current_int8.data(), input_quantized.data(), 
                input_quantized.size() * sizeof(int8_t));
    
    float current_scale = input_scale;
    
    // 逐层进行INT8推理
    for (size_t i = 0; i < layers_.size(); ++i) {
        float out_scale = 1.0f;
        current_int8 = layers_[i]->forward_quantized(current_int8, current_scale, out_scale);
        current_scale = out_scale;
    }
    
    // 最后反量化为浮点输出
    Tensor<float> output = Tensor<float>::dequantize(
        vector<int8_t>(current_int8.data(), current_int8.data() + current_int8.size()),
        current_scale,
        current_int8.shape()
    );
    
    return output;
}

void Model::quantize() {
    layer_scales_.clear();
    
    for (auto& layer : layers_) {
        layer->quantize_weights();
        layer_scales_.push_back(layer->get_weight_scale());
    }
    
    is_quantized_ = true;
    cout << "模型量化完成，共 " << layers_.size() << " 层\n";
}

void Model::save_quantized(const string& filepath) const {
    if (!is_quantized_) {
        throw runtime_error("模型尚未量化，无法保存");
    }
    
    ofstream fout(filepath, ios::binary);
    if (!fout.is_open()) {
        throw runtime_error("无法创建输出文件: " + filepath);
    }
    
    // 写入层数
    int32_t num_layers = static_cast<int32_t>(layers_.size());
    fout.write(reinterpret_cast<const char*>(&num_layers), sizeof(int32_t));
    
    // 写入每层的量化权重
    for (const auto& layer : layers_) {
        layer->save_quantized(fout);
    }
    
    fout.close();
    cout << "量化模型已保存到: " << filepath << "\n";
}
