@echo off
REM ============================================
REM 基于 ResNet 的工业零件表面缺陷检测系统 - Windows 启动脚本
REM ============================================

chcp 65001 >nul
echo 🏭 基于 ResNet 的工业零件表面缺陷检测系统
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

REM 检查 Python 版本
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 🐍 Python 版本: %PYTHON_VERSION%

REM 检查是否安装了必要的包
echo.
echo 📋 检查依赖包...

python -c "import torch" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ torch
) else (
    echo   ❌ torch ^(未安装^)
)

python -c "import torchvision" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ torchvision
) else (
    echo   ❌ torchvision ^(未安装^)
)

python -c "import matplotlib" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ matplotlib
) else (
    echo   ❌ matplotlib ^(未安装^)
)

python -c "import streamlit" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ streamlit
) else (
    echo   ❌ streamlit ^(未安装^)
)

python -c "from PIL import Image" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ PIL
) else (
    echo   ❌ PIL ^(未安装^)
)

REM 检查必要文件是否存在
echo.
echo 📁 检查必要文件...

if not exist "app.py" (
    echo   ❌ app.py ^(未找到^)
    pause
    exit /b 1
) else (
    echo   ✅ app.py
)

if not exist "best_model.pth" (
    echo   ⚠️  best_model.pth ^(未找到，将先训练模型^)
    echo   运行命令: python train.py
    pause
    python train.py
    echo.
    echo 训练完成后再次运行此脚本启动 Web 界面
    pause
    exit /b 0
) else (
    echo   ✅ best_model.pth
)

REM 启动 Streamlit 应用
echo.
echo 🚀 启动 Streamlit Web 应用...
echo ============================================
echo.

streamlit run app.py

REM 启动失败时的提示
echo.
echo ============================================
echo 💡 提示：
echo 1. Web 界面将在浏览器中自动打开
echo 2. 默认访问地址：http://localhost:8501
echo 3. 如需停止服务，在终端按 Ctrl+C
echo 4. 如需重新启动，再次运行此脚本
echo ============================================
pause
