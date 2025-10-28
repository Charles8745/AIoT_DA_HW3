# 數據集分析報告

## 📊 您擁有的數據集

### 1️⃣ **phishing_dataset.csv**
```
行數: 11,054 行 (包括數據)
特徵: 31 列 (全數值)
格式: CSV
內容: 網釣檢測特徵
值域: -1, 0, 1
```

**特徵詳情:**
- 31 個數值特徵 (看起來是網釣網站的特性指標)
- 值範圍: -1 (否/非釣魚), 0 (不確定), 1 (是/釣魚)
- 沒有列名 (需要手動添加)
- 最後一列是目標變數 (0=非釣魚, 1=釣魚)

**使用的筆記本:**
- ✅ Decision Tree Phishing Detector
- ✅ Logistic Regression Phishing Detector

---

### 2️⃣ **sms_spam_no_header.csv**
```
行數: 5,574 行
特徵: 2 列 (分類 + 文本)
格式: CSV
內容: SMS 垃圾短信檢測
```

**特徵詳情:**
- 第 1 列: "type" (ham/spam) → 目標變數
- 第 2 列: "text" (短信文本) → 特徵

**示例:**
```
"ham","Go until jurong point, crazy.. Available only in bugis..."
"ham","Ok lar... Joking wif u oni..."
"spam","Free entry in 2 a wkly comp to win FA Cup final tkts..."
```

**使用的筆記本:**
- ✅ Bayesian Spam Detector with Nltk

---

### 3️⃣ **sms_spam_perceptron.csv**
```
行數: 100 行 (包括表頭)
特徵: 3 列
格式: CSV (帶表頭)
內容: 簡化的 SMS 垃圾短信數據
```

**特徵詳情:**
- 第 1 列: "type" (ham/spam) → 目標變數
- 第 2 列: "sex" (0/1) → 特徵
- 第 3 列: "buy" (0/1) → 特徵

**特點:**
- 🔴 **非常小的數據集** (只有 99 個樣本!)
- 只有 2 個簡化特徵
- 不是原始短信,而是預處理後的特徵

**使用的筆記本:**
- ✅ Perceptron
- ✅ Linear Regression

---

### 4️⃣ **sms_spam_svm.csv**
```
行數: 151 行 (包括表頭)
特徵: 3 列
格式: CSV (帶表頭)
內容: 簡化的 SMS 垃圾短信數據
```

**特徵詳情:**
- 第 1 列: "type" (ham/spam) → 目標變數
- 第 2 列: "suspect" → 特徵 (數值)
- 第 3 列: "neutral" → 特徵 (數值)

**特點:**
- 🔴 **很小的數據集** (只有 150 個樣本)
- 只有 2 個簡化特徵
- 不是原始短信,而是預處理後的特徵

**使用的筆記本:**
- ✅ SVM

---

## 📈 數據集對比表

| 數據集 | 筆記本 | 任務 | 行數 | 類型 | 特徵 | 特點 |
|--------|--------|------|------|------|------|------|
| **phishing_dataset.csv** | Decision Tree, Logistic Regression | 網釣檢測 | 11,054 | 數值 | 31 個 | ✅ 大型, 完整 |
| **sms_spam_no_header.csv** | Bayesian | 垃圾短信 | 5,574 | 文本 | 1 個 | ✅ 大型, 原始文本 |
| **sms_spam_perceptron.csv** | Perceptron, Linear Reg | 垃圾短信 | 99 | 數值 | 2 個 | 🔴 很小, 簡化特徵 |
| **sms_spam_svm.csv** | SVM | 垃圾短信 | 150 | 數值 | 2 個 | 🔴 很小, 簡化特徵 |

---

## 🎯 關鍵發現

### 發現 1: **兩個獨立的任務**

您的代碼分為兩個**獨立的分類任務**:

#### 任務 A: 網釣檢測 (Phishing Detection)
```
數據集: phishing_dataset.csv (11,054 行)
模型: Decision Tree, Logistic Regression
特徵: 31 個數值特徵
規模: 大型 ✅
```

