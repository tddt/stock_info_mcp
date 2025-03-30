from typing import List, Dict, Optional
import akshare as ak
import pandas as pd
from datetime import datetime
from functools import wraps

from src.core.exceptions import StockDataFetchError, StockNotFoundError
from src.models.stock import StockPrice, StockBasicInfo, StockNews, FinanceNews

class StockRepository:
    """股票数据仓库，负责数据访问层"""

    @staticmethod
    def handle_fetch_error(func):
        """处理数据获取错误的装饰器"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                raise StockDataFetchError(str(e), details=kwargs)
        return wrapper

    @staticmethod
    def _convert_to_records(df: pd.DataFrame) -> List[Dict]:
        """转换DataFrame为字典列表"""
        if df.empty:
            return []
        return df.to_dict(orient='records')

    @handle_fetch_error
    async def get_stock_history(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        period: str = "daily"
    ) -> List[StockPrice]:
        """获取股票历史数据"""
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        if df.empty:
            raise StockNotFoundError(stock_code)
        
        records = self._convert_to_records(df)
        # 限制返回最近90天的数据
        return [StockPrice(**record) for record in records[-90:]]

    @handle_fetch_error
    async def get_stock_basic_info(self, stock_code: str) -> StockBasicInfo:
        """获取股票基本信息"""
        df = ak.stock_individual_info_em(symbol=stock_code)
        if df.empty:
            raise StockNotFoundError(stock_code)
        
        info_dict = self._convert_to_records(df)[0]
        return StockBasicInfo(**info_dict)

    @handle_fetch_error
    async def get_risk_stocks(self) -> List[StockBasicInfo]:
        """获取风险警示股票列表"""
        df = ak.stock_zh_a_st_em()
        records = self._convert_to_records(df)
        # 限制返回数量，避免数据过大
        return [StockBasicInfo(**record) for record in records[:100]]

    @handle_fetch_error
    async def get_stock_news(self, stock_code: str) -> List[StockNews]:
        """获取个股新闻"""
        df = ak.stock_news_em(symbol=stock_code)
        if df.empty:
            return []
        
        records = self._convert_to_records(df)
        # 限制返回数量，避免数据过大
        return [StockNews(**record) for record in records[:20]]

    @handle_fetch_error
    async def get_finance_news(self) -> List[FinanceNews]:
        """获取财经新闻"""
        df = ak.stock_news_main_cx()
        records = self._convert_to_records(df)
        # 限制返回数量，避免数据过大
        return [FinanceNews(**record) for record in records[:50]]

    @handle_fetch_error
    async def get_stock_merito(self, stock_code: str) -> Dict:
        """获取股票主营业务信息"""
        df = ak.stock_zyjs_ths(symbol=stock_code)
        if df.empty:
            raise StockNotFoundError(stock_code)
        return self._convert_to_records(df)[0]
