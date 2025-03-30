from typing import Dict, List, Union
import akshare as ak
import datetime
import logging
from functools import wraps

logger = logging.getLogger('stock-utils')

def handle_stock_errors(func):
    """装饰器：统一处理股票数据获取错误"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"股票数据操作失败: {e}")
            return {
                "error": str(e),
                "message": "股票数据操作失败，请检查参数"
            }
    return wrapper

def format_date(date: Union[str, datetime.datetime]) -> str:
    """统一格式化日期为YYYYMMDD格式"""
    if isinstance(date, datetime.datetime):
        return date.strftime('%Y%m%d')
    return date

def get_date_range(days: int = 30) -> tuple[str, str]:
    """获取日期范围，默认最近30天"""
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    return format_date(start_date), format_date(end_date)

class StockDataFetcher:
    """股票数据获取工具类"""
    
    @staticmethod
    @handle_stock_errors
    async def get_history_data(
        stock_code: str, 
        start_date: str, 
        end_date: str,
        period: str = "daily"
    ) -> List[Dict]:
        """获取股票历史数据"""
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        return df.to_dict(orient='records')
    
    @staticmethod
    @handle_stock_errors
    async def get_basic_info(stock_code: str) -> List[Dict]:
        """获取股票基本信息"""
        df = ak.stock_individual_info_em(symbol=stock_code)
        return df.to_dict(orient='records')
    
    @staticmethod
    @handle_stock_errors
    async def get_risk_stocks() -> List[Dict]:
        """获取风险警示股票"""
        df = ak.stock_zh_a_st_em()
        return df.to_dict(orient='records')
    
    @staticmethod
    @handle_stock_errors
    async def get_merito_data(stock_code: str) -> List[Dict]:
        """获取股票主营介绍数据"""
        df = ak.stock_zyjs_ths(symbol=stock_code)
        return df.to_dict(orient='records')

    @staticmethod
    @handle_stock_errors
    async def get_news(stock_code: str) -> List[Dict]:
        """获取个股新闻数据"""
        df = ak.stock_news_em(symbol=stock_code)
        return df.to_dict(orient='records')
    
    @staticmethod
    @handle_stock_errors
    async def get_finance_news() -> List[Dict]:
        """获取财经新闻数据"""
        df = ak.stock_news_main_cx()
        return df.to_dict(orient='records')