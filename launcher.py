#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工业零件表面缺陷检测系统 - 应用启动器
用于打包成独立应用程序
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

# 获取应用资源目录（用于打包后查找资源）
def get_resource_path(relative_path):
    """获取资源文件的绝对路径（支持打包后的应用）"""
    try:
        # PyInstaller 创建的临时文件夹
        base_path = sys._MEIPASS
    except AttributeError:
        # 正常运行模式
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_model_file():
    """检查模型文件是否存在"""
    model_path = get_resource_path("best_model.pth")
    if not os.path.exists(model_path):
        print("❌ 错误：未找到模型文件 best_model.pth")
        print("请确保模型文件已训练并放置在正确位置")
        return False
    return True

def start_streamlit():
    """启动 Streamlit 应用"""
    try:
        # 检查模型文件
        if not check_model_file():
            print("\n按任意键退出...")
            input()
            sys.exit(1)
        
        # 获取 app.py 的路径
        app_path = get_resource_path("app.py")
        
        if not os.path.exists(app_path):
            print(f"❌ 错误：未找到 app.py 文件")
            print(f"   路径：{app_path}")
            print("\n按任意键退出...")
            input()
            sys.exit(1)
        
        # 设置 Streamlit 配置
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'false'
        os.environ['STREAMLIT_SERVER_PORT'] = '8501'
        os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
        
        print("🏭 工业零件表面缺陷检测系统")
        print("=" * 50)
        print("正在启动应用...")
        print()
        
        # 启动 Streamlit
        # 使用 subprocess 启动 streamlit
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", app_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # 等待 Streamlit 启动
        print("⏳ 正在等待 Streamlit 服务启动...")
        time.sleep(3)
        
        # 自动打开浏览器
        try:
            webbrowser.open("http://localhost:8501")
        except:
            pass
        
        print("✅ 应用已启动！")
        print("🌐 访问地址：http://localhost:8501")
        print()
        print("💡 提示：关闭此窗口将停止应用")
        print("=" * 50)
        print()
        
        # 持续读取输出
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print(line, end='', flush=True)
        
        # 等待进程结束
        process.wait()
            
    except KeyboardInterrupt:
        print("\n\n⏹️  应用已停止")
        try:
            process.terminate()
        except:
            pass
    except Exception as e:
        print(f"\n❌ 启动失败：{e}")
        import traceback
        traceback.print_exc()
        print("\n按任意键退出...")
        input()

if __name__ == "__main__":
    start_streamlit()
