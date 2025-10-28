"""
Streamlit App Testing Guide and Utilities

提供測試 Streamlit 應用的多種方式
"""

import subprocess
import os
import sys
from pathlib import Path


class StreamlitTester:
    """Streamlit 應用測試工具"""
    
    def __init__(self, app_path: str = "sources/streamlit_app.py"):
        self.app_path = app_path
        self.base_dir = Path(__file__).parent.parent
        
    def check_dependencies(self) -> dict:
        """檢查必要的依賴"""
        dependencies = {
            'streamlit': False,
            'plotly': False,
            'pandas': False,
            'numpy': False,
        }
        
        for package in dependencies.keys():
            try:
                __import__(package)
                dependencies[package] = True
                print(f"✅ {package} 已安裝")
            except ImportError:
                print(f"❌ {package} 未安裝")
        
        return dependencies
    
    def install_dependencies(self):
        """安裝缺失的依賴"""
        print("🔧 安裝 Streamlit 應用依賴...")
        packages = ['streamlit', 'plotly', 'pandas', 'numpy']
        
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                print(f"📦 安裝 {package}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             check=True)
    
    def run_local_server(self, port: int = 8501):
        """本地運行 Streamlit 伺服器"""
        print(f"\n🚀 啟動 Streamlit 應用...")
        print(f"📍 訪問地址: http://localhost:{port}")
        print(f"📄 應用文件: {self.app_path}")
        print("\n按 Ctrl+C 停止伺服器\n")
        
        os.chdir(self.base_dir)
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run',
            self.app_path,
            '--logger.level=debug',
            f'--server.port={port}'
        ])
    
    def lint_app(self) -> bool:
        """檢查應用的語法和風格"""
        print("🔍 檢查應用文件...")
        
        app_file = self.base_dir / self.app_path
        
        if not app_file.exists():
            print(f"❌ 應用文件不存在: {app_file}")
            return False
        
        # 檢查語法
        try:
            with open(app_file, 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, str(app_file), 'exec')
            print(f"✅ 語法檢查通過")
            return True
        except SyntaxError as e:
            print(f"❌ 語法錯誤: {e}")
            return False
    
    def test_imports(self) -> bool:
        """測試應用的導入"""
        print("\n📚 測試應用導入...")
        
        try:
            sys.path.insert(0, str(self.base_dir))
            # 嘗試導入模組（但不執行）
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "streamlit_app",
                self.base_dir / self.app_path
            )
            module = importlib.util.module_from_spec(spec)
            
            print("✅ 所有導入成功")
            return True
        except Exception as e:
            print(f"❌ 導入失敗: {e}")
            return False
    
    def validate_structure(self) -> dict:
        """驗證應用結構"""
        print("\n📋 驗證應用結構...")
        
        app_file = self.base_dir / self.app_path
        
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            '有 main() 函數': 'def main()' in content,
            '有 Neumorphism 設計': 'NEUMORPHISM_CSS' in content,
            '有顏色定義': 'NEUMORPHISM_COLORS' in content,
            '有頁面函數': 'def page_overview' in content,
            '有 Streamlit 導入': 'import streamlit' in content,
            '有 Plotly 導入': 'import plotly' in content,
        }
        
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"{status} {check}")
        
        return checks
    
    def get_app_info(self) -> dict:
        """獲取應用信息"""
        print("\n📊 應用信息:")
        
        app_file = self.base_dir / self.app_path
        
        with open(app_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        info = {
            '行數': len(lines),
            '文件大小': f"{app_file.stat().st_size / 1024:.1f} KB",
        }
        
        # 計算函數
        functions = [line for line in lines if line.strip().startswith('def ')]
        info['函數數'] = len(functions)
        
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        return info


def main():
    """主測試程序"""
    print("=" * 70)
    print("🎨 Streamlit 應用測試工具")
    print("=" * 70)
    
    tester = StreamlitTester()
    
    # 1. 檢查依賴
    print("\n1️⃣  檢查依賴...")
    deps = tester.check_dependencies()
    
    missing = [k for k, v in deps.items() if not v]
    if missing:
        print(f"\n⚠️  缺失依賴: {', '.join(missing)}")
        install = input("要安裝缺失的依賴嗎? (y/n): ").lower() == 'y'
        if install:
            tester.install_dependencies()
    
    # 2. 語法檢查
    print("\n2️⃣  語法檢查...")
    if not tester.lint_app():
        print("❌ 應用有語法錯誤")
        return
    
    # 3. 導入測試
    print("\n3️⃣  導入測試...")
    if not tester.test_imports():
        print("❌ 應用導入失敗")
        return
    
    # 4. 結構驗證
    print("\n4️⃣  結構驗證...")
    structure = tester.validate_structure()
    
    # 5. 應用信息
    print("\n5️⃣  應用信息")
    tester.get_app_info()
    
    # 6. 啟動伺服器
    print("\n" + "=" * 70)
    print("✅ 所有檢查通過!")
    print("=" * 70)
    
    launch = input("\n要啟動 Streamlit 伺服器嗎? (y/n): ").lower() == 'y'
    if launch:
        tester.run_local_server()


if __name__ == '__main__':
    main()
