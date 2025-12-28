#!/bin/bash
# ============================================
# 基于 ResNet 的工业零件表面缺陷检测系统 - Mac/Linux 启动脚本
# ============================================

echo "🏭 基于 ResNet 的工业零件表面缺陷检测系统"
echo "============================================"
echo ""

# 检查 conda 环境是否存在
if ! command -v conda &> /dev/null; then
    echo "❌ 错误：未找到 conda 环境"
    echo "请先安装 Miniconda 或 Anaconda"
    echo "下载地址：https://docs.conda.io/en/latest/miniconda.html"
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

# 检查 Python 版本
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "🐍 Python 版本: ${PYTHON_VERSION}"

# 检查是否安装了必要的包
echo ""
echo "📋 检查依赖包..."

check_package() {
    if python -c "import $1" 2>/dev/null; then
        echo "  ✅ $1"
    else
        echo "  ❌ $1 (未安装)"
    fi
}

check_package "torch"
check_package "torchvision"
check_package "matplotlib"
check_package "streamlit"
check_package "PIL"

# 检查必要文件是否存在
echo ""
echo "📁 检查必要文件..."

if [ ! -f "app.py" ]; then
    echo "  ❌ app.py (未找到)"
    exit 1
else
    echo "  ✅ app.py"
fi

if [ ! -f "best_model.pth" ]; then
    echo "  ⚠️  best_model.pth (未找到，将先训练模型)"
    echo "  运行命令: python train.py"
    read -p "按 Enter 键继续，或按 Ctrl+C 退出..."
    python train.py
    echo ""
    echo "训练完成后再次运行此脚本启动 Web 界面"
    exit 0
else
    echo "  ✅ best_model.pth"
fi

# 启动 Streamlit 应用
echo ""
echo "🚀 启动 Streamlit Web 应用..."
echo "============================================"
echo ""

streamlit run app.py

# 启动失败时的提示
echo ""
echo "============================================"
echo "💡 提示："
echo "1. Web 界面将在浏览器中自动打开"
echo "2. 默认访问地址：http://localhost:8501"
echo "3. 如需停止服务，在终端按 Ctrl+C"
echo "4. 如需重新启动，再次运行此脚本"
echo "============================================"
