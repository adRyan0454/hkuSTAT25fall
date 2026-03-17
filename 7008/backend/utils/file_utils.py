"""
文件上传工具
"""
import os
import uuid
from datetime import datetime
from fastapi import UploadFile


async def save_upload_file(file: UploadFile, upload_dir: str = "uploads") -> str:
    """
    保存上传的文件
    
    Args:
        file: 上传的文件
        upload_dir: 上传目录
        
    Returns:
        文件保存路径
    """
    # 确保上传目录存在
    os.makedirs(upload_dir, exist_ok=True)
    
    # 获取文件扩展名
    file_ext = os.path.splitext(file.filename)[1]
    
    # 生成唯一文件名
    unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{file_ext}"
    
    # 文件保存路径
    file_path = os.path.join(upload_dir, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return file_path


def delete_file(file_path: str) -> bool:
    """
    删除文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        是否删除成功
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


