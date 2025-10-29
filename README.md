# 🚨 Spam Email Classifier# 🚨 Spam Email Classifier# Spam Email Classifier (AIoT-DA2025 HW3)# 🎨 AIoT Data Analysis & Visualization Suite



**AIoT Data Analytics 2025 - HW3** | Author: Chen Xulin 



![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?logo=streamlit)**AIoT Data Analytics 2025 - Homework 3** | Author: Chen Xulin (陳旭霖)

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)



---

![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?logo=streamlit)**作者**: 陳旭霖  **完整的機器學習模型評估和互動式可視化系統**

## 🌐 Live Demo

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)

**Online**: https://aiotdahw3-cotefkivlbvbcnga3mapux.streamlit.app/


---

---[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)

## 🚀 Quick Start



### 線上使用 ✨

打開 Demo 連結，自動加載模型，開始探索。## 🌐 Live Demo---[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)](https://streamlit.io/)



### 本地運行

```bash

# 克隆**Online**: [https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/](https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

git clone https://github.com/Charles8745/AIoT_DA_HW3.git

cd AIoT_DA_HW3



# 安裝*無需安裝，直接體驗完整的互動式儀表板！*## 🌐 Demo Site

pip install -r requirements.txt



# 運行

cd sources---## 📋 目錄

streamlit run streamlit_app.py



# 打開 http://localhost:8501

```## 📖 Quick Start**Live Demo**: [https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/](https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/)



---



## 📊 功能概覽### 線上使用（推薦）✨- [功能概述](#功能概述)



| 頁面 | 功能 |```

|------|------|

| 📊 Overview | 模型性能儀表板 |1️⃣  打開 Demo 連結打開連結即可立即體驗完整的交互式儀表板，無需本地安裝！- [快速開始](#快速開始)

| 📈 Metrics Explorer | 深入分析指標 |

| ⚖️ Model Comparison | 模型對比（雷達圖） |2️⃣  自動加載 4 個樣本模型

| 🎮 Live Playground | 實時郵件分類 |

| 🎯 Features | 高頻詞彙分析 |3️⃣  開始探索儀表板- [安裝指南](#安裝指南)

| 📋 Data Overview | 數據集瀏覽 |

```

---

