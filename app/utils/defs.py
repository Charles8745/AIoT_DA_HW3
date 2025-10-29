"""實用工具函數。

包含文本處理、可視化和相容性函數。

Module contents:
    - 文本預處理: get_tokens(), get_lemmas()
    - 新增預處理: 來自 preprocessing 模組的橋接函數
    - 可視化: plot_decision_regions()
    - 工具: versiontuple()
"""

from textblob import TextBlob
import re

# ==================== 原始文本處理函數 ====================

def get_tokens(msg):
    """獲取文本的標記 (tokens)。
    
    使用簡單的正規表達式和空白分割。
    
    Args:
        msg: 輸入文本
    
    Returns:
        標記列表
    
    Example:
        >>> tokens = get_tokens("Hello world!")
        >>> print(tokens)
        ['Hello', 'world']
    """
    # 使用簡單方法：移除非字母數字，然後分割
    text = str(msg).lower()
    # 移除標點符號，保留字母和數字
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # 分割並移除空白
    tokens = [t for t in text.split() if t.strip()]
    return tokens


def get_lemmas(msg):
    """獲取文本的詞根 (lemmas)。
    
    簡化版本：直接返回小寫的標記
    (完整版本可使用 TextBlob 或 NLTK)
    
    Args:
        msg: 輸入文本
    
    Returns:
        詞根列表
    
    Example:
        >>> lemmas = get_lemmas("Running quickly")
        >>> print(lemmas)
        ['running', 'quickly']
    """
    # 簡化版本：使用 get_tokens 並轉換為小寫
    # 完整版本可在此使用 TextBlob 的 lemma 功能
    return get_tokens(msg)


# ==================== 橋接函數 (新預處理模組) ====================

def get_preprocessor(config=None):
    """獲取文本預處理器。
    
    這是使用新預處理模組的橋接函數。允許
    現有代碼無縫遷移到新的預處理系統。
    
    Args:
        config: 預處理配置。如果為 None，使用預設配置。
    
    Returns:
        TextPreprocessor 實例
    
    Example:
        >>> preprocessor = get_preprocessor()
        >>> cleaned = preprocessor.process("Visit http://example.com")
        >>> print(cleaned)
        'visit example com'
    """
    try:
        from preprocessing import TextPreprocessor, PreprocessingConfig
        if config is None:
            config = PreprocessingConfig()
        return TextPreprocessor(config)
    except ImportError:
        # 備用方案：返回 None，讓調用者知道模組不可用
        return None


def preprocess_aggressive(text):
    """使用積極預處理清理文本。
    
    這是使用新預處理模組的便利函數。
    移除 URLs、emails、標點、停用詞等。
    
    Args:
        text: 輸入文本
    
    Returns:
        清理後的文本
    
    Example:
        >>> text = "Visit http://SPAM.com!!! Or email admin@fake.net"
        >>> print(preprocess_aggressive(text))
        'visit spam com email admin fake'
    """
    try:
        from preprocessing import preprocess_text, get_aggressive_config
        config = get_aggressive_config()
        return preprocess_text(text, config)
    except ImportError:
        # 備用方案：使用原始方法
        from textblob import TextBlob
        text = TextBlob(str(text)).lower()
        return ' '.join([word.lemma for word in text.words])


def preprocess_conservative(text):
    """使用保守預處理清理文本。
    
    這是使用新預處理模組的便利函數。
    只移除 URLs、emails 和空白。
    
    Args:
        text: 輸入文本
    
    Returns:
        清理後的文本
    
    Example:
        >>> text = "Visit http://example.com for DEALS!!!"
        >>> print(preprocess_conservative(text))
        'Visit for DEALS'
    """
    try:
        from preprocessing import preprocess_text, get_conservative_config
        config = get_conservative_config()
        return preprocess_text(text, config)
    except ImportError:
        # 備用方案：只移除 URLs/emails
        import re
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', text)
        return text


# ==================== 可視化函數 ====================

# 感謝 Sebastian Raschka 提供的 plot_decision_regions
# https://github.com/rasbt/python-machine-learning-book

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import warnings

def versiontuple(v):
    """將版本字串轉換為元組。
    
    Args:
        v: 版本字串 (e.g., "1.9.0")
    
    Returns:
        整數元組 (e.g., (1, 9, 0))
    """
    return tuple(map(int, (v.split("."))))

def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    """繪製分類器的決策邊界。
    
    使用網格搜索為二維特徵可視化分類器的決策區域。
    
    Args:
        X: 特徵矩陣 (N x 2)
        y: 標籤向量 (N,)
        classifier: 訓練過的分類器物件 (需具有 predict 方法)
        test_idx: 測試集索引 (可選)
        resolution: 網格解析度 (預設: 0.02)
    
    Returns:
        None (直接繪製到 matplotlib 圖表)
    
    Example:
        >>> plot_decision_regions(X_train, y_train, classifier, test_idx=test_indices)
    """

    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=cmap(idx),
                    marker=markers[idx], label=cl)

    # highlight test samples
    if test_idx:
        # plot all samples
        if not versiontuple(np.__version__) >= versiontuple('1.9.0'):
            X_test, y_test = X[list(test_idx), :], y[list(test_idx)]
            warnings.warn('Please update to NumPy 1.9.0 or newer')
        else:
            X_test, y_test = X[test_idx, :], y[test_idx]

        plt.scatter(X_test[:, 0],
                    X_test[:, 1],
                    c='',
                    alpha=1.0,
                    linewidths=1,
                    marker='o',
                    s=55, label='test set')

