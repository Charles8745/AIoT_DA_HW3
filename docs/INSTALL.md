# Installation Guide

## Quick Start (推薦)

### 線上體驗（無需安裝）
```bash
https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/
```

---

## 本地運行

### 1. 系統需求
- Python 3.8+
- 2GB RAM (推薦 4GB+)

### 2. 克隆或下載
```bash
git clone https://github.com/Charles8745/AIoT_DA_HW3.git
cd AIoT_DA_HW3
```

### 3. 建立虛擬環境
```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. 安裝依賴
```bash
pip install -r config/requirements.txt
```

### 5. 運行應用
```bash
streamlit run app/streamlit_app.py
```

打開瀏覽器訪問 `http://localhost:8501`

---

## 故障排查

**問題：Module not found**
```bash
# 重新安裝依賴
pip install --upgrade -r config/requirements.txt
```

**問題：Port 8501 已被佔用**
```bash
streamlit run app/streamlit_app.py --server.port 8502
```

**問題：清除快取**
```bash
streamlit cache clear
```
