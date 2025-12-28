#!/bin/bash
# ============================================
# 基于 ResNet 的工业零件表面缺陷检测系统 - Mac/Linux 训练脚本
# ============================================

echo "🏭 基于 ResNet 的工业零件表面缺陷检测系统 - 模型训练"
echo "============================================"
echo ""

# 检查 conda 环境是否存在
if ! command -v conda &> /dev/null; then
    echo "❌ 错误：未找到 conda 环境"
    echo "请先安装 Miniconda 或 Anaconda"
    exit 1
fi

# 检查 conda 环境名称
ENV_NAME="uu"
if ! conda env list | grep -q "^${ENV_NAME}\s"; then
    echo "📦 创建 conda 环境: ${ENV_NAME}"
    conda create -n ${ENV_NAME} python=3.9 -y
    echo "✅ 环境创建完成"
else
    echo "✅ conda 环境 ${ENV_NAME} 已存在"
fi

# 激活 conda 环境
echo "🔄 激活 conda 环境: ${ENV_NAME}"
source $(conda info --root)/bin/activate ${ENV_NAME}

# 检查是否安装了必要的包
echo ""
echo "📋 检查依赖包..."

if ! python -c "import torch" 2>/dev/null; then
    echo "📦 安装依赖包..."
    pip install -r requirements.txt
fi

# 检查数据集
echo ""
echo "📁 检查数据集..."

if [ ! -d "data/train/images" ]; then
    echo "❌ 错误：未找到训练数据集"
    echo "请确保 data/train/images 目录存在且包含按类别分类的图片"
    exit 1
fi

if [ ! -d "data/validation/images" ]; then
    echo "❌ 错误：未找到验证数据集"
    echo "请确保 data/validation/images 目录存在且包含按类别分类的图片"
    exit 1
fi

echo "✅ 数据集检查完成"

# 开始训练
echo ""
echo "🚀 开始训练模型..."
echo "============================================"
echo ""

python train.py

echo ""
echo "============================================"
echo "✅ 训练完成！"
echo "📊 训练曲线已保存为: training_curve.png"
echo "💾 最佳模型已保存为: best_model.pth"
echo ""
echo "💡 接下来可以运行以下命令启动 Web 演示界面："
echo "   Mac/Linux: ./run.sh"
echo "   Windows:   run.bat"
echo "============================================"
