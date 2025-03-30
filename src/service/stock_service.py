from datetime import datetime, timedelta
from typing import List, Dict, Optional

from src.config.settings import settings
from src.core.exceptions import InvalidPaginationError, InvalidDateFormatError
from src.models.stock import (
    StockPrice, StockBasicInfo, StockNews,
    FinanceNews, PaginationInfo, PaginatedResponse
)
from src.repository.stock_repository import StockRepository

class StockService:
    """股票服务类，处理业务逻辑"""

    def __init__(self, repository: Optional[StockRepository] = None):
        """初始化服务，支持依赖注入"""
        self.repository = repository or StockRepository()

    def _validate_date_format(self, date: str) -> bool:
        """验证日期格式是否正确"""
        try:
            datetime.strptime(date, '%Y%m%d')
            return True
        except ValueError:
            raise InvalidDateFormatError(date)

    def _get_date_range(self, days: int = None) -> tuple[str, str]:
        """获取日期范围"""
        days = days or settings.DEFAULT_HISTORY_DAYS
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d')

    def _paginate_data(self, data: List, page: int, page_size: int) -> PaginatedResponse:
        """对数据进行分页处理"""
        if page < 1 or page_size < 1:
            raise InvalidPaginationError(page, page_size)

        total = len(data)
        start = (page - 1) * page_size
        end = start + page_size

        return PaginatedResponse(
            data=data[start:end],
            pagination=PaginationInfo(
                total=total,
                page=page,
                page_size=page_size,
                total_pages=(total + page_size - 1) // page_size
            )
        )

    async def get_stock_history(
        self,
        stock_code: str,
        start_date: str,
        end_date: str
    ) -> List[StockPrice]:
        """获取股票历史数据"""
        self._validate_date_format(start_date)
        self._validate_date_format(end_date)
        return await self.repository.get_stock_history(stock_code, start_date, end_date)

    async def get_stock_monthly_data(self, stock_code: str) -> List[StockPrice]:
        """获取股票月度数据"""
        start_date, end_date = self._get_date_range()
        return await self.repository.get_stock_history(stock_code, start_date, end_date)

    async def get_stock_basic_info(self, stock_code: str) -> StockBasicInfo:
        """获取股票基本信息"""
        return await self.repository.get_stock_basic_info(stock_code)

    async def get_risk_stocks(self) -> List[StockBasicInfo]:
        """获取风险警示股票"""
        return await self.repository.get_risk_stocks()

    async def get_stock_news(self, stock_code: str) -> List[StockNews]:
        """获取个股新闻"""
        return await self.repository.get_stock_news(stock_code)

    async def get_finance_news(
        self,
        page: int = 1,
        page_size: int = None
    ) -> PaginatedResponse:
        """获取财经新闻（分页）"""
        page_size = page_size or settings.DEFAULT_PAGE_SIZE
        news_list = await self.repository.get_finance_news()
        return self._paginate_data(news_list, page, page_size)

    async def get_stock_merito(self, stock_code: str) -> Dict:
        """获取股票主营业务信息"""
        return await self.repository.get_stock_merito(stock_code)
