#!/bin/bash
# ============================================
# 工业零件表面缺陷检测系统 - macOS 应用打包脚本
# ============================================

echo "🏭 工业零件表面缺陷检测系统 - 应用打包"
echo "============================================"
echo ""

# 检查是否在 conda 环境中
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo "⚠️  警告：未检测到 conda 环境"
    echo "请先激活 conda 环境：conda activate uu"
    echo ""
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查必要文件
echo "📁 检查必要文件..."

if [ ! -f "app.py" ]; then
    echo "❌ 错误：未找到 app.py"
    exit 1
fi

if [ ! -f "best_model.pth" ]; then
    echo "❌ 错误：未找到 best_model.pth"
    echo "请先运行训练脚本：python train.py"
    exit 1
fi

if [ ! -f "launcher.py" ]; then
    echo "❌ 错误：未找到 launcher.py"
    exit 1
fi

echo "✅ 所有必要文件检查完成"
echo ""

# 检查 PyInstaller
echo "📦 检查 PyInstaller..."

if ! command -v pyinstaller &> /dev/null; then
    echo "📥 安装 PyInstaller..."
    pip install pyinstaller
fi

echo "✅ PyInstaller 已就绪"
echo ""

# 清理旧的构建文件
echo "🧹 清理旧的构建文件..."
rm -rf build/
rm -rf dist/
echo "✅ 清理完成"
echo ""

# 开始打包
echo "🔨 开始打包应用..."
echo "这可能需要几分钟时间，请耐心等待..."
echo ""

pyinstaller defect_detection.spec

# 检查打包结果
if [ -f "dist/工业零件表面缺陷检测" ]; then
    echo ""
    echo "============================================"
    echo "✅ 打包成功！"
    echo ""
    echo "📦 应用位置：dist/工业零件表面缺陷检测"
    echo ""
    echo "💡 使用方法："
    echo "   1. 进入 dist 目录：cd dist"
    echo "   2. 运行应用：./工业零件表面缺陷检测"
    echo ""
    echo "📝 或者直接双击运行可执行文件"
    echo "============================================"
else
    echo ""
    echo "============================================"
    echo "❌ 打包失败！"
    echo "请检查错误信息并重试"
    echo "============================================"
    exit 1
fi
