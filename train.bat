@echo off
REM ============================================
REM 基于 ResNet 的工业零件表面缺陷检测系统 - Windows 训练脚本
REM ============================================

chcp 65001 >nul
echo 🏭 基于 ResNet 的工业零件表面缺陷检测系统 - 模型训练
echo ============================================
echo.

REM 检查 conda 是否存在
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 错误：未找到 conda 环境
    echo 请先安装 Miniconda 或 Anaconda
    echo 下载地址：https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

REM 设置 conda 环境名称
set ENV_NAME=uu

REM 检查 conda 环境是否存在
conda env list | findstr /C:"%ENV_NAME%" >nul
if %errorlevel% neq 0 (
    echo 📦 创建 conda 环境: %ENV_NAME%
    conda create -n %ENV_NAME% python=3.9 -y
    echo ✅ 环境创建完成
) else (
    echo ✅ conda 环境 %ENV_NAME% 已存在
)

REM 激活 conda 环境
echo 🔄 激活 conda 环境: %ENV_NAME%
call conda activate %ENV_NAME%

REM 检查是否安装了必要的包
echo.
echo 📋 检查依赖包...

python -c "import torch" 2>nul
if %errorlevel% neq 0 (
    echo 📦 安装依赖包...
    pip install -r requirements.txt
)

REM 检查数据集
echo.
echo 📁 检查数据集...

if not exist "data\train\images" (
    echo ❌ 错误：未找到训练数据集
    echo 请确保 data\train\images 目录存在且包含按类别分类的图片
    pause
    exit /b 1
)

if not exist "data\validation\images" (
    echo ❌ 错误：未找到验证数据集
    echo 请确保 data\validation\images 目录存在且包含按类别分类的图片
    pause
    exit /b 1
)

echo ✅ 数据集检查完成

REM 开始训练
echo.
echo 🚀 开始训练模型...
echo ============================================
echo.

python train.py

echo.
echo ============================================
echo ✅ 训练完成！
echo 📊 训练曲线已保存为: training_curve.png
echo 💾 最佳模型已保存为: best_model.pth
echo.
echo 💡 接下来可以运行以下命令启动 Web 演示界面：
echo    Windows: run.bat
echo    Mac/Linux: ./run.sh
echo ============================================
pause
