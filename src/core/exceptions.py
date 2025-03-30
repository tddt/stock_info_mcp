from typing import Optional, Any, Dict

class StockException(Exception):
    """股票服务基础异常类"""
    def __init__(
        self,
        message: str,
        code: str = "STOCK_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)

class StockNotFoundError(StockException):
    """股票不存在异常"""
    def __init__(self, stock_code: str):
        super().__init__(
            message=f"股票代码 {stock_code} 不存在",
            code="STOCK_NOT_FOUND",
            details={"stock_code": stock_code}
        )

class InvalidDateFormatError(StockException):
    """日期格式错误异常"""
    def __init__(self, date: str):
        super().__init__(
            message=f"日期格式错误: {date}，应为YYYYMMDD格式",
            code="INVALID_DATE_FORMAT",
            details={"date": date}
        )

class StockDataFetchError(StockException):
    """股票数据获取错误异常"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="DATA_FETCH_ERROR",
            details=details
        )

class InvalidPaginationError(StockException):
    """分页参数错误异常"""
    def __init__(self, page: int, page_size: int):
        super().__init__(
            message="分页参数错误",
            code="INVALID_PAGINATION",
            details={"page": page, "page_size": page_size}
        )
