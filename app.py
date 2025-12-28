"""
基于 ResNet18 的工业零件表面缺陷分类 Web 演示应用
使用 Streamlit 框架实现
"""

import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import os

# 设置页面配置
st.set_page_config(
    page_title="工业零件表面缺陷智能检测系统",
    page_icon="🏭",
    layout="wide"
)

# ============================================
# 1. 定义类别名称（与训练时一致）
# ============================================
class_names = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']
class_names_cn = {
    'crazing': '裂纹',
    'inclusion': '夹杂',
    'patches': '斑块',
    'pitted_surface': '麻点',
    'rolled-in_scale': '氧化皮',
    'scratches': '划痕'
}

# ============================================
# 2. 定义模型结构（必须与训练时完全一致）
# ============================================
@st.cache_resource
def load_model():
    """加载训练好的模型，使用缓存加速"""
    # 加载预训练的 ResNet18
    model = models.resnet18(pretrained=False)
    
    # 获取原始全连接层的输入特征数
    num_ftrs = model.fc.in_features
    
    # 修改全连接层（与训练时一致：Linear(输入,256) -> ReLU -> Linear(256,6)）
    model.fc = nn.Sequential(
        nn.Linear(num_ftrs, 256),
        nn.ReLU(),
        nn.Linear(256, 6)
    )
    
    # 加载训练好的权重
    if os.path.exists('best_model.pth'):
        model.load_state_dict(torch.load('best_model.pth', map_location='cpu'))
        st.success("✅ 模型加载成功！")
    else:
        st.error("❌ 未找到模型文件 'best_model.pth'，请先运行 train.py 训练模型")
        return None
    
    # 设置为评估模式
    model.eval()
    return model

# ============================================
# 3. 定义图像预处理（与验证集一致）
# ============================================
def preprocess_image(image):
    """对上传的图像进行预处理"""
    # 定义预处理变换（与验证集一致）
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # 应用预处理
    image_tensor = preprocess(image)
    # 添加batch维度
    image_tensor = image_tensor.unsqueeze(0)
    return image_tensor

# ============================================
# 4. 模型推理函数
# ============================================
def predict(image, model):
    """对图像进行预测"""
    # 预处理图像
    image_tensor = preprocess_image(image)
    
    # 进行推理
    with torch.no_grad():
        outputs = model(image_tensor)
        # 获取预测结果
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        # 获取最大概率的类别
        confidence, predicted_idx = torch.max(probabilities, 0)
    
    # 转换为Python类型
    predicted_class = class_names[predicted_idx.item()]
    confidence_percent = confidence.item() * 100
    
    return predicted_class, confidence_percent, probabilities.numpy()

# ============================================
# 5. Streamlit 主界面
# ============================================
def main():
    # 页面标题
    st.title("🏭 工业零件表面缺陷智能检测系统")
    st.markdown("---")
    
    # 创建侧边栏
    with st.sidebar:
        st.header("📖 项目介绍")
        st.markdown("""
        本系统基于 **ResNet18** 深度学习模型，用于识别工业零件表面的6种常见缺陷：
        - **裂纹** - 表面出现细小裂纹
        - **夹杂** - 表面嵌入异物
        - **斑块** - 表面出现斑块状缺陷
        - **麻点** - 表面出现细小凹坑
        - **氧化皮** - 表面氧化形成的鳞片
        - **划痕** - 表面被划伤的痕迹
        
        **技术特点：**
        - 迁移学习：利用 ImageNet 预训练模型
        - 参数冻结：冻结前8层，仅训练全连接层
        - 数据增强：提高模型泛化能力
        - 高精度：验证集准确率达 98.33%
        """)
        
        st.markdown("---")
        
        st.header("📋 使用说明")
        st.markdown("""
        1. 点击下方 **"上传图片"** 区域
        2. 选择一张工业零件图片（支持 JPG/PNG 格式）
        3. 系统将自动进行缺陷检测
        4. 查看检测结果和各类别置信度分布
        """)
        
        st.markdown("---")
        
        st.info("💡 提示：建议上传清晰的工业零件表面图片以获得最佳检测效果")
    
    # 主内容区域
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 上传待检测图片")
        uploaded_file = st.file_uploader(
            "请选择一张工业零件图片",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # 读取并显示图片
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption="上传的图片", use_column_width=True)
    
    with col2:
        st.subheader("🔍 检测结果")
        
        if uploaded_file is not None:
            # 加载模型（使用缓存）
            model = load_model()
            
            if model is not None:
                # 进行预测
                with st.spinner("正在分析图片..."):
                    predicted_class, confidence, probabilities = predict(image, model)
                
                # 显示预测结果
                st.markdown(f"""
                <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #2e7d32; font-size: 24px;">{class_names_cn[predicted_class]}</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">{predicted_class}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #2196f3;">
                    <h3 style="margin: 0; color: #1565c0; font-size: 24px;">置信度: {confidence:.2f}%</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # 显示所有类别的概率
                st.markdown("---")
                st.subheader("📊 各类别概率分布")
                
                # 创建概率条形图
                prob_data = []
                for i, class_name in enumerate(class_names):
                    prob_data.append({
                        '类别': class_names_cn[class_name],
                        '英文': class_name,
                        '概率': probabilities[i] * 100
                    })
                
                # 排序并显示
                prob_data_sorted = sorted(prob_data, key=lambda x: x['概率'], reverse=True)
                
                # 使用进度条显示概率
                for item in prob_data_sorted:
                    # 根据概率设置颜色
                    if item['概率'] >= 80:
                        color = "#4caf50"  # 绿色
                    elif item['概率'] >= 50:
                        color = "#ff9800"  # 橙色
                    else:
                        color = "#f44336"  # 红色
                    
                    st.markdown(f"""
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold;">{item['类别']}</span>
                            <span style="color: {color}; font-weight: bold;">{item['概率']:.2f}%</span>
                        </div>
                        <div style="background-color: #e0e0e0; border-radius: 5px; height: 25px; overflow: hidden;">
                            <div style="background-color: {color}; height: 100%; width: {item['概率']}%; transition: width 0.3s ease;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 使用 Streamlit 的 bar chart
                import pandas as pd
                df = pd.DataFrame(prob_data_sorted)
                df_display = df[['类别', '概率']].set_index('类别')
                st.bar_chart(df_display)
                
                # 显示详细数据表格
                st.markdown("---")
                st.subheader("📈 详细数据")
                df_table = pd.DataFrame(prob_data_sorted)
                df_table = df_table.rename(columns={'类别': '中文类别', '英文': '英文类别', '概率': '置信度(%)'})
                st.dataframe(df_table, use_container_width=True, hide_index=True)
        
        else:
            # 等待上传提示
            st.info("👈 请在左侧上传图片进行检测")
            st.markdown("""
            <div style="text-align: center; padding: 50px; color: #999;">
                <p style="font-size: 18px;">暂无图片</p>
                <p style="font-size: 14px;">请上传工业零件表面图片开始检测</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
        <p>🏭 基于 ResNet18 的工业零件表面缺陷智能检测系统</p>
        <p>《人工智能应用技术》期末课程作业</p>
        <p>验证集准确率: <strong>98.33%</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
