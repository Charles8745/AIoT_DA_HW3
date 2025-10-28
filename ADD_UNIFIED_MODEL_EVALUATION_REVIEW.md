# add-unified-model-evaluation 提案審查報告

日期: 2025-10-22  
審查者: AI Assistant  
狀態: ⚠️ 需要澄清和改進

## 審查概述

提案整體良好，但存在以下需要澄清和改進的地方：

## 🔴 關鍵問題 (必須解決)

### 1. 數據集不一致問題 ⚠️
**位置**: design.md, spec.md  
**問題**: 提案假設所有模型使用相同的 train/test 數據，但實際情況並非如此

**當前代碼中的不一致:**
```
- Bayesian 使用: sms_spam_no_header.csv
- Decision Tree 使用: phishing_dataset.csv  
- Perceptron 使用: sms_spam_perceptron.csv
- SVM 使用: sms_spam_svm.csv
- Logistic Regression 使用: phishing_dataset.csv
```

**問題**: 如果每個模型使用不同的數據集，`compare_with()` 的結果將不可比較

**建議修改:**
```markdown
### 數據集標準化策略
1. **選項 A**: 定義標準評估數據集 (推薦)
   - 垃圾短信任務: sms_spam_no_header.csv
   - 網釣檢測任務: phishing_dataset.csv

2. **選項 B**: ModelEvaluator 支援多數據集
   - 在 report 中註明使用的數據集
   - compare_with() 檢查數據集一致性

3. **選項 C**: 創建標準化訓練集
   - 統一分割策略 (train_size, test_size)
   - 使用相同的隨機種子
```

**改進**: ⭐ 強烈建議在 proposal.md 中明確說明

---

### 2. 模型兼容性不明確 ⚠️
**位置**: design.md  
**問題**: 提案說"任何 sklearn 兼容模型"，但沒有說明驗證和錯誤處理

**潛在問題:**
- 不支持 sklearn 的模型 (例如自訂實現) 會導致運行時錯誤
- 不同模型的輸出格式可能不同
- 某些模型可能沒有 `predict_proba()` 方法 (ROC 曲線需要)

**建議修改:**
```markdown
### 模型兼容性
**支援的模型類型:**
1. scikit-learn 分類器 (所有)
   - 需要: predict(), predict_proba() (用於 ROC)
   - 驗證: isinstance(model, BaseEstimator)

2. 不支援的模型:
   - 自訂模型 (需先包裝為 sklearn 兼容)
   - 不提供 predict_proba 的模型 (ROC 曲線將跳過)

**錯誤處理:**
```python
def __init__(self, model, X_train, y_train, X_test, y_test):
    if not hasattr(model, 'predict'):
        raise ValueError("Model must have predict method")
    if not hasattr(model, 'predict_proba'):
        warnings.warn("Model lacks predict_proba - ROC curve unavailable")
```

**改進**: ⭐ 在 design.md 中新增"模型兼容性"部分

---

### 3. 二分類 vs 多類分類支援不明確 ⚠️
**位置**: spec.md  
**問題**: 所有示例都是二分類，沒有明確多類分類支援

**需要澄清的問題:**
- Linear Regression 用於回歸，不是分類 (為什麼在評估框架中?)
- Decision Tree 可能用於多類分類
- ROC 曲線對多類分類的支援是什麼?

**建議修改:**
```markdown
### 分類類型支援

#### 支援的分類類型
1. **二分類** (Binary Classification)
   - Bayesian (垃圾/非垃圾)
   - Logistic Regression (釣魚/非釣魚)
   - Perceptron
   - SVM
   
2. **多類分類** (Multi-class Classification)
   - Decision Tree (可支援多類)
   - 其他模型如適用

#### 指標計算
- **二分類**: 標準精度、召回率、F1、AUC-ROC
- **多類**: 
  - macro-averaged: 平均所有類別
  - weighted-averaged: 按類別頻率加權
  - per-class: 每個類別單獨顯示

#### ROC 曲線
- **二分類**: 標準 ROC 曲線
- **多類**: One-vs-Rest ROC 曲線 (每類一條)

#### 混淆矩陣
- **二分類**: 2x2 矩陣
- **多類**: NxN 矩陣，支援熱力圖視覺化
```

**改進**: ⭐ 在 spec.md 中詳細說明

---

## 🟡 中度問題 (應該改進)

### 4. Linear Regression 包含在評估框架中？

**問題**: Linear Regression 在 `sources/` 中，但它是回歸模型，不是分類模型

**當前狀態:**
- 所有評估指標設計用於分類
- Linear Regression 不能使用 accuracy、precision、recall 等

**建議:**
```markdown
### 支援的算法

**分類算法** (支援 ModelEvaluator):
✅ Bayesian Spam Detector
✅ Decision Tree Phishing Detector
✅ Perceptron
✅ SVM
✅ Logistic Regression

**不支援** (回歸算法):
❌ Linear Regression (不包含在 ModelEvaluator 中)

註: 如果需要支援 Linear Regression，需要創建單獨的 RegressionEvaluator
```

**改進**: ⭐ 在 proposal.md 或 spec.md 中澄清

---

### 5. 現有代碼中的評估邏輯重複不夠明確

**問題**: 提案說減少 30-40% 代碼重複，但沒有具體例子

**建議**:
```markdown
### 代碼重複分析

