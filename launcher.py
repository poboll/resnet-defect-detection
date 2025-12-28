#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工业零件表面缺陷检测系统 - 应用启动器
"""

import os
import sys
import subprocess
import webbrowser
import time
import socket

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def is_port_in_use(port):
    """检查端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def wait_for_server(port, timeout=30):
    """等待服务器启动"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(port):
            return True
        time.sleep(0.5)
    return False

def main():
    print("=" * 50)
    print("🏭 工业零件表面缺陷检测系统")
    print("=" * 50)
    print()
    
    # 检查文件
    app_path = get_resource_path("app.py")
    model_path = get_resource_path("best_model.pth")
    
    print(f"📁 应用路径: {app_path}")
    print(f"📁 模型路径: {model_path}")
    print()
    
    if not os.path.exists(app_path):
        print(f"❌ 错误: 未找到 app.py")
        input("按 Enter 键退出...")
        return
    
    if not os.path.exists(model_path):
        print(f"❌ 错误: 未找到 best_model.pth")
        input("按 Enter 键退出...")
        return
    
    # 设置工作目录
    os.chdir(os.path.dirname(app_path))
    
    # 设置环境变量
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    print("🚀 正在启动 Streamlit 服务...")
    print()
    
    try:
        # 启动 Streamlit
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", app_path,
             "--server.headless=true",
             "--server.port=8501",
             "--browser.gatherUsageStats=false"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # 等待服务器启动
        print("⏳ 等待服务器启动...")
        if wait_for_server(8501, timeout=30):
            print()
            print("✅ 服务已启动!")
            print("🌐 请在浏览器中访问: http://localhost:8501")
            print()
            print("💡 提示: 按 Ctrl+C 或关闭此窗口停止服务")
            print("=" * 50)
            print()
            
            # 只打开一次浏览器
            webbrowser.open("http://localhost:8501")
        else:
            print("⚠️ 服务启动超时，请手动访问 http://localhost:8501")
        
        # 显示输出
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                print(line, end='', flush=True)
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 正在停止服务...")
        process.terminate()
        process.wait()
        print("✅ 服务已停止")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n按 Enter 键退出...")

if __name__ == "__main__":
    main()
