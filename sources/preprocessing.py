"""文本預處理和特徵工程模組。

提供文本清理、正規化和特徵提取的標準化功能。
用於垃圾短信檢測和網釣郵件分類任務。

Module Structure:
    - PreprocessingConfig: 預處理配置資料類
    - TextPreprocessor: 主要文本預處理類
    - 獨立預處理函數: 各個預處理步驟

Author:
    AIoT_DA_HW3 Team
    Enhanced preprocessing module (2025-10-22)

References:
    - NLTK: Natural Language Toolkit (stopwords)
    - TextBlob: Simple API for text processing
    
Example:
    >>> from sources.preprocessing import TextPreprocessor, PreprocessingConfig
    >>> config = PreprocessingConfig(remove_stopwords=True)
    >>> preprocessor = TextPreprocessor(config)
    >>> text = "Visit http://spam.com!!! Contact: spam@fake.net"
    >>> cleaned = preprocessor.process(text)
    >>> print(cleaned)
    'visit spam com contact'
"""

import re
import warnings
from dataclasses import dataclass
from typing import List, Optional, Union

import nltk
from nltk.corpus import stopwords

# 英文停用詞 (離線版本，避免 SSL/網路問題)
ENGLISH_STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an',
    'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before',
    'being', 'below', 'between', 'both', 'but', 'by', 'can', 'could', 'did',
    'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from',
    'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers',
    'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is',
    'it', 'its', 'itself', 'just', 'me', 'might', 'more', 'most', 'my', 'myself',
    'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our',
    'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 'so',
    'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves',
    'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where',
    'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours',
    'yourself', 'yourselves'
}

# 嘗試從 NLTK 載入停用詞，失敗時使用離線版本
def _load_stopwords():
    """載入停用詞，優先使用 NLTK，失敗時使用內置版本。"""
    try:
        nltk.data.find('corpora/stopwords')
        return set(stopwords.words('english'))
    except (LookupError, Exception):
        # 嘗試下載（某些環境可能成功）
        try:
            nltk.download('stopwords', quiet=True)
            return set(stopwords.words('english'))
        except Exception:
            # 使用離線版本
            return ENGLISH_STOPWORDS


@dataclass
class PreprocessingConfig:
    """文本預處理配置。
    
    Attributes:
        lowercase (bool): 是否轉換為小寫。預設: True
        remove_urls (bool): 是否移除 URLs。預設: True
        remove_emails (bool): 是否移除電郵地址。預設: True
        remove_punctuation (bool): 是否移除標點符號。預設: True
        remove_numbers (bool): 是否移除數字。預設: False
        remove_stopwords (bool): 是否移除停用詞。預設: False
        normalize_whitespace (bool): 是否正規化空白。預設: True
        remove_non_ascii (bool): 是否移除非 ASCII 字符。預設: True
    
    Example:
        >>> config = PreprocessingConfig(
        ...     lowercase=True,
        ...     remove_urls=True,
        ...     remove_stopwords=True
        ... )
    """
    lowercase: bool = True
    remove_urls: bool = True
    remove_emails: bool = True
    remove_punctuation: bool = True
    remove_numbers: bool = False
    remove_stopwords: bool = False
    normalize_whitespace: bool = True
    remove_non_ascii: bool = True


