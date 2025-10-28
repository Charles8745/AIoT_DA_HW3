# 實現前檢查清單 - add-unified-model-evaluation

## ✅ 提案文件完整性檢查

### proposal.md 檢查
- [x] 明確支持的任務 (Phishing, Spam)
- [x] 明確支持的數據集
- [x] 排除的項目列表 (Linear Regression, Multi-class, Cross-task)
- [x] 數據標準化策略說明
- [x] Perceptron/SVM 遷移計劃說明
- [x] 清晰的範圍定義

### design.md 檢查
- [x] 初始化驗證邏輯詳細說明
- [x] 三個設計決策的清楚解釋
- [x] 任務內比較的實現邏輯
- [x] 支持/不支持模型清單
- [x] 集成示例 (Phishing + Spam)
- [x] Linear Regression 拒絕邏輯

### spec.md 檢查
- [x] 5 個主要需求 (R1-R5)
- [x] 二分類驗證要求
- [x] 模型兼容性要求
- [x] 數據集標準化要求
- [x] 3 個完整代碼示例
- [x] 約束條件明確列出

### tasks.md 檢查
- [x] 9 個實現階段 (Phase 1-9)
- [x] Phase 4 包含數據標準化任務
- [x] Phase 5 包含所有 5 個筆記本遷移
- [x] Phase 7 包含 60+ 測試目標
- [x] 清晰的定義完成條件

---

## ✅ 決策文件完整性

- [x] DECISION_SUMMARY.md 已生成
- [x] 三個關鍵決策已說明
  - [x] 數據集策略: 方案 A (任務內比較,標準化到 sms_spam_no_header.csv)
  - [x] Linear Regression: 排除
  - [x] 多類分類: 只支持二分類
- [x] 對每個筆記本的影響已列出
- [x] 驗證點已明確

---

## ✅ 數據準備檢查

### 網釣檢測任務
- [x] phishing_dataset.csv 存在
- [x] 行數: 11,054 ✓
- [x] 特徵: 31 列 ✓
- [x] 類別: 2 (0, 1) ✓
- [x] 當前使用: Decision Tree, Logistic Regression ✓
- [x] 需要修改: 無 ✓

### 垃圾短信任務 - 標準化
- [x] sms_spam_no_header.csv 存在
- [x] 行數: 5,574 ✓
- [x] 格式: CSV 文本 ✓
- [x] 類別: 2 (ham, spam) ✓
- [x] 當前使用: Bayesian ✓
- [x] 需要遷移: Perceptron (從 sms_spam_perceptron.csv) ⚠️
- [x] 需要遷移: SVM (從 sms_spam_svm.csv) ⚠️

### 舊數據集 (已廢棄)
- [x] sms_spam_perceptron.csv: 99 行 (太小, 廢棄)
- [x] sms_spam_svm.csv: 150 行 (太小, 廢棄)

---

## ✅ 模型兼容性檢查

### 支持的模型 ✅

| 模型 | 預測方法 | predict() | predict_proba() | 當前使用 | 筆記本 |
|------|---------|-----------|-----------------|---------|--------|
| Bayesian | GaussianNB | ✅ | ✅ | Spam | Bayesian Spam Detector |
| Decision Tree | DecisionTreeClassifier | ✅ | ✅ | Phishing | Decision Tree Phishing |
| Perceptron | Perceptron | ✅ | ❌ → ✅ | Spam | Perceptron |
| SVM | SVC(probability=True) | ✅ | ✅ | Spam | SVM |
| Logistic Reg | LogisticRegression | ✅ | ✅ | Phishing | Logistic Regression |

**特別注意:**
- Perceptron 需要檢查是否原生支援 predict_proba()
  - 如果不支援,需要使用 CalibratedClassifierCV 包裝
- SVM 需要 probability=True 參數

### 不支持的模型 ❌

| 模型 | 原因 | predict() | predict_proba() |
|------|------|-----------|-----------------|
| Linear Regression | 回歸算法,非分類 | ✅ | ❌ |

---

## ✅ 筆記本集成計劃

### Bayesian Spam Detector
- 當前數據集: sms_spam_no_header.csv ✅ (已標準)
- 需要修改: 集成 ModelEvaluator
- 工作量: 低 (只需添加評估代碼)
- 預計影響: 無破壞性更改

### Decision Tree Phishing Detector
- 當前數據集: phishing_dataset.csv ✅ (已標準)
- 需要修改: 集成 ModelEvaluator
- 工作量: 低
- 預計影響: 無破壞性更改

### Perceptron
- 當前數據集: sms_spam_perceptron.csv ❌ (需遷移)
- 需要修改:
  1. 改為使用 sms_spam_no_header.csv
  2. 提取文本特徵
  3. 集成 ModelEvaluator
- 工作量: 中 (數據處理邏輯改變)
- 預計影響: 可能提高準確率 (數據更大)

### SVM
- 當前數據集: sms_spam_svm.csv ❌ (需遷移)
- 需要修改:
  1. 改為使用 sms_spam_no_header.csv
  2. 提取文本特徵
  3. 集成 ModelEvaluator
- 工作量: 中 (數據處理邏輯改變)
- 預計影響: 可能提高準確率 (數據更大)