#### 現有重複的評估代碼模式

**模式 1: 訓練-測試分割** (每個筆記本)
```python
# 現有代碼重複:
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)
accuracy_train = accuracy_score(y_train, y_pred_train)
accuracy_test = accuracy_score(y_test, y_pred_test)
```

**模式 2: 混淆矩陣** (每個筆記本)
```python
# 現有代碼重複:
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
```

**模式 3: ROC 曲線** (多個筆記本)
```python
# 現有代碼重複:
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.2f})')
```

#### 統一後的代碼
```python
from sources.model_evaluation import ModelEvaluator
evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)
evaluator.calculate_metrics()
evaluator.plot_confusion_matrix()
evaluator.plot_roc_curve()
```

**預計代碼減少**: 每個筆記本 40-50 行 (共 5 筆記本 = 200-250 行)
**改進**: ⭐ 在 scope 或 impact 中添加具體例子
```

---

### 6. 比較功能的目的不明確

**問題**: `compare_with()` 和 `plot_model_comparison()` 的典型用例不明確

**建議**:
```markdown
### 使用場景示例

#### 場景 1: 比較相同任務的不同算法
```python
# 垃圾短信檢測任務
evaluators = {
    'Bayesian': ModelEvaluator(bayes, X_train, y_train, X_test, y_test),
    'SVM': ModelEvaluator(svm, X_train, y_train, X_test, y_test),
    'Logistic': ModelEvaluator(lr, X_train, y_train, X_test, y_test)
}

# 生成對比報告
comparison = pd.DataFrame({
    name: eval.calculate_metrics() 
    for name, eval in evaluators.items()
})
```

#### 場景 2: 相同算法、不同數據集
```python
# 同一算法在不同任務上的性能
svm_spam = ModelEvaluator(svm_spam_model, ...)
svm_phish = ModelEvaluator(svm_phish_model, ...)
comparison = svm_spam.compare_with(svm_phish)
```

**改進**: ⭐ 在 spec.md 中添加真實場景示例
```

---

### 7. 測試覆蓋不明確

**位置**: tasks.md  
**問題**: Phase 1 說"寫單元測試"，但沒有說測試覆蓋率目標

**建議修改**:
```markdown
### Phase 1: Core Module (修訂)
- [ ] Create `sources/model_evaluation.py` with ModelEvaluator class
- [ ] Implement `__init__` method with input validation
- [ ] Implement `calculate_metrics()` returning dict
- [ ] **Write unit tests covering:**
  - ✓ Valid model and data inputs
  - ✓ Invalid inputs (wrong shapes, types)
  - ✓ Metrics match scikit-learn results
  - ✓ Binary and multi-class classification
  - **Target coverage: >85%**
```

**改進**: ⭐ 在 tasks.md 中詳細化測試要求

---

## 🟢 優點 (保留)

### ✅ 清晰的架構
- 模塊結構明確 (ModelEvaluator 類)
- 職責清晰 (計算、可視化、比較)

### ✅ 實用的 API 設計
- 簡單的初始化
- 直觀的方法名稱
- 返回標準數據結構

### ✅ 完整的階段計劃
- 5 個明確的實現階段
- 包含集成和文檔

### ✅ 低風險
- 沒有破壞性更改
- 向後相容

---

## 📋 改進清單

| 優先級 | 項目 | 文件位置 | 建議 |
|--------|------|---------|------|
| 🔴 高 | 數據集不一致 | proposal.md | 澄清數據集標準化策略 |
| 🔴 高 | 模型兼容性 | design.md | 添加模型兼容性檢查和錯誤處理 |
| 🔴 高 | 分類類型支援 | spec.md | 明確二分類/多類支援 |
| 🟡 中 | Linear Regression | proposal.md | 澄清是否包含 |
| 🟡 中 | 代碼重複示例 | scope | 添加具體減少代碼的例子 |
| 🟡 中 | 比較用例 | spec.md | 添加真實使用場景 |
| 🟡 中 | 測試覆蓋 | tasks.md | 明確測試目標 (>85%) |

---

## 建議改進行動

### 立即改進 (強烈建議)
1. ✏️ 在 proposal.md 中添加"數據集標準化"部分
2. ✏️ 在 design.md 中添加"模型兼容性"部分
3. ✏️ 在 spec.md 中詳細說明二分類/多類支援

### 後續改進 (應該做)
4. ✏️ 澄清 Linear Regression 是否包含
5. ✏️ 添加具體代碼重複減少的例子
6. ✏️ 添加真實比較場景

### 實現前檢查
7. ✅ 確認所有 5 個筆記本的數據集情況
8. ✅ 驗證模型是否都支援 predict_proba()
9. ✅ 檢查是否有多類分類場景

---

## 總結

提案的**核心思想很好**（統一評估框架），但需要在以下方面更明確：

1. **數據集管理**: 如何處理不同的輸入數據集
2. **模型支援**: 明確支持哪些模型類型
3. **分類支援**: 清楚地支援二分類還是多類
4. **實現細節**: 錯誤處理、驗證邏輯

建議在開始實現前解決這些問題，以確保實現符合預期。

---

**下一步**: 
- 是否需要我按上述建議修改這些檔案?
- 或者您想先討論這些澄清點?