class TextPreprocessor:
    """文本預處理管道。
    
    提供配置驅動的文本預處理功能。支援多個預處理步驟的
    靈活組合，適應不同的分析任務。
    
    Attributes:
        config (PreprocessingConfig): 預處理配置
        stopwords_set (set): 英文停用詞集合
    
    Example:
        >>> preprocessor = TextPreprocessor()
        >>> text = "Hello!!! Visit http://example.com or email test@example.com"
        >>> cleaned = preprocessor.process(text)
        >>> print(cleaned)
        'hello visit example com or email test example com'
    """
    
    def __init__(self, config: Optional[PreprocessingConfig] = None):
        """初始化文本預處理器。
        
        Args:
            config: 預處理配置。如果為 None，使用預設配置。
        
        Raises:
            TypeError: 如果 config 不是 PreprocessingConfig 類型。
        """
        if config is None:
            config = PreprocessingConfig()
        elif not isinstance(config, PreprocessingConfig):
            raise TypeError(f"config 必須是 PreprocessingConfig 類型，得到 {type(config)}")
        
        self.config = config
        
        # 載入停用詞 (使用改進的載入器)
        self.stopwords_set = _load_stopwords()
    
    def remove_urls(self, text: str) -> str:
        """移除文本中的 URLs。
        
        移除 http、https、ftp 等協議的 URLs。
        
        Args:
            text: 輸入文本
        
        Returns:
            移除 URLs 後的文本
        
        Example:
            >>> processor = TextPreprocessor()
            >>> processor.remove_urls("Visit http://example.com today")
            'Visit  today'
        """
        # 移除 http/https/ftp URLs (case-insensitive)
        url_pattern = r'(?:http|https|ftp)[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        text = re.sub(url_pattern, '', text, flags=re.IGNORECASE)
        # 移除 www. URLs
        www_pattern = r'www\.[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}'
        text = re.sub(www_pattern, '', text, flags=re.IGNORECASE)
        return text
    
    def remove_emails(self, text: str) -> str:
        """移除文本中的電郵地址。
        
        移除標準格式的電郵地址 (user@domain.com)。
        
        Args:
            text: 輸入文本
        
        Returns:
            移除電郵後的文本
        
        Example:
            >>> processor = TextPreprocessor()
            >>> processor.remove_emails("Contact: john@example.com")
            'Contact: '
        """
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.sub(email_pattern, '', text)
    
    def remove_punctuation(self, text: str) -> str:
        """移除文本中的標點符號。
        
        移除常見的標點符號，但保留空格和字母數字。
        
        Args:
            text: 輸入文本
        
        Returns:
            移除標點後的文本
        
        Example:
            >>> processor = TextPreprocessor()
            >>> processor.remove_punctuation("Hello!!! How are you???")
            'Hello How are you'
        """
        # 移除標點符號，但保留空格
        punctuation_pattern = r'[^\w\s]'
        return re.sub(punctuation_pattern, '', text)
    
    def remove_numbers(self, text: str) -> str:
        """移除文本中的數字。
        
        移除所有數字字符 (0-9)。
        
        Args:
            text: 輸入文本
        
        Returns:
            移除數字後的文本
        
        Example:
            >>> processor = TextPreprocessor()
            >>> processor.remove_numbers("Call 555-1234 or 100 items")
            'Call  or  items'
        """
        return re.sub(r'\d+', '', text)
    
    def normalize_whitespace(self, text: str) -> str:
        """正規化空白字符。
        
        移除多餘的空格、換行符和制表符。
        
        Args:
            text: 輸入文本
        
        Returns:
            正規化後的文本
        
        Example:
            >>> processor = TextPreprocessor()
            >>> processor.normalize_whitespace("Hello    world\\n\\nTest")
            'Hello world Test'
        """
        # 移除換行符和制表符
        text = re.sub(r'[\n\r\t]+', ' ', text)
        # 移除多餘的空格
        text = re.sub(r'\s+', ' ', text)
        # 移除首尾空格
        return text.strip()
    
    def normalize_case(self, text: str) -> str:
        """正規化大小寫。
        
        將文本轉換為小寫。
        
        Args:
            text: 輸入文本
        
        Returns:
            小寫文本
        
        Example:
            >>> processor = TextPreprocessor()
            >>> processor.normalize_case("Hello WORLD")
            'hello world'
        """
        return text.lower()
    
    def remove_non_ascii(self, text: str) -> str:
        """移除非 ASCII 字符。
        
        移除所有非 ASCII 字符（例如特殊符號、外語字符）。
        
        Args:
            text: 輸入文本
        
        Returns:
            移除非 ASCII 字符後的文本
        
        Example:
            >>> processor = TextPreprocessor()
            >>> processor.remove_non_ascii("Hello café")
            'Hello caf'
        """
        return ''.join(char for char in text if ord(char) < 128)
    
    def remove_stopwords(self, text: str) -> str:
        """移除停用詞。
        
        移除常見的英文停用詞 (the, a, is 等)。
        需要先進行標記化。
        
        Args:
            text: 輸入文本（單詞之間以空格分隔）
        
        Returns:
            移除停用詞後的文本
        
        Example:
            >>> processor = TextPreprocessor()
            >>> processor.remove_stopwords("the quick brown fox")
            'quick brown fox'
        """
        if not self.stopwords_set:
            warnings.warn("停用詞集合為空，無法移除停用詞")
            return text
        
        words = text.split()
        filtered_words = [
            word for word in words 
            if word.lower() not in self.stopwords_set
        ]
        return ' '.join(filtered_words)
    
    def process(self, text: Union[str, int, float]) -> str:
        """執行完整的預處理管道。
        
        按照最佳順序執行配置中指定的預處理步驟：
        1. URL/Email 移除
        2. 大小寫正規化
        3. 標點符號移除
        4. 數字移除 (可選)
        5. 空白正規化
        6. 非 ASCII 移除
        7. 停用詞移除 (可選)
        
        Args:
            text: 輸入文本。支援字串、整數或浮點數。
        
        Returns:
            預處理後的文本
        
        Raises:
            ValueError: 如果輸入為 None
            TypeError: 如果輸入類型不支援
        
        Example:
            >>> config = PreprocessingConfig(remove_stopwords=True)
            >>> processor = TextPreprocessor(config)
            >>> text = "Visit http://spam.com!!! Contact: spam@fake.net"
            >>> processor.process(text)
            'visit spam com contact'
        """
        # 輸入驗證
        if text is None:
            raise ValueError("輸入文本不能為 None")
        
        # 轉換為字串
        try:
            text = str(text)
        except Exception as e:
            raise TypeError(f"無法將輸入轉換為字串: {e}") from e
        
        # 執行預處理管道
        try:
            # 1. URL/Email 移除
            if self.config.remove_urls:
                text = self.remove_urls(text)
            if self.config.remove_emails:
                text = self.remove_emails(text)
            
            # 2. 大小寫正規化
            if self.config.lowercase:
                text = self.normalize_case(text)
            
            # 3. 標點符號移除
            if self.config.remove_punctuation:
                text = self.remove_punctuation(text)
            
            # 4. 數字移除
            if self.config.remove_numbers:
                text = self.remove_numbers(text)
            
            # 5. 空白正規化
            if self.config.normalize_whitespace:
                text = self.normalize_whitespace(text)
            
            # 6. 非 ASCII 移除
            if self.config.remove_non_ascii:
                text = self.remove_non_ascii(text)
            
            # 7. 停用詞移除 (在最後，因為需要標記化)
            if self.config.remove_stopwords:
                text = self.remove_stopwords(text)
            
            return text
        
        except Exception as e:
            raise RuntimeError(f"預處理失敗: {e}") from e
    
    def batch_process(self, texts: List[Union[str, int, float]]) -> List[str]:
        """批量預處理文本。
        
        對多個文本執行相同的預處理管道。
        
        Args:
            texts: 文本列表
        
        Returns:
            預處理後的文本列表
        
        Raises:
            ValueError: 如果輸入為 None 或空列表
            TypeError: 如果輸入不是列表
        
        Example:
            >>> processor = TextPreprocessor()
            >>> texts = ["Visit http://example.com", "Check spam@test.net"]
            >>> processor.batch_process(texts)
            ['visit example com', 'check spam test net']
        """
        if texts is None:
            raise ValueError("輸入文本列表不能為 None")
        
        if not isinstance(texts, (list, tuple)):
            raise TypeError(f"輸入必須是列表或元組，得到 {type(texts)}")
        
        if len(texts) == 0:
            raise ValueError("輸入文本列表不能為空")
        
        return [self.process(text) for text in texts]