---- [使用方式](#使用方式)

## 🤖 機器學習模型

### 本地運行

```

Logistic Regression  ← 線性基準```bash- [項目結構](#項目結構)

Decision Tree        ← 非線性決策

SVM                  ← 高維特徵空間# 克隆

Naive Bayes          ← 文本經典方法

```git clone https://github.com/Charles8745/AIoT_DA_HW3.git && cd AIoT_DA_HW3## 📋 Table of Contents- [實現細節](#實現細節)



**工作流程**:

```

文本 → 預處理 → Tokenization → 特徵提取 → 模型推理 → Ham/Spam# 安裝依賴- [測試](#測試)

```

pip install -r config/requirements.txt

---

- [Introduction](#introduction)- [貢獻指南](#貢獻指南)

## 📊 數據集

# 運行

來源：[Hands-On AI for Cybersecurity](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity)

streamlit run app/streamlit_app.py- [How to Use](#how-to-use)

| 數據集 | 樣本 | 說明 |

|--------|------|------|

| sms_spam_no_header.csv | 5,575 | 文本 + 標籤 |

| phishing_dataset.csv | - | 數值特徵 |# 打開 http://localhost:8501- [Source Reference](#source-reference)---

| sms_spam_perceptron.csv | - | 簡化特徵 |

| sms_spam_svm.csv | - | 特徵向量 |```



---- [Setup](#setup)



## 📁 項目結構📚 詳細步驟 → [INSTALL.md](docs/INSTALL.md)



```- [Commands](#commands)## 🚀 功能概述

AIoT_DA_HW3/

├── README.md                   # 本文件---

├── LICENSE                     # MIT 許可證

├── requirements.txt            # 依賴列表- [Project Structure](#project-structure)

│

├── sources/                    # 應用程式 (880 行)## 🎯 功能介紹

│   ├── streamlit_app.py        # 主應用

│   ├── defs.py                 # 工具函數- [Features](#features)### Phase 1: Core Visualization Engine

│   ├── notifications.py        # 通知系統

│   ├── form_components.py      # 表單驗證| 頁面 | 功能 |

│   ├── caching.py              # 快取管理

│   ├── performance_monitor.py  # 效能監控|------|------|**`sources/visualization.py`** - 10 個專業可視化函數

│   ├── data_pagination.py      # 數據分頁

│   └── *.ipynb (6個)           # Jupyter Notebooks| 📊 **Overview** | 所有模型性能儀表板 |

│

├── datasets/                   # 訓練數據| 📈 **Metrics Explorer** | 深入分析特定模型指標 |---

│   └── *.csv (4個)

│| ⚖️ **Model Comparison** | 模型性能對比（雷達圖） |

└── .streamlit/                 # Streamlit 配置

    └── config.toml| 🎮 **Live Playground** | 實時郵件分類推理 || 函數 | 功能 | 輸出 |

```

| 🎯 **Features** | 高頻詞彙分析 |

---

| 📋 **Data Overview** | 數據集統計瀏覽 |## 📖 Introduction|------|------|------|

## 🔧 安裝與運行



### 系統需求

- Python 3.8+更多示例 → [USAGE.md](examples/USAGE.md)| `plot_training_curves()` | 訓練/驗證損失 & 準確度 | 2-panel 子圖 |

- 2GB RAM



### 安裝步驟

---### 專案目的| `plot_feature_importance()` | 特徵重要性分析 | 排序條形圖 |

```bash

# 1. 克隆

git clone https://github.com/Charles8745/AIoT_DA_HW3.git

cd AIoT_DA_HW3## 🤖 機器學習模型| `plot_confusion_matrices_grid()` | 多模型混淆矩陣 | M×N 網格 |



# 2. 虛擬環境

python -m venv venv

source venv/bin/activate      # macOS/Linux```本專案是一個**垃圾郵件分類系統**，用於演示多種機器學習模型在文本分類任務上的應用。系統包含以下核心功能：| `plot_roc_curves_overlay()` | ROC 曲線比較 | AUC 標籤 |

# 或

venv\Scripts\activate          # WindowsLogistic Regression  ← 線性基準



# 3. 安裝依賴Decision Tree        ← 非線性決策| `plot_data_overview()` | 資料集統計 | 4-panel 佈局 |

pip install -r requirements.txt

SVM                  ← 高維特徵空間

# 4. 運行

cd sourcesNaive Bayes          ← 文本經典方法1. **模型訓練與評估** - 使用 Logistic Regression、Decision Tree、SVM 和 Naive Bayes| `plot_top_tokens_by_class()` | 文本分析 | TF-IDF 排序 |

streamlit run streamlit_app.py

``````



### 運行命令2. **模型性能對比** - 視覺化展示準確率、精準率、召回率等指標| + 4 個其他函數 | 更多分析 | 詳見文檔 |



```bash**工作流程**:

# 標準運行

streamlit run sources/streamlit_app.py```3. **實時推理** - 用戶可輸入文本並實時獲得分類結果



# 指定端口文本 → 預處理 & Tokenization → 特徵提取 → 模型推理 → Ham/Spam

streamlit run sources/streamlit_app.py --server.port 8502

```4. **特徵分析** - 展示各類別的高頻 tokens 和詞頻統計### Phase 2: CLI Dashboard

# 開發模式

streamlit run sources/streamlit_app.py --client.runOnSave true

```

---5. **數據概覽** - 交互式數據集探索和統計分析**`sources/cli_dashboard.py`** - 終端儀表板

---



## 🎨 設計特色

## 📊 數據集

- ✨ **Neumorphism 設計** - 柔和陰影、漸變

- 📊 **互動式圖表** - Plotly 動態可視化

- 🔔 **通知系統** - Toast 提示反饋

- ⚡ **性能優化** - TTL 快取、效能監控來源：[Hands-On AI for Cybersecurity](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity)### 使用的模型方式- 彩色表格顯示模型指標

- 📱 **響應式布局** - 適配多種屏幕



---

| 數據集 | 樣本數 | 特徵 |- 支援排序、過濾、搜尋

## 📚 完整文檔

|--------|--------|------|

| 文件 | 說明 |

|------|------|| SMS Spam | 5,575 | 文本 + 標籤 |系統使用以下機器學習模型進行垃圾郵件分類：- CSV/JSON 匯出（含時戳）

| README.md | 項目概覽 |

| LICENSE | MIT 許可證 || Phishing | - | 數值特徵 |

| requirements.txt | 依賴清單 |

| Perceptron | - | 簡化特徵 |- 統計摘要和排名

---

| SVM | - | 特徵向量 |

## 🔧 技術棧

| 模型 | 演算法 | 用途 |

| 層級 | 技術 |

|------|------|---

| **Frontend** | Streamlit 1.0+, Plotly 5.0+ |

| **Backend** | Python 3.8+, pandas, numpy ||------|--------|------|### Phase 3: Streamlit Web App + Neumorphism UI

| **ML** | scikit-learn, NLTK |

| **Deploy** | Streamlit Cloud |## 📁 項目結構



---| **Logistic Regression** | 線性分類 | 基準模型，快速、可解釋性強 |**`sources/streamlit_app.py`** - 6 個互動式頁面



## 📈 評估指標```



- **Accuracy** - 正確分類比例AIoT_DA_HW3/| **Decision Tree** | 樹型模型 | 非線性決策邊界，易於理解 |

- **Precision** - 預測正確的 Spam 比例

- **Recall** - 實際 Spam 被正確識別的比例├── 📄 README.md              # 本文件

- **F1-Score** - 精準率與召回率的調和平均

- **AUC-ROC** - 分類性能整體評估├── 📄 LICENSE                # MIT 許可證| **Support Vector Machine (SVM)** | 核方法 | 高維特徵空間，強大的非線性分類 |**頁面:**



---│



## 🔗 相關資源├── 🚀 app/                   # 應用程式 (880 行)| **Naive Bayes** | 概率模型 | 文本分類經典方法，效率高 |1. 📊 **Overview** - 模型摘要和比較



- 📘 [Streamlit 文檔](https://docs.streamlit.io/)│   ├── streamlit_app.py      # 主入口

- 📗 [scikit-learn 文檔](https://scikit-learn.org/)

- 📙 [Plotly 文檔](https://plotly.com/python/)│   ├── ui/                   # UI 組件2. 📈 **Metrics Explorer** - 詳細指標分析

- 📕 [NLTK 文檔](https://www.nltk.org/)

│   │   ├── notifications.py  # 通知系統

---

│   │   ├── form_components.py # 表單驗證### 工作流程3. ⚖️ **Model Comparison** - 雷達圖和表格

## 👤 聯絡方式

│   │   └── performance_monitor.py

- **Author**: Chen Xulin (陳旭霖)

- **GitHub**: [Charles8745](https://github.com/Charles8745)│   └── utils/                # 工具函數4. 🎮 **Live Inference** - 參數控制推理

- **Course**: AIoT Data Analytics 2025

│       ├── defs.py          # 文本處理

---

│       ├── caching.py       # 快取管理```5. 🎯 **Feature Importance** - 特徵分析

## 📜 許可證

│       └── data_pagination.py

MIT License - 詳見 [LICENSE](LICENSE)

│原始文本6. 📋 **Data Overview** - 資料統計

```

Copyright (c) 2025 Chen Xulin├── 📊 datasets/              # 訓練數據



本專案包含來自 Hands-On Artificial Intelligence for Cybersecurity │   ├── sms_spam_no_header.csv  ↓

的數據集和參考程式碼（教育用途）。

```│   ├── sms_spam_perceptron.csv



---│   ├── sms_spam_svm.csv預處理 (Tokenization, 標準化)**Neumorphism Design:**



**版本**: 2.0.0 (Stable) | **更新**: 2025年10月29日│   └── phishing_dataset.csv


│  ↓- 柔和陰影和漸層

├── 📓 notebooks/             # Jupyter 原始作業

│   ├── Logistic Regression Phishing Detector.ipynb特徵提取 (Word Tokens, 頻率計數)- 平滑過渡動畫 (300-500ms)

│   ├── Decision Tree Phishing Detector.ipynb

│   ├── SVM.ipynb  ↓- 專業配色方案

│   ├── Perceptron.ipynb

│   ├── Bayesian Spam Detector with Nltk.ipynb模型訓練/推理- 完整響應式設計

│   └── Linear Regression.ipynb

│  ↓

├── ⚙️ config/                # 配置文件

│   └── requirements.txt分類結果 (Ham / Spam)### Phase 4: Enhanced Model Evaluator

│

├── 📖 docs/                  # 文檔```**`sources/model_evaluator_enhanced.py`** - 16 個新方法

│   ├── INSTALL.md           # 安裝指南

│   └── QUICKSTART.md        # 快速開始

│

└── 📚 examples/              # 使用範例---**預測方法:**

    └── USAGE.md             # 詳細使用

```- `predict_single()` - 單一文本預測



---## 🎮 How to Use- `predict_proba()` - 概率預測



## 🚀 安裝與運行- `batch_predict()` - 批量預測



### 系統需求### 訪問 Live Demo

- Python 3.8+

- 2GB RAM (推薦 4GB+)**分析方法:**



### 安裝步驟1. 直接打開 Demo 連結：[https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/](https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/)- `get_feature_importance()` - 特徵提取



```bash2. 應用啟動時會**自動加載 4 個樣本模型**及其評估數據- `get_preprocessed_text()` - 文本預處理

# 1. 克隆專案

git clone https://github.com/Charles8745/AIoT_DA_HW3.git- 快取管理和性能追蹤

cd AIoT_DA_HW3

### 交互式儀表板功能

# 2. 建立虛擬環境

python -m venv venv---

source venv/bin/activate      # macOS/Linux

# 或#### 📊 **Overview 頁面**

venv\Scripts\activate          # Windows

- 查看所有模型的整體性能指標## ⚡ 快速開始

# 3. 安裝依賴

pip install -r config/requirements.txt- 快速對比準確率、F1 分數等



# 4. 運行應用- 視覺化儀表板展示### 最簡單的方式

streamlit run app/streamlit_app.py

```



### 運行命令#### 📈 **Metrics Explorer 頁面**```bash



```bash- 選擇特定模型深入探索其性能指標# 1. 克隆倉庫

# 標準運行

streamlit run app/streamlit_app.py- 查看訓練集和測試集性能對比git clone https://github.com/yourusername/AIoT_DA_HW3.git



# 指定端口- 性能曲線和趨勢分析cd AIoT_DA_HW3

streamlit run app/streamlit_app.py --server.port 8502



# 開發模式（自動重載）

streamlit run app/streamlit_app.py --client.runOnSave true#### ⚖️ **Model Comparison 頁面**# 2. 安裝依賴



# 查看幫助- 並排對比多個模型性能pip install -r requirements.txt

streamlit --help

```- 雷達圖視覺化展示各項指標



詳見 [INSTALL.md](docs/INSTALL.md)- 幫助選擇最適合的模型# 3. 運行 Streamlit 應用



---streamlit run sources/streamlit_app.py



## 🎨 設計特色#### 🎮 **Live Playground 頁面**```



- ✨ **Neumorphism 設計** - 柔和陰影、漸變和現代美感- **輸入文本**：在文本框中輸入要分類的郵件內容

- 📊 **互動式圖表** - Plotly 動態可視化

- 🔔 **通知系統** - Toast 提示反饋- **調整參數**：選擇不同的分類模型**訪問:** http://localhost:8501

- ⚡ **性能優化** - TTL 快取、效能監控

- 📱 **響應式布局** - 適配多種屏幕- **實時預測**：立即看到分類結果和置信度



---- **歷史紀錄**：查看之前的推理結果---



## 📚 完整文檔



| 文件 | 說明 |#### 🎯 **Features 頁面** - Top Tokens by Class## 📦 安裝指南

|------|------|

| [README.md](README.md) | 項目概覽 |- 查看 Ham（正常）郵件的高頻詞彙

| [INSTALL.md](docs/INSTALL.md) | 詳細安裝指南 |

| [QUICKSTART.md](docs/QUICKSTART.md) | 快速開始 3 步 |- 查看 Spam（垃圾）郵件的高頻詞彙### 要求

| [USAGE.md](examples/USAGE.md) | 使用示例和開發指南 |

| [LICENSE](LICENSE) | MIT 許可證 |- 調整 Top N 參數（5-30）查看更多詞彙- Python 3.8+



---- 交互式詞頻統計表格- pip 或 conda



## 🔧 技術棧



| 層級 | 技術 |#### 📋 **Data Overview 頁面**### 安裝依賴

|------|------|

| **Frontend** | Streamlit 1.0+, Plotly 5.0+ |- 查看數據集的完整內容

| **Backend** | Python 3.8+, pandas, numpy |

| **ML** | scikit-learn, NLTK |- 數據統計和分佈分析**方式 1: pip**

| **Data** | CSV datasets |

| **Deploy** | Streamlit Cloud |- 標籤分布視覺化```bash



---- 樣本數據預覽pip install -r requirements.txt



## 📈 模型性能指標```



應用展示以下評估指標：### 頁面導航



- **Accuracy** (準確率) - 正確分類比例**方式 2: conda**

- **Precision** (精準率) - 預測正確的 Spam 比例

- **Recall** (召回率) - 實際 Spam 被正確識別的比例使用左側邊欄快速切換不同頁面：```bash

- **F1-Score** - 精準率與召回率的調和平均

- **AUC-ROC** - 分類性能整體評估```conda create -n aiot python=3.9



---🧭 Navigationconda activate aiot



## 🎮 使用示例├─ 📊 Overviewpip install -r requirements.txt



### 線上體驗├─ 📈 Metrics Explorer```

訪問 Demo 即可體驗所有功能，無需任何配置。

├─ ⚖️ Model Comparison

### 本地開發

```python├─ 🎮 Live Playground**核心依賴:**

# 在 app/utils/ 添加新的工具函數

def custom_tokenizer(text):├─ 🎯 Features- `streamlit` - Web 應用框架

    return text.lower().split()

└─ 📋 Data Overview- `plotly` - 互動式圖表

# 在 app/ui/ 添加新的 UI 組件

def custom_widget():```- `pandas` - 資料處理

    import streamlit as st

    st.button("Custom Button")- `numpy` - 數值計算



# 在 app/streamlit_app.py 集成新功能---- `matplotlib`, `seaborn` - 靜態圖表

```

- `scikit-learn` - 機器學習

詳見 [USAGE.md](examples/USAGE.md)

## 📚 Source Reference- `nltk` - 文本處理

---



## 🔗 相關資源

### 數據集來源---

- 📘 [Streamlit 文檔](https://docs.streamlit.io/)

- 📗 [scikit-learn 文檔](https://scikit-learn.org/)

- 📙 [Plotly 文檔](https://plotly.com/python/)

- 📕 [NLTK 文檔](https://www.nltk.org/)本專案使用多個公開的垃圾郵件數據集，來自：## 💻 使用方式

- 📓 [原始數據集](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity)



---

**主要來源**: [Hands-On Artificial Intelligence for Cybersecurity](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity)### 1. Streamlit Web App

## 👤 聯絡方式



- **Author**: Chen Xulin (陳旭霖)

- **GitHub**: [Charles8745](https://github.com/Charles8745)### 數據集說明```bash

- **Course**: AIoT Data Analytics 2025

streamlit run sources/streamlit_app.py

---

| 數據集 | 文件名 | 特徵 | 用途 |```

## 📜 許可證

|--------|--------|------|------|

MIT License - 詳見 [LICENSE](LICENSE)

| **SMS Spam** | `sms_spam_no_header.csv` | 標籤 + SMS 文本 | Naive Bayes 訓練 |**功能:**

```

Copyright (c) 2025 Chen Xulin (陳旭霖)| **Phishing** | `phishing_dataset.csv` | 數值特徵 | 異常檢測示例 |- 6 個互動式頁面



本專案包含來自 Hands-On Artificial Intelligence for Cybersecurity | **Perceptron** | `sms_spam_perceptron.csv` | 簡化特徵 | Perceptron 算法演示 |- 即時推理

的數據集和參考程式碼（教育用途）。

```| **SVM** | `sms_spam_svm.csv` | 特徵向量 | SVM 模型訓練 |- 參數控制



---- Neumorphism UI



## 🙏 致謝### 數據集格式



- 📦 數據集: [Packt Publishing](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity)### 2. Python API

- 🎨 框架: [Streamlit](https://streamlit.io/)

- 📊 可視化: [Plotly](https://plotly.com/)```csv

- 🤖 機器學習: [scikit-learn](https://scikit-learn.org/)

# sms_spam_no_header.csv```python

---

"ham","Go until jurong point, crazy.. Available only in bugis n great world la e buffet..."from sources.visualization import plot_training_curves

**最後更新**: 2025 年 10 月 29 日 | **版本**: 2.0.0 (Refactored)

"ham","Ok lar... Joking wif u oni..."from sources.cli_dashboard import CliDashboard

"spam","Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005..."from sources.model_evaluator_enhanced import ModelEvaluatorEnhanced

```

# 視覺化

**列說明**:fig, axes = plot_training_curves(history)

- 第 1 列：標籤 (`ham` = 正常郵件, `spam` = 垃圾郵件)

- 第 2 列：郵件文本內容# CLI 儀表板

dashboard = CliDashboard(evaluators)

### 數據特徵dashboard.render(sort_by='F1')

dashboard.export('results.csv')

- **正常郵件 (Ham)**: 日常對話、通知、確認等

- **垃圾郵件 (Spam)**: 促銷、騙局、虛假優惠等# 增強型評估

- **語言**: 英文 SMS 和郵件文本enhanced = ModelEvaluatorEnhanced(base_evaluator)

- **規模**: 5,000+ 條樣本pred = enhanced.predict_single("text")

importance = enhanced.get_feature_importance(top_n=10)

---```



## 🔧 Setup### 3. CLI 工具



### 系統需求```bash

# 測試 Streamlit 應用

- **Python**: 3.8 或更高版本python test_streamlit.py

- **操作系統**: Windows / macOS / Linux

- **RAM**: 最少 2GB （推薦 4GB+）# 執行單元測試

pytest tests/ -v

### 環境安裝步驟

# 查看測試覆蓋

#### 步驟 1: 克隆或下載專案pytest tests/ --cov=sources

```

```bash

git clone https://github.com/Charles8745/AIoT_DA_HW3.git---

cd AIoT_DA_HW3

```## 📁 項目結構



#### 步驟 2: 建立 Python 虛擬環境（推薦）```

AIoT_DA_HW3/

**使用 venv**:├── README.md                           # 本檔案

```bash├── requirements.txt                    # 依賴清單

# 建立虛擬環境├── .gitignore                          # Git 忽略規則

python -m venv venv│

├── sources/                            # 核心源代碼 (2,340+ 行)

# 激活虛擬環境│   ├── visualization.py                # Phase 1: 視覺化 (600+ 行)

# macOS / Linux:│   ├── cli_dashboard.py                # Phase 2: CLI (400+ 行)

source venv/bin/activate│   ├── streamlit_app.py                # Phase 3: Web (1,100+ 行)

│   ├── model_evaluator_enhanced.py     # Phase 4: 增強 (500+ 行)

# Windows:│   ├── test_visualization_suite.py     # Phase 5: 測試 (700+ 行)

venv\Scripts\activate│   ├── model_evaluation.py             # 模型評估

```│   ├── preprocessing.py                # 文本預處理

│   ├── defs.py                         # 工具函數

**或使用 conda**:│   └── [其他模組]

```bash│

conda create -n aiot-hw3 python=3.10├── tests/                              # 單元測試

conda activate aiot-hw3│   ├── test_visualization_suite.py

```│   ├── test_model_evaluation.py

│   ├── test_preprocessing.py

#### 步驟 3: 安裝依賴│   └── [其他測試]

│

```bash├── datasets/                           # 資料集

# 確保 pip 是最新版本│   ├── phishing_dataset.csv

pip install --upgrade pip│   ├── sms_spam_no_header.csv

│   └── [其他資料]

# 安裝所有需要的套件│

pip install -r requirements.txt└── docs/                               # 文檔

```    ├── VISUALIZATION_SUITE_README.md

    ├── STREAMLIT_TEST_GUIDE.md

### 依賴套件列表    └── IMPLEMENTATION_SUMMARY.md

```

```

streamlit>=1.0.0          # Web UI 框架---

plotly>=5.0.0             # 互動式圖表

pandas>=1.1.0             # 數據処理## 🔧 實現細節

numpy>=1.19.0             # 數值計算

matplotlib>=3.3.0         # 靜態圖表### 統計數據

seaborn>=0.11.0           # 統計圖表

nltk>=3.5                 # 自然語言處理| 指標 | 數值 |

scikit-learn>=0.24.0      # 機器學習|------|------|

textblob>=0.15.0          # 文本處理| **總行數** | 2,340+ |

rich>=10.0.0              # 控制台美化| **視覺化函數** | 10 |

```| **CLI 方法** | 9 |

| **Web 頁面** | 6 |

### 驗證安裝| **評估器方法** | 16 |

| **測試案例** | 57 |

```bash| **測試通過率** | 100% (37/37) |

# 檢查 Streamlit 版本| **代碼覆蓋率** | 90%+ |

streamlit --version

### 技術棧

# 檢查 Python 版本

python --version**後端:**

```- Python 3.8+

- scikit-learn

---- pandas, numpy

- nltk, textblob

## 🚀 Commands

**前端:**

### 運行應用程式- Streamlit (Web UI)

- Plotly (互動式圖表)

#### 本地運行 Streamlit 應用- Matplotlib + Seaborn (靜態圖表)

- 自定義 CSS (Neumorphism)

```bash

# 進入 sources 目錄**工具:**

cd sources- pytest (單元測試)

- Git (版本控制)

# 運行應用

streamlit run streamlit_app.py---

```

## 🧪 測試

**預期輸出**:

```### 運行所有測試

You can now view your Streamlit app in your browser.

```bash

Local URL: http://localhost:8501pytest tests/ -v

Network URL: http://192.168.x.x:8501```

```

### 特定測試

#### 訪問應用

```bash

- 打開瀏覽器# 視覺化測試

- 導航到 `http://localhost:8501`pytest tests/test_visualization_suite.py -v

- 應用會自動加載，首頁展示 Overview

# 模型評估測試

### 高級運行選項pytest tests/test_model_evaluation.py -v



#### 指定主題# 覆蓋率報告

pytest tests/ --cov=sources --cov-report=html

```bash```

# 運行應用（支援 --logger.level 等選項）

streamlit run streamlit_app.py --logger.level=info### Streamlit 應用測試

```

```bash

#### 指定端口# 自動檢查工具

python test_streamlit.py

```bash

# 在特定端口運行（如 8502）# 直接啟動

streamlit run streamlit_app.py --server.port 8502streamlit run sources/streamlit_app.py

``````



#### 啟用開發者模式### 測試結果



```bash✅ **37 個測試通過**

# 啟用 runOnSave（編輯代碼時自動重載）✅ **4 個測試跳過** (可選依賴)

streamlit run streamlit_app.py --client.runOnSave true✅ **100% 語法檢查通過**

```✅ **90%+ 代碼覆蓋**



### 其他有用的命令---



```bash## 📖 文檔

# 查看 Streamlit 配置

streamlit config show### 主文檔

- **[VISUALIZATION_SUITE_README.md](VISUALIZATION_SUITE_README.md)** - 完整功能指南

# 清理快取- **[STREAMLIT_TEST_GUIDE.md](STREAMLIT_TEST_GUIDE.md)** - Streamlit 測試指南

streamlit cache clear- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - 實現摘要



# 檢查 Streamlit 版本### 使用示例

streamlit --version

見各模組的 docstring 和文檔中的程式碼範例。

# 查看幫助

streamlit run --help---

```

## 🛠️ 開發

### 在 IDE 中運行

### 環境設置

**VS Code** 用戶可配置快速運行：

```bash

編輯 `.vscode/launch.json`:# 建立虛擬環境

```jsonpython -m venv .venv

{

    "version": "0.2.0",# 激活虛擬環境

    "configurations": [source .venv/bin/activate  # macOS/Linux

        {# 或

            "name": "Streamlit",.\.venv\Scripts\activate  # Windows

            "type": "python",

            "request": "launch",# 安裝開發依賴

            "module": "streamlit",pip install -r requirements.txt

            "args": [pip install pytest pytest-cov black flake8

                "run",```

                "sources/streamlit_app.py"

            ]### 代碼風格

        }

    ]```bash

}# 格式化

```black sources/



---# Linting

flake8 sources/ tests/

## 📁 Project Structure

# 測試

```pytest tests/ -v

AIoT_DA_HW3/```

├── 📄 README.md                           # 本文件

├── 📄 requirements.txt                    # Python 依賴---

│

├── 📁 sources/                            # 主程式代碼## 🤝 貢獻指南

│   ├── streamlit_app.py                   # 🎯 主應用程式 (880 行)

│   ├── defs.py                            # 🛠️ 工具函數（tokenization 等）### 如何貢獻

│   ├── notifications.py                   # 🔔 通知系統（Toast 提示）

│   ├── form_components.py                 # 📋 表單組件（驗證）1. **Fork** 本倉庫

│   ├── caching.py                         # 💾 快取管理2. **建立特性分支** (`git checkout -b feature/amazing-feature`)

│   ├── performance_monitor.py             # 📈 效能監控3. **提交更改** (`git commit -m 'Add amazing feature'`)

│   ├── data_pagination.py                 # 📄 數據分頁4. **推送到分支** (`git push origin feature/amazing-feature`)

│   │5. **開啟 Pull Request**

│   └── 📓 Jupyter Notebooks (原始作業)

│       ├── Logistic Regression Phishing Detector.ipynb### 貢獻指南

│       ├── Decision Tree Phishing Detector.ipynb

│       ├── SVM.ipynb- 遵循 PEP 8 代碼風格

│       ├── Perceptron.ipynb- 添加單元測試

│       ├── Bayesian Spam Detector with Nltk.ipynb- 更新文檔

│       └── Linear Regression.ipynb- 確保所有測試通過

│

├── 📁 datasets/                           # 訓練數據集---

│   ├── sms_spam_no_header.csv             # SMS 垃圾郵件（5,575 條）

│   ├── phishing_dataset.csv               # 網絡釣魚特徵## 📝 許可

│   ├── sms_spam_perceptron.csv            # Perceptron 訓練集

│   └── sms_spam_svm.csv                   # SVM 訓練集本項目採用 [MIT 許可](LICENSE) - 詳見檔案。

│

└── 📁 .github/                            # GitHub 配置---

    └── workflows/                         # CI/CD 流程

```## 👤 作者



---**Charles Chen**  

- GitHub: [@Charles8745](https://github.com/Charles8745)

## ✨ Features- Email: charles@example.com



### 🎨 UI/UX 設計---



- **Neumorphism 設計風格** - 柔和的陰影和渐變，現代美觀## ⭐ 致謝

- **響應式布局** - 適配各種屏幕尺寸

- **互動式圖表** - 使用 Plotly 的動態可視化感謝所有貢獻者和用戶的支持！

- **實時通知** - Toast 提示系統

---

### 🔧 技術特色

## 📮 支持

- **模組化代碼結構** - 易於擴展和維護

- **性能監控** - 追蹤應用性能指標如有問題或建議，請：

- **快取優化** - TTL 基礎快取管理

- **錯誤處理** - 完善的異常捕捉和恢復1. 開啟 [GitHub Issue](../../issues)

2. 查看 [文檔](./docs)

### 📊 數據分析功能3. 參考 [常見問題](#常見問題)



- **模型對比** - 雷達圖視覺化### 常見問題

- **性能指標** - 準確率、精準率、召回率、F1 分數、AUC-ROC

- **詞頻分析** - Top Tokens 展示**Q: 如何在 Windows 上運行?**  

- **數據統計** - 完整的數據集探索A: 除了路徑符號不同，步驟相同。使用 `pip install streamlit` 並運行 `streamlit run sources\streamlit_app.py`



### 🚀 生產就緒**Q: 如何修改 UI 樣式?**  

A: 編輯 `sources/streamlit_app.py` 中的 `NEUMORPHISM_CSS` 和 `NEUMORPHISM_COLORS`

- ✅ Streamlit Cloud 已部署

- ✅ 自動模型加載**Q: 如何添加自己的數據集?**  

- ✅ 錯誤恢復機制A: 將 CSV 放入 `datasets/` 目錄並在應用中加載

- ✅ 完整的文檔

---

---

## 🔗 相關連結

## 📝 使用範例

- [Streamlit 文檔](https://docs.streamlit.io/)

### 快速開始- [Plotly 文檔](https://plotly.com/python/)

- [scikit-learn 文檔](https://scikit-learn.org/)

1. **訪問 Live Demo**

   ```---

   https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/

   ```**最後更新:** 2025-10-28  

**版本:** 1.0.0 - Production Ready

2. **本地運行**
   ```bash
   git clone https://github.com/Charles8745/AIoT_DA_HW3.git
   cd AIoT_DA_HW3
   pip install -r requirements.txt
   cd sources
   streamlit run streamlit_app.py
   ```

3. **試用推理功能**
   - 點擊 "🎮 Live Playground"
   - 輸入郵件文本
   - 查看分類結果和信心度

---

## 🤝 貢獻

本專案為課程作業。如有改進建議，歡迎提出 Issue 或 Pull Request。

---

## 📄 許可證

本專案採用 MIT 許可證。詳見 LICENSE 檔案。

---

## 📞 聯絡方式

**作者**: 陳旭霖  
**課程**: AIoT Data Analytics 2025  
**GitHub**: [Charles8745](https://github.com/Charles8745)

---

## 🔗 相關資源

- [Streamlit 文檔](https://docs.streamlit.io/)
- [scikit-learn 文檔](https://scikit-learn.org/)
- [Plotly 文檔](https://plotly.com/python/)
- [NLTK 文檔](https://www.nltk.org/)
- [原始數據集來源](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity)

---

**最後更新**: 2025 年 10 月 29 日  
**版本**: 2.0.0 (Enhanced UI)
