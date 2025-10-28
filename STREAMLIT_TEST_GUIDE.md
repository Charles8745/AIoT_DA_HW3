# 🎨 Streamlit 應用測試指南

## 📋 目錄

1. [快速開始](#快速開始)
2. [方法一：自動測試工具](#方法一自動測試工具)
3. [方法二：直接運行](#方法二直接運行)
4. [方法三：互動式測試](#方法三互動式測試)
5. [測試檢查清單](#測試檢查清單)
6. [常見問題](#常見問題)
7. [故障排除](#故障排除)

---

## 快速開始

### 最簡單的方式：直接運行

```bash
cd /Users/charles88/Desktop/AIoT/AIoT_DA_HW3
streamlit run sources/streamlit_app.py
```

**預期結果:**
- 瀏覽器自動打開 `http://localhost:8501`
- 看到 6 個頁面選項
- 體驗 Neumorphism UI 設計

---

## 方法一：自動測試工具 ⭐ 推薦

### 執行測試工具

```bash
cd /Users/charles88/Desktop/AIoT/AIoT_DA_HW3
python test_streamlit.py
```

### 工具會進行的檢查

1. ✅ **依賴檢查** - 驗證 streamlit, plotly, pandas 等
2. ✅ **語法檢查** - 檢查 Python 文件語法
3. ✅ **導入測試** - 驗證所有模組導入
4. ✅ **結構驗證** - 確認所有必要組件存在
5. ✅ **應用信息** - 顯示統計數據
6. 🚀 **啟動伺服器** - 可選的自動啟動

### 示例輸出

```
======================================================================
🎨 Streamlit 應用測試工具
======================================================================

1️⃣  檢查依賴...
✅ streamlit 已安裝
✅ plotly 已安裝
✅ pandas 已安裝
✅ numpy 已安裝

2️⃣  語法檢查...
✅ 語法檢查通過

3️⃣  導入測試...
✅ 所有導入成功

4️⃣  結構驗證...
✅ 有 main() 函數
✅ 有 Neumorphism 設計
✅ 有顏色定義
✅ 有頁面函數
✅ 有 Streamlit 導入
✅ 有 Plotly 導入

5️⃣  應用信息
  行數: 684
  文件大小: 21.5 KB
  函數數: 6

======================================================================
✅ 所有檢查通過!
======================================================================

要啟動 Streamlit 伺服器嗎? (y/n):
```

---

## 方法二：直接運行

### 安裝依賴

```bash
# 安裝 Streamlit 和相關包
pip install streamlit plotly pandas numpy

# 或安裝完整依賴
pip install streamlit plotly pandas numpy nltk textblob rich
```

### 運行應用

```bash
cd /Users/charles88/Desktop/AIoT/AIoT_DA_HW3
streamlit run sources/streamlit_app.py
```

### 運行選項

```bash
# 基本運行
streamlit run sources/streamlit_app.py

# 指定端口
streamlit run sources/streamlit_app.py --server.port 8502

# 調試模式
streamlit run sources/streamlit_app.py --logger.level=debug

# 禁用檔案監視（開發中修改不會自動重載）
streamlit run sources/streamlit_app.py --client.showErrorDetails=true
```

---

## 方法三：互動式測試

### Python REPL 測試

```python
# 1. 導入必要模組
import sys
from pathlib import Path
sys.path.insert(0, '/Users/charles88/Desktop/AIoT/AIoT_DA_HW3')

# 2. 測試導入
from sources import streamlit_app as app

# 3. 檢查設計系統
print("✅ Neumorphism 顏色:")
for color, value in app.NEUMORPHISM_COLORS.items():
    print(f"  {color}: {value}")

# 4. 檢查頁面
print("\n✅ 頁面函數:")
pages = [m for m in dir(app) if m.startswith('page_')]
for page in pages:
    print(f"  - {page}()")

# 5. 檢查 CSS
print(f"\n✅ CSS 組件數: {app.NEUMORPHISM_CSS.count('.')}")
```

### 運行測試

```bash
cd /Users/charles88/Desktop/AIoT/AIoT_DA_HW3
python -c "
import sys
sys.path.insert(0, '.')
from sources import streamlit_app as app

print('✅ Streamlit app 成功導入')
print(f'✅ 頁面函數: {len([m for m in dir(app) if m.startswith(\"page_\")])}')
print(f'✅ Neumorphism 顏色定義: {len(app.NEUMORPHISM_COLORS)}')
"
```

---

## 測試檢查清單

### 基本功能測試

在瀏覽器中測試以下功能：

#### 📊 Overview 頁面
- [ ] 模型摘要卡片顯示 4 個指標
- [ ] 模型比較表格顯示所有模型
- [ ] 指標卡片使用正確的 Neumorphism 樣式
- [ ] 可以選擇不同的模型

#### 📈 Metrics Explorer 頁面
- [ ] 下拉菜單能選擇不同模型
- [ ] 顯示 Accuracy、Precision、Recall、F1、AUC
- [ ] 如果有訓練歷史，顯示損失曲線

#### ⚖️ Model Comparison 頁面
- [ ] 顯示雷達圖比較
- [ ] 比較表格正確顯示所有模型的指標
- [ ] 雷達圖有 5 個軸（各個指標）

#### 🎮 Live Inference 頁面
- [ ] 文本輸入區域可用
- [ ] 預測按鈕可點擊
- [ ] 結果卡片顯示預測、信心分數、分數
- [ ] 參數滑塊（信心閾值、批次大小）可調整
- [ ] 推理歷史記錄可展開/收起

#### 🎯 Feature Importance 頁面
- [ ] 顯示特徵重要性條形圖
- [ ] 可調整 Top N features
- [ ] 圖表正確排序

#### 📋 Data Overview 頁面
- [ ] 顯示 4 個指標卡片（樣本數、特徵、類別、缺失數據）
- [ ] 顯示類別分佈圓餅圖
- [ ] 圖表正確使用顏色

### Neumorphism UI 測試

- [ ] 卡片有柔和陰影效果
- [ ] 按鈕懸停時有深度變化
- [ ] 顏色使用規定的調色板
- [ ] 圓角正確（12-16px）
- [ ] 轉換動畫平滑（300-500ms）

### 互動性測試

- [ ] 側邊欄導航工作正常
- [ ] 頁面切換流暢
- [ ] 所有輸入控件響應正常
- [ ] 沒有控制台錯誤

---

## 常見問題

### Q1: 運行時出現 "ModuleNotFoundError: No module named 'streamlit'"

**解決方案:**
```bash
pip install streamlit
```

### Q2: 頁面不更新/卡住了

**解決方案:**
```bash
# 重新啟動伺服器
# Ctrl+C 停止
streamlit run sources/streamlit_app.py
```

### Q3: 看不到預期的圖表或數據

**解決方案:**
- 檢查瀏覽器控制台是否有錯誤
- 清除瀏覽器快取
- 確保所有依賴已安裝
- 查看終端是否有錯誤消息

### Q4: 如何在遠端伺服器上運行

```bash
streamlit run sources/streamlit_app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true
```

然後訪問 `http://server-ip:8501`

### Q5: 如何修改應用和看到實時更新

1. 編輯 `sources/streamlit_app.py`
2. 保存檔案
3. 瀏覽器會自動重新加載（或在側邊欄點擊 "Rerun"）

---

## 故障排除

### 檢查步驟

#### 1. 驗證文件存在
```bash
ls -lh /Users/charles88/Desktop/AIoT/AIoT_DA_HW3/sources/streamlit_app.py
```

#### 2. 檢查 Python 版本
```bash
python --version  # 需要 3.7+
```

#### 3. 驗證依賴
```bash
python -c "import streamlit; print(streamlit.__version__)"
python -c "import plotly; print(plotly.__version__)"
```

#### 4. 檢查應用語法
```bash
python -m py_compile sources/streamlit_app.py
# 無輸出表示 OK，有錯誤會顯示
```

#### 5. 查看詳細日誌
```bash
streamlit run sources/streamlit_app.py --logger.level=debug 2>&1 | tee streamlit.log
```

### 常見錯誤和修復

| 錯誤 | 原因 | 解決方案 |
|------|------|--------|
| `ModuleNotFoundError` | 缺失依賴 | `pip install streamlit` |
| `SyntaxError` | 文件有語法錯誤 | 檢查代碼或回滾更改 |
| `Address already in use` | 端口被占用 | 用 `--server.port 8502` 更換端口 |
| 頁面全白 | 未捕獲的異常 | 查看終端和瀏覽器控制台 |
| 圖表不顯示 | Plotly 問題 | 更新 `pip install --upgrade plotly` |

---

## 開發技巧

### 1. 使用代理模型進行測試

```python
# 在應用中添加模擬數據
import streamlit as st

@st.cache_resource
def get_test_evaluators():
    """獲取測試用的模擬評估器"""
    class MockEvaluator:
        def __init__(self, name):
            self.model_name = name
            self.accuracy_test = 0.85 + np.random.random() * 0.1
            self.precision_test = 0.82 + np.random.random() * 0.1
            # ... 其他屬性
    
    return [
        MockEvaluator('Model_1'),
        MockEvaluator('Model_2'),
    ]
```

### 2. 性能優化

```python
# 使用 @st.cache_data 快取數據
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

# 使用 @st.cache_resource 快取資源
@st.cache_resource
def create_model():
    return train_model()
```

### 3. 調試技巧

```python
# 在代碼中添加調試信息
st.write("DEBUG:", variable_name)

# 查看 session state
st.write(st.session_state)

# 性能分析
import time
start = time.time()
# ... 代碼
st.write(f"耗時: {time.time() - start:.2f}s")
```

---

## 相關資源

- **Streamlit 文檔:** https://docs.streamlit.io/
- **Plotly 文檔:** https://plotly.com/python/
- **本項目文檔:** `VISUALIZATION_SUITE_README.md`

---

## 測試完成後

如果所有測試都通過了，恭喜！🎉

應用已準備好部署或進一步開發。您可以：

1. 🚀 部署到 [Streamlit Cloud](https://streamlit.io/cloud)
2. 📝 添加更多功能
3. 🎨 自定義 UI 和樣式
4. 📊 集成真實數據

---

**最後更新:** 2025-10-28  
**狀態:** ✅ 準備測試