#### 任務 B: 垃圾短信檢測 (Spam Detection)
```
數據集: 多個 (sms_spam_*.csv)
模型: Bayesian, Perceptron, SVM
特徵: 2-2000+ 個 (取決於數據集)
規模: 混合 (5,574 / 150 / 99)
```

---

### 發現 2: **不同的數據集特性**

#### 網釣檢測 (phishing_dataset.csv)
- ✅ 單一統一的數據集
- ✅ 11,054 個樣本 (相對大型)
- ✅ 31 個數值特徵
- ✅ 易於模型間比較
- **結論**: 適合標準化評估

#### 垃圾短信檢測 (SMS)
- ⚠️ 3 個不同的數據集!
  - sms_spam_no_header.csv (5,574 行, 原始文本)
  - sms_spam_perceptron.csv (99 行, 簡化特徵)
  - sms_spam_svm.csv (150 行, 簡化特徵)
- ⚠️ 不同的特徵表現形式
- ⚠️ 不同的樣本大小
- **結論**: 模型間無法直接比較

---

### 發現 3: **數據特徵的差異**

```
╔════════════════════════════════════════════════════════════╗
║           SMS 數據集的特徵表現形式                        ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║ sms_spam_no_header.csv                                   ║
║ ├─ 格式: 原始短信文本                                     ║
║ ├─ 行數: 5,574                                            ║
║ ├─ 特徵提取: Bayesian 在筆記本中提取                     ║
║ └─ 用於: Bayesian 算法                                   ║
║                                                            ║
║ sms_spam_perceptron.csv                                  ║
║ ├─ 格式: 預處理特徵 (sex, buy)                            ║
║ ├─ 行數: 99                                               ║
║ ├─ 特徵: 已經提取好                                       ║
║ └─ 用於: Perceptron, Linear Regression                   ║
║                                                            ║
║ sms_spam_svm.csv                                         ║
║ ├─ 格式: 預處理特徵 (suspect, neutral)                    ║
║ ├─ 行數: 150                                              ║
║ ├─ 特徵: 已經提取好                                       ║
║ └─ 用於: SVM                                              ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## 💡 對 ModelEvaluator 設計的影響

### 問題 1: 數據集不一致

根據實際數據集情況:

**❌ 無法進行跨數據集比較:**
```python
# 這個比較沒有意義!
bayes_eval = ModelEvaluator(bayes, X_train_sms, y_train_sms, X_test_sms, y_test_sms)
svm_eval = ModelEvaluator(svm, X_train_sms2, y_train_sms2, X_test_sms2, y_test_sms2)
comparison = bayes_eval.compare_with(svm_eval)  # ⚠️ 不同的訓練集!
```

**✅ 可以進行任務內比較:**
```python
# 這個比較有意義! (如果有統一的訓練集)
dt_eval = ModelEvaluator(dt, X_train_phish, y_train_phish, X_test_phish, y_test_phish)
lr_eval = ModelEvaluator(lr, X_train_phish, y_train_phish, X_test_phish, y_test_phish)
comparison = dt_eval.compare_with(lr_eval)  # ✅ 相同的訓練集
```

---

### 建議方案

根據您的數據集結構,我建議:

#### 🎯 方案 A: **只支持任務內比較** (最簡單 ⭐ 推薦)

```python
# 只允許相同任務內的模型比較

# 網釣檢測任務內比較 ✅
dt_phish = ModelEvaluator(dt, X_train_phish, y_train_phish, X_test_phish, y_test_phish)
lr_phish = ModelEvaluator(lr, X_train_phish, y_train_phish, X_test_phish, y_test_phish)
comparison = dt_phish.compare_with(lr_phish)  # ✅ OK

# 垃圾短信任務內比較... (需要統一數據集)
# ⚠️ 但您有 3 個不同的垃圾短信數據集,所以還需要決定
```

**優點:**
- ✅ 簡單清晰
- ✅ 結果準確
- ✅ 減少混淆

**缺點:**
- ❌ 功能受限
- ❌ 無法跨任務比較

---

#### 🎯 方案 B: **創建標準數據集** (完整但需修改代碼)

為每個任務創建單一標準的訓練/測試集:

```
標準化後的結構:
├─ phishing_dataset.csv (保持原樣)
│  ├─ 訓練集: 70% (7,738 行)
│  └─ 測試集: 30% (3,316 行)
│
└─ sms_spam_standard.csv (統一垃圾短信數據集)
   ├─ 訓練集: 70% (3,900 行)
   └─ 測試集: 30% (1,674 行)
   └─ 使用 sms_spam_no_header.csv 為基礎
