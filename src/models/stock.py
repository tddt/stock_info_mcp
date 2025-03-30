from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StockPrice(BaseModel):
    """股票价格数据模型"""
    date: str
    open: float
    close: float
    high: float
    low: float
    volume: float
    amount: float

class StockBasicInfo(BaseModel):
    """股票基本信息数据模型"""
    code: str
    name: str
    industry: Optional[str]
    area: Optional[str]
    market: Optional[str]

class StockNews(BaseModel):
    """股票新闻数据模型"""
    title: str
    content: str
    date: datetime
    source: Optional[str]

class FinanceNews(BaseModel):
    """财经新闻数据模型"""
    title: str
    content: str
    date: datetime
    source: Optional[str]

class PaginationInfo(BaseModel):
    """分页信息模型"""
    total: int
    page: int
    page_size: int
    total_pages: int

class PaginatedResponse(BaseModel):
    """分页响应模型"""
    data: List
    pagination: PaginationInfo