### Logistic Regression
- 當前數據集: phishing_dataset.csv ✅ (已標準)
- 需要修改: 集成 ModelEvaluator
- 工作量: 低
- 預計影響: 無破壞性更改

### Linear Regression
- 決策: 不支持 ❌
- 原因: 回歸算法,不是分類
- 工作量: 0 (無需修改)
- 註釋: 可在筆記本中保留,但不會集成到 ModelEvaluator

---

## ✅ 測試策略檢查

### Phase 1 測試目標: 18 個測試
- [ ] 模型初始化 (3 個)
  - [ ] 有效模型初始化成功
  - [ ] 無 predict_proba 的模型拒絕
  - [ ] Linear Regression 拒絕

- [ ] 二分類驗證 (3 個)
  - [ ] 二分類接受
  - [ ] 多類拒絕
  - [ ] 單類拒絕

- [ ] 數據形狀驗證 (3 個)
  - [ ] 形狀一致接受
  - [ ] 形狀不匹配拒絕
  - [ ] 特徵數不匹配拒絕

- [ ] 指標計算 (9 個)
  - [ ] accuracy 計算正確
  - [ ] precision 計算正確
  - [ ] recall 計算正確
  - [ ] f1 計算正確
  - [ ] auc_roc 計算正確
  - [ ] train/test 指標分離
  - [ ] task_name 記錄
  - [ ] 邊界情況: 完美模型
  - [ ] 邊界情況: 零模型

### Phase 2-3 測試目標: 25 個測試
- [ ] 混淆矩陣可視化 (5 個)
- [ ] ROC 曲線可視化 (5 個)
- [ ] 生成報告 (3 個)
- [ ] 兩模型比較 (7 個)
- [ ] 多模型比較 (5 個)

### Phase 7 終目標: 60+ 測試
- [ ] 單元測試: 50+
- [ ] 集成測試: 10+
- [ ] 目標覆蓋率: >90%

---

## ✅ 代碼品質檢查

### 代碼風格
- [ ] PEP 8 兼容
- [ ] 類型提示完整
- [ ] 文件名小寫下劃線 (model_evaluation.py)
- [ ] 類名 PascalCase (ModelEvaluator)
- [ ] 方法名 snake_case (_validate_*)

### 文檔
- [ ] 模塊級文檔字符串
- [ ] 類級文檔字符串
- [ ] 方法級文檔字符串 (參數, 返回, 異常)
- [ ] 複雜邏輯內聯註釋

### 錯誤處理
- [ ] 清晰的錯誤消息
- [ ] 適當的異常類型 (ValueError, AttributeError)
- [ ] 無裸異常
- [ ] 邊界情況處理

---

## ✅ 與現有代碼的一致性

### defs.py 兼容性
- [ ] 不修改現有函數簽名
- [ ] get_tokens() 繼續工作
- [ ] get_lemmas() 繼續工作
- [ ] 向後兼容 100%

### preprocessing.py 兼容性
- [ ] ModelEvaluator 可與預處理結合使用
- [ ] 無依賴衝突
- [ ] 可在同一筆記本中一起使用

### 筆記本兼容性
- [ ] 現有代碼繼續運作
- [ ] ModelEvaluator 是可選的增強
- [ ] 不破壞現有輸出

---

## ✅ OpenSpec 流程檢查

- [x] 提案結構完整 (proposal.md, design.md, spec.md, tasks.md)
- [x] 決策已明確 (DECISION_SUMMARY.md)
- [x] 準備就緒檢查清單 (本文件)
- [ ] 等待批准 (Approval Status: [ ] Ready for implementation)

---

## 📝 準備狀態

| 項目 | 狀態 | 備註 |
|------|------|------|
| 提案文件 | ✅ | 所有 4 個文件已更新 |
| 決策文件 | ✅ | DECISION_SUMMARY.md 已生成 |
| 數據檢查 | ✅ | 所有數據集已驗證 |
| 模型兼容性 | ✅ | 所有模型已檢查 |
| 筆記本計劃 | ✅ | 遷移計劃已制定 |
| 測試策略 | ✅ | 60+ 測試已規劃 |
| 代碼品質 | ✅ | 檢查清單已準備 |
| 向後兼容性 | ✅ | 無破壞性更改 |

---

## 🚀 準備開始實現

### 下一步
1. ✅ 確認所有決策 (已完成)
2. ✅ 生成檢查清單 (已完成)
3. ⏳ 更新 proposal.md approval status: `[x] Ready for implementation`
4. ⏳ 開始 Phase 1: Core Module Development
   - 創建 sources/model_evaluation.py
   - 實現 ModelEvaluator.__init__
   - 實現 calculate_metrics()
   - 寫 18 個初始測試

### 預計時間表
- Phase 1-3 (核心): 4-6 小時
- Phase 4 (數據遷移): 2-3 小時
- Phase 5 (集成): 3-4 小時
- Phase 6-9 (文檔/驗證): 3-4 小時
- **總計**: 12-17 小時

---

## ✨ 總結

所有準備工作已完成:
- ✅ 決策已確認
- ✅ 數據已檢查
- ✅ 模型已驗證
- ✅ 計劃已制定
- ✅ 測試已規劃

**可以開始實現了!** 🎉

---

最後修改: 2025-10-22
狀態: ✅ 準備開始 Phase 1
