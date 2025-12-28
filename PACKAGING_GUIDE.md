# 📦 工业零件表面缺陷检测系统 - 应用打包指南

## 📋 目录

1. [打包概述](#打包概述)
2. [准备工作](#准备工作)
3. [打包步骤](#打包步骤)
4. [使用打包后的应用](#使用打包后的应用)
5. [常见问题](#常见问题)
6. [高级配置](#高级配置)

---

## 打包概述

本项目使用 **PyInstaller** 将 Streamlit Web 应用打包成独立的 macOS 可执行文件。打包后的应用可以直接双击运行，无需安装 Python 环境或依赖包。

### 优势

- ✅ **独立运行**：无需安装 Python 和依赖包
- ✅ **一键启动**：双击即可运行应用
- ✅ **自动打开浏览器**：启动后自动在浏览器中打开应用
- ✅ **便携性好**：可以复制到其他 Mac 上使用

### 文件说明

| 文件 | 说明 |
|------|------|
| [`launcher.py`](launcher.py:1) | 应用启动器，负责启动 Streamlit 服务 |
| [`defect_detection.spec`](defect_detection.spec:1) | PyInstaller 打包配置文件 |
| [`build_app.sh`](build_app.sh:1) | 一键打包脚本 |

---

## 准备工作

### 1. 环境要求

- **操作系统**：macOS 10.15 或更高版本
- **Python**：3.9 或更高版本
- **内存**：建议 8GB 或更高
- **磁盘空间**：至少 2GB 可用空间

### 2. 安装依赖

```bash
# 激活 conda 环境
conda activate uu

# 安装 PyInstaller
pip install pyinstaller
```

### 3. 检查必要文件

确保以下文件存在于项目根目录：

- ✅ `app.py` - Streamlit 应用主文件
- ✅ `best_model.pth` - 训练好的模型文件
- ✅ `launcher.py` - 应用启动器
- ✅ `defect_detection.spec` - 打包配置文件

---

## 打包步骤

### 方式一：使用一键打包脚本（推荐）

```bash
# 激活 conda 环境
conda activate uu

# 运行打包脚本
./build_app.sh
```

打包脚本会自动完成以下操作：
1. 检查 conda 环境
2. 检查必要文件
3. 安装 PyInstaller（如果未安装）
4. 清理旧的构建文件
5. 执行打包
6. 显示打包结果

### 方式二：手动打包

```bash
# 1. 激活 conda 环境
conda activate uu

# 2. 清理旧的构建文件
rm -rf build/ dist/

# 3. 执行打包
pyinstaller defect_detection.spec
```

### 打包过程说明

打包过程可能需要 **5-15 分钟**，具体时间取决于您的 Mac 性能。打包过程包括：

1. **分析依赖**：PyInstaller 分析 Python 代码及其依赖
2. **收集文件**：收集所有需要的 Python 模块和数据文件
3. **打包资源**：将模型文件和应用代码打包到可执行文件中
4. **生成应用**：生成独立的可执行文件

---

## 使用打包后的应用

### 运行应用

打包成功后，可执行文件位于 `dist/` 目录：

```bash
# 进入 dist 目录
cd dist

# 运行应用
./工业零件表面缺陷检测
```

或者直接在 Finder 中双击 `工业零件表面缺陷检测` 文件。

### 应用启动流程

1. 应用启动后，会显示控制台窗口
2. 等待 3-5 秒，Streamlit 服务启动
3. 浏览器自动打开 `http://localhost:8501`
4. 开始使用应用进行缺陷检测

### 停止应用

在控制台窗口按 `Ctrl+C` 或直接关闭控制台窗口即可停止应用。

---

## 常见问题

### Q1: 打包失败，提示找不到模块

**解决方案**：在 `defect_detection.spec` 文件的 `hiddenimports` 列表中添加缺失的模块。

```python
hiddenimports = [
    # ... 其他模块
    '缺失的模块名',
]
```

### Q2: 打包后的应用无法启动

**可能原因**：
1. 模型文件未正确打包
2. Python 版本不兼容
3. 依赖包未正确安装

**解决方案**：
1. 检查 `best_model.pth` 是否在项目根目录
2. 确保使用与训练时相同的 Python 版本
3. 重新安装依赖包：`pip install -r requirements.txt`

### Q3: 应用启动后浏览器没有自动打开

**解决方案**：手动在浏览器中访问 `http://localhost:8501`

### Q4: 打包后的应用文件很大（>500MB）

**这是正常的**。PyInstaller 会将所有 Python 依赖打包到可执行文件中，包括：
- PyTorch（约 200MB）
- Torchvision（约 100MB）
- NumPy、Matplotlib 等科学计算库
- Streamlit 及其依赖

### Q5: 如何减小应用体积？

**方法**：
1. 使用 `--exclude-module` 排除不需要的模块
2. 使用 UPX 压缩（已在配置中启用）
3. 考虑使用虚拟环境仅安装必要的依赖

---

## 高级配置

### 添加应用图标

1. 准备一个 `.icns` 格式的图标文件
2. 将图标文件放在项目根目录，命名为 `app_icon.icns`
3. 修改 `defect_detection.spec` 文件：

```python
exe = EXE(
    # ... 其他参数
    icon='app_icon.icns',  # 添加图标
)
```

### 隐藏控制台窗口

如果不想显示控制台窗口，修改 `defect_detection.spec`：

```python
exe = EXE(
    # ... 其他参数
    console=False,  # 改为 False
)
```

**注意**：隐藏控制台后，将无法看到应用输出信息，调试会比较困难。

### 创建 macOS .app 包

如果需要创建标准的 macOS 应用包（`.app`），可以使用以下命令：

```bash
# 创建 .app 包
pyinstaller --onefile --windowed --name "工业零件表面缺陷检测" \
    --icon=app_icon.icns \
    --add-data "app.py:." \
    --add-data "best_model.pth:." \
    --hidden-import streamlit \
    --hidden-import PIL \
    launcher.py
```

### 分发给其他 Mac 用户

打包后的应用可以直接复制到其他 Mac 上使用，但需要注意：

1. **系统版本**：目标 Mac 的 macOS 版本不能低于打包时的版本
2. **架构兼容**：确保目标 Mac 的 CPU 架构与打包时一致（Intel 或 Apple Silicon）
3. **权限问题**：首次运行可能需要授予终端访问权限

---

## 技术细节

### PyInstaller 工作原理

PyInstaller 通过以下步骤打包应用：

1. **静态分析**：分析 Python 代码，找出所有导入的模块
2. **收集依赖**：收集所有需要的 Python 模块和数据文件
3. **创建引导程序**：创建一个引导程序，用于解压和运行应用
4. **打包资源**：将所有资源打包到单个可执行文件中

### Streamlit 打包挑战

Streamlit 是一个 Web 框架，打包时需要特别注意：

1. **隐藏导入**：Streamlit 使用动态导入，需要手动指定隐藏导入
2. **资源文件**：确保 `app.py` 和 `best_model.pth` 正确打包
3. **端口配置**：使用固定的端口（8501）避免冲突

### 打包配置说明

`defect_detection.spec` 文件的关键配置：

```python
# 数据文件
datas = [
    ('app.py', '.'),           # Streamlit 应用
    ('best_model.pth', '.'),   # 模型文件
]

# 隐藏导入（Streamlit 相关）
hiddenimports = [
    'streamlit',
    'streamlit.cli',
    'streamlit.runtime',
    # ... 更多隐藏导入
]
```

---

## 总结

使用 PyInstaller 打包后的应用具有以下特点：

| 特性 | 说明 |
|------|------|
| **独立性** | 无需安装 Python 环境 |
| **便携性** | 可复制到其他 Mac 使用 |
| **易用性** | 双击即可运行 |
| **兼容性** | 支持主流 macOS 版本 |
| **体积** | 约 500MB-1GB |

打包完成后，您可以将 `dist/工业零件表面缺陷检测` 文件复制到任何位置或分享给其他 Mac 用户使用。

---

## 相关文档

- [PyInstaller 官方文档](https://pyinstaller.org/)
- [Streamlit 官方文档](https://docs.streamlit.io/)
- [项目 README](README.md)
