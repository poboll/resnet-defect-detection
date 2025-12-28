# 🚀 GitHub Actions 自动构建指南

## 📋 目录

1. [概述](#概述)
2. [自动构建配置](#自动构建配置)
3. [使用方法](#使用方法)
4. [下载构建产物](#下载构建产物)
5. [手动触发构建](#手动触发构建)
6. [版本发布](#版本发布)
7. [常见问题](#常见问题)

---

## 概述

本项目使用 **GitHub Actions** 实现了跨平台自动构建，可以自动生成 Windows、macOS 和 Linux 三个平台的可执行文件。

### 支持的平台

| 平台 | 可执行文件名 | 文件扩展名 |
|------|-------------|-----------|
| Windows | `工业零件表面缺陷检测.exe` | `.exe` |
| macOS | `工业零件表面缺陷检测` | 无 |
| Linux | `工业零件表面缺陷检测` | 无 |

### 触发条件

自动构建会在以下情况下触发：

- ✅ 推送代码到 `main` 或 `master` 分支
- ✅ 创建 Pull Request 到 `main` 或 `master` 分支
- ✅ 推送标签（如 `v1.0.0`）
- ✅ 手动触发（通过 GitHub 网页界面）

---

## 自动构建配置

### 工作流文件

GitHub Actions 配置文件位于：[`.github/workflows/build.yml`](.github/workflows/build.yml:1)

### 工作流程

```
触发构建 → 并行构建三平台 → 上传构建产物 → (可选) 创建发布版本
```

### 构建矩阵

| 操作系统 | GitHub Runner | Python 版本 |
|---------|---------------|-------------|
| Windows | `windows-latest` | 3.9 |
| macOS | `macos-latest` | 3.9 |
| Linux | `ubuntu-latest` | 3.9 |

---

## 使用方法

### 步骤 1：推送到 GitHub

```bash
# 初始化 Git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: 工业零件表面缺陷检测系统"

# 添加远程仓库（替换为您的仓库地址）
git remote add origin https://github.com/yourusername/resnet-defect-detection.git

# 推送到 GitHub
git push -u origin main
```

### 步骤 2：查看构建状态

1. 访问您的 GitHub 仓库
2. 点击 **Actions** 标签页
3. 查看最新的工作流运行状态

### 步骤 3：等待构建完成

构建过程大约需要 **10-20 分钟**，具体时间取决于：

- 网络速度（下载依赖）
- GitHub Runner 性能
- PyInstaller 打包时间

---

## 下载构建产物

### 方式一：从 Actions 页面下载

1. 访问仓库的 **Actions** 页面
2. 点击最近一次成功的工作流运行
3. 滚动到页面底部的 **Artifacts** 部分
4. 下载对应平台的构建产物：
   - `defect-detection-windows` - Windows 版本
   - `defect-detection-macos` - macOS 版本
   - `defect-detection-linux` - Linux 版本

### 方式二：从 Release 页面下载（推荐）

如果您创建了版本标签，可以从 Release 页面下载：

1. 访问仓库的 **Releases** 页面
2. 选择对应的版本
3. 下载对应平台的可执行文件

### 下载后的文件结构

```
defect-detection-windows/
└── 工业零件表面缺陷检测.exe    # Windows 可执行文件

defect-detection-macos/
└── 工业零件表面缺陷检测         # macOS 可执行文件

defect-detection-linux/
└── 工业零件表面缺陷检测         # Linux 可执行文件
```

---

## 手动触发构建

如果您不想推送代码，可以手动触发构建：

1. 访问仓库的 **Actions** 页面
2. 在左侧选择 **Build Multi-Platform Executables** 工作流
3. 点击右侧的 **Run workflow** 按钮
4. 选择分支（通常是 `main`）
5. 点击绿色的 **Run workflow** 按钮

---

## 版本发布

### 创建版本标签

```bash
# 创建并推送标签（例如 v1.0.0）
git tag v1.0.0
git push origin v1.0.0
```

### 自动创建 Release

推送标签后，GitHub Actions 会自动：

1. 构建三个平台的可执行文件
2. 创建一个新的 Release
3. 将可执行文件上传到 Release
4. 自动生成 Release Notes

### 访问 Release

1. 访问仓库的 **Releases** 页面
2. 选择对应的版本
3. 下载对应平台的可执行文件

### 版本号规范

建议使用语义化版本号（Semantic Versioning）：

- `v1.0.0` - 首次正式发布
- `v1.1.0` - 新增功能
- `v1.0.1` - Bug 修复
- `v2.0.0` - 重大更新

---

## 常见问题

### Q1: 构建失败怎么办？

**可能原因**：

1. **代码错误**：检查 Python 代码是否有语法错误
2. **依赖问题**：确保 `requirements.txt` 中的所有包都能正常安装
3. **文件缺失**：确保 `best_model.pth` 和 `app.py` 存在

**解决方案**：

1. 查看 Actions 页面的错误日志
2. 在本地测试构建：`pyinstaller launcher.py`
3. 修复问题后重新推送代码

### Q2: 构建时间太长？

**这是正常的**。首次构建需要：

- 下载 Python 环境
- 安装所有依赖包（PyTorch、Streamlit 等）
- PyInstaller 打包

后续构建会使用缓存，速度会快一些。

### Q3: 下载的可执行文件无法运行？

**可能原因**：

1. **平台不匹配**：确保下载了对应平台的文件
2. **权限问题**（Linux/macOS）：
   ```bash
   chmod +x 工业零件表面缺陷检测
   ```
3. **安全软件拦截**：Windows 可能会拦截未签名的可执行文件

**解决方案**：

1. 确认下载了正确的平台版本
2. 给文件添加执行权限（Linux/macOS）
3. 在安全软件中添加信任

### Q4: 如何修改构建配置？

编辑 [`.github/workflows/build.yml`](.github/workflows/build.yml:1) 文件：

```yaml
# 修改 Python 版本
python-version: '3.9'

# 添加更多 PyInstaller 选项
--onefile --windowed --name "工业零件表面缺陷检测"

# 添加更多隐藏导入
--hidden-import streamlit
--hidden-import your_module
```

修改后推送代码，新的配置会自动生效。

### Q5: 可以构建其他架构吗？

可以！修改 `.github/workflows/build.yml` 文件，添加更多矩阵：

```yaml
strategy:
  matrix:
    os: [windows-latest, macos-latest, macos-13, ubuntu-latest]
    include:
      - os: macos-13  # Intel Mac
        platform: macos-intel
```

### Q6: 如何减小可执行文件体积？

**方法**：

1. 使用虚拟环境，只安装必要的依赖
2. 在 PyInstaller 配置中排除不需要的模块：
   ```yaml
   --exclude-module matplotlib
   --exclude-module scipy
   ```
3. 使用 UPX 压缩（已在配置中启用）

---

## 高级配置

### 添加应用图标

1. 准备图标文件：
   - Windows: `.ico` 文件
   - macOS: `.icns` 文件
   - Linux: `.png` 文件

2. 将图标文件添加到仓库

3. 修改 `.github/workflows/build.yml`：

```yaml
# Windows
--icon=app_icon.ico

# macOS
--icon=app_icon.icns

# Linux
--icon=app_icon.png
```

### 隐藏控制台窗口（Windows）

修改 `.github/workflows/build.yml`：

```yaml
pyinstaller --onefile --windowed --name "工业零件表面缺陷检测" \
  # ... 其他选项
```

**注意**：隐藏控制台后，将无法看到应用输出信息。

### 自动化测试

在构建前添加测试步骤：

```yaml
- name: Run tests
  run: |
    python -m pytest tests/
```

### 代码签名（macOS/Windows）

需要配置相应的签名证书：

```yaml
- name: Sign macOS binary
  if: matrix.os == 'macos-latest'
  run: |
    codesign --sign "${{ secrets.APPLE_CERT }}" dist/工业零件表面缺陷检测
```

---

## 总结

使用 GitHub Actions 自动构建的优势：

| 特性 | 说明 |
|------|------|
| **自动化** | 推送代码自动构建，无需手动操作 |
| **跨平台** | 一次配置，三端自动构建 |
| **版本管理** | 自动创建 Release，方便版本管理 |
| **免费** | GitHub Actions 公开仓库免费使用 |
| **可靠性** | 使用 GitHub 官方 Runner，稳定可靠 |

---

## 相关文档

- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [PyInstaller 官方文档](https://pyinstaller.org/)
- [项目 README](README.md)
- [应用打包指南](PACKAGING_GUIDE.md)