# ==================== 便利函數 ====================

def preprocess_text(
    text: Union[str, int, float],
    config: Optional[PreprocessingConfig] = None
) -> str:
    """快速預處理文本的便利函數。
    
    使用指定的配置預處理單個文本。
    
    Args:
        text: 輸入文本
        config: 預處理配置。如果為 None，使用預設配置。
    
    Returns:
        預處理後的文本
    
    Example:
        >>> preprocess_text("Visit HTTP://EXAMPLE.COM!!!")
        'visit example com'
    """
    if config is None:
        config = PreprocessingConfig()
    
    preprocessor = TextPreprocessor(config)
    return preprocessor.process(text)


def get_default_config() -> PreprocessingConfig:
    """獲取預設的預處理配置。
    
    Returns:
        預設配置物件
    
    Example:
        >>> config = get_default_config()
        >>> print(config.remove_stopwords)
        False
    """
    return PreprocessingConfig()


def get_aggressive_config() -> PreprocessingConfig:
    """獲取積極的預處理配置 (移除更多內容)。
    
    適用於需要高度清理文本的情況。
    
    Returns:
        積極配置物件 (移除停用詞、數字等)
    
    Example:
        >>> config = get_aggressive_config()
        >>> processor = TextPreprocessor(config)
    """
    return PreprocessingConfig(
        lowercase=True,
        remove_urls=True,
        remove_emails=True,
        remove_punctuation=True,
        remove_numbers=True,
        remove_stopwords=True,
        normalize_whitespace=True,
        remove_non_ascii=True
    )


def get_conservative_config() -> PreprocessingConfig:
    """獲取保守的預處理配置 (移除較少內容)。
    
    適用於需要保留更多原始資訊的情況。
    
    Returns:
        保守配置物件 (只移除 URLs、emails、空白)
    
    Example:
        >>> config = get_conservative_config()
        >>> processor = TextPreprocessor(config)
    """
    return PreprocessingConfig(
        lowercase=False,
        remove_urls=True,
        remove_emails=True,
        remove_punctuation=False,
        remove_numbers=False,
        remove_stopwords=False,
        normalize_whitespace=True,
        remove_non_ascii=False
    )
