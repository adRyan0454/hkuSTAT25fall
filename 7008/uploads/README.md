# Uploads 目录说明

## 📁 目录用途

此目录用于存储系统运行时产生的所有上传文件。

## 📂 建议的目录结构

```
uploads/
├── employees/          # 员工相关文件
│   ├── photos/        # 员工照片
│   └── documents/     # 员工文档
├── announcements/      # 公告附件
├── performance/        # 绩效相关文件
└── temp/              # 临时文件
```

## 🔒 安全注意事项

1. **文件验证**
   - 验证文件类型（只允许图片、PDF等）
   - 限制文件大小（如最大10MB）
   - 检查文件内容（防止恶意文件）

2. **访问控制**
   - 需要登录才能访问
   - 员工只能访问自己的文件
   - 管理员可以访问所有文件

3. **文件命名**
   - 使用UUID或时间戳重命名
   - 避免中文和特殊字符
   - 保留原始扩展名

## 📝 使用示例

### 上传文件（前端）

```javascript
// Vue前端上传示例
const formData = new FormData()
formData.append('file', file)

const res = await uploadPhoto(formData)
console.log('文件路径:', res.data.file_path)
// 输出: /uploads/employees/photos/uuid-xxx.jpg
```

### 保存文件（后端）

```python
# backend/utils/file_utils.py
import os
import uuid
from fastapi import UploadFile

async def save_upload_file(file: UploadFile, subdir: str = "employees/photos"):
    # 生成唯一文件名
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    
    # 创建完整路径
    upload_dir = f"uploads/{subdir}"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = f"{upload_dir}/{filename}"
    
    # 保存文件
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return f"/{file_path}"
```

### 访问文件

```html
<!-- 在Vue前端中显示图片 -->
<img :src="`http://localhost:8000${employee.photo_path}`" alt="员工照片" />

<!-- 实际访问 -->
<!-- http://localhost:8000/uploads/employees/photos/uuid-xxx.jpg -->
```

## 🧹 清理建议

定期清理临时文件和无用文件：

```python
# 清理脚本示例
import os
import time

def clean_temp_files(max_age_days=7):
    """清理7天前的临时文件"""
    temp_dir = "uploads/temp"
    now = time.time()
    
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        if os.path.isfile(file_path):
            # 检查文件年龄
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age_days * 86400:
                os.remove(file_path)
                print(f"已删除: {file_path}")
```

## ⚠️ 重要提示

1. **不要提交到Git**
   - 此目录在 `.gitignore` 中
   - 上传的文件不应该被版本控制
   - 生产环境使用云存储（如阿里云OSS）

2. **备份策略**
   - 定期备份重要文件
   - 使用云存储服务
   - 设置自动备份任务

3. **磁盘空间**
   - 监控磁盘使用情况
   - 设置文件大小限制
   - 定期清理无用文件

## 📊 文件统计

可以添加文件统计功能：

```python
import os

def get_upload_stats():
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk("uploads"):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            file_count += 1
    
    return {
        "file_count": file_count,
        "total_size_mb": total_size / 1024 / 1024
    }
```

## 🚀 生产环境建议

生产环境推荐使用云存储服务：

- **阿里云OSS**
- **腾讯云COS**
- **AWS S3**
- **七牛云**

优势：
- ✅ 高可用性
- ✅ CDN加速
- ✅ 自动备份
- ✅ 不占用服务器空间
- ✅ 更好的安全性