```

**優點:**
- ✅ 所有模型可以直接比較
- ✅ 結果準確可靠
- ✅ 符合 ML 最佳實踐

**缺點:**
- ❌ 需要修改所有 5 個筆記本
- ❌ 工作量大
- ❌ 可能破壞現有筆記本

---

## 📋 現狀對澄清討論的影響

### 回答之前的問題

#### 問題 1: 數據集不一致
**您現在知道的事實:**
- 網釣檢測: 單一數據集 (11,054 行) ✅
- 垃圾短信: 3 個不同數據集 (5,574 / 150 / 99 行) ❌

**建議決策:**
```
選擇: 方案 A (只支持任務內比較)

理由:
1. 您的垃圾短信任務已經有 3 個不同的數據集
2. 強制統一會破壞現有筆記本
3. 但至少可以在每個任務內進行比較
```

---

#### 問題 2: Linear Regression 如何處理?
**您現在知道的事實:**
- Linear Regression 使用 sms_spam_perceptron.csv
- 這是一個只有 99 行和 2 個特徵的超小數據集
- 不適合用於分類評估 (它本身是回歸算法)

**建議決策:**
```
選擇: 排除 Linear Regression

理由:
1. 它是回歸算法,不是分類算法
2. 使用的數據集是分類任務 (混淆)
3. 沒有 predict_proba(),無法支援 ROC 曲線
4. 在代碼審查報告中也建議排除
```

---

#### 問題 3: 多類分類支援?
**您現在知道的事實:**
- Phishing: 2 類 (0=非釣魚, 1=釣魚)
- Spam: 2 類 (ham/spam)
- **所有任務都是二分類** ✅

**建議決策:**
```
選擇: 只支持二分類 (當前所有任務都是)

理由:
1. 您沒有多類分類任務
2. 簡化實現
3. 如果將來需要,再擴展

但可以添加 warning:
if len(np.unique(y)) != 2:
    raise ValueError("Only binary classification is supported")
```

---

## 🚀 下一步建議

### 第一步: 決定數據集策略

根據上面的分析,您需要決定:

**問題: 垃圾短信任務使用哪個數據集作為標準?**

選項:
1. **sms_spam_no_header.csv** (5,574 行, 推薦 ⭐)
   - ✅ 最大的數據集
   - ✅ 是原始文本 (完整信息)
   - ✅ Bayesian 已經在使用
   
2. **sms_spam_perceptron.csv** (99 行)
   - ❌ 太小
   - ❌ 特徵已簡化
   - ❌ 不推薦
   
3. **sms_spam_svm.csv** (150 行)
   - ❌ 太小
   - ❌ 特徵已簡化
   - ❌ 不推薦

### 第二步: 決定是否修改筆記本

**如果選擇 sms_spam_no_header.csv:**
- Bayesian: 已經在使用 ✅
- Perceptron: 需要改為使用 sms_spam_no_header.csv
- SVM: 需要改為使用 sms_spam_no_header.csv
- Linear Regression: 排除 (改用 sms_spam_no_header.csv, 但不推薦包含)

### 第三步: 修改 ModelEvaluator 設計

基於您的決定:
1. ✅ 只支持二分類
2. ✅ 排除 Linear Regression
3. ✅ 只支持任務內比較
4. ✅ 在 proposal.md 明確說明

---

## 📝 總結

您有:
- **1 個網釣檢測數據集** (11,054 行, 統一)
- **3 個垃圾短信數據集** (5,574 / 150 / 99 行, 不統一)
- **6 個 ML 筆記本** (5 個分類 + 1 個回歸)

**ModelEvaluator 建議:**
- 支持二分類 ✅
- 排除 Linear Regression ✅
- 支持任務內比較 ✅
- 記錄使用的數據集信息 ✅

**下一步:** 決定垃圾短信任務是否標準化到 sms_spam_no_header.csv
