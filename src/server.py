import argparse
import logging
from mcp.server.fastmcp import FastMCP

from .config.settings import settings, configure_logging
from .service.stock_service import StockService
from .models.stock import PaginatedResponse
from .core.exceptions import StockException

# 初始化MCP服务器
mcp = FastMCP(settings.SERVICE_NAME)
logger = logging.getLogger(settings.SERVICE_NAME)

# 初始化服务实例
stock_service = StockService()

def handle_error(func):
    """统一异常处理装饰器"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except StockException as e:
            logger.error(f"业务错误: {str(e)}", exc_info=True)
            return {
                "error": e.code,
                "message": e.message,
                "details": e.details
            }
        except Exception as e:
            logger.error(f"系统错误: {str(e)}", exc_info=True)
            return {
                "error": "SYSTEM_ERROR",
                "message": "系统内部错误",
                "details": {"error": str(e)}
            }
    return wrapper

@mcp.tool('get_stock_info')
@handle_error
async def get_stock_info(stock_code: str, fromdate: str, todate: str):
    """获取股票历史数据"""
    return await stock_service.get_stock_history(stock_code, fromdate, todate)

@mcp.tool('get_stock_price_monthly')
@handle_error
async def get_stock_price_monthly(stock_code: str):
    """获取股票月度数据"""
    return await stock_service.get_stock_monthly_data(stock_code)

@mcp.tool('stock_individual_basic_info')
@handle_error
async def stock_individual_basic_info(stock_code: str):
    """获取股票基本信息"""
    return await stock_service.get_stock_basic_info(stock_code)

@mcp.tool('risk_stocks')
@handle_error
async def risk_stocks():
    """获取风险警示股票列表"""
    return await stock_service.get_risk_stocks()

@mcp.tool('stock_merito_data')
@handle_error
async def stock_merito_data(stock_code: str):
    """获取股票主营业务数据"""
    return await stock_service.get_stock_merito(stock_code)

@mcp.tool('get_stock_news')
@handle_error
async def get_stock_news(stock_code: str):
    """获取个股新闻"""
    return await stock_service.get_stock_news(stock_code)

@mcp.tool('get_finance_news')
@handle_error
async def get_finance_news(page: int = 1, page_size: int = None):
    """获取财经新闻"""
    result = await stock_service.get_finance_news(page, page_size)
    if isinstance(result, PaginatedResponse):
        return result.model_dump()
    return result

def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='股票数据服务')
    parser.add_argument(
        '--transport',
        choices=['stdio', 'http'],
        default=settings.TRANSPORT,
        help='传输协议: stdio(默认)或http'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=settings.HTTP_PORT,
        help=f'HTTP服务器端口(默认{settings.HTTP_PORT})'
    )
    parser.add_argument(
        '--log-level',
        choices=['debug', 'info', 'warning', 'error'],
        default=settings.LOG_LEVEL.lower(),
        help=f'日志级别(默认{settings.LOG_LEVEL.lower()})'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    settings.LOG_LEVEL = args.log_level.upper()
    configure_logging()
    
    try:
        logger.info("启动MCP服务...")
        if args.transport == 'http':
            mcp.run_http(port=args.port)
        else:
            mcp.run()
        logger.info("MCP服务启动成功")
    except Exception as e:
        logger.error(f"MCP服务启动失败: {e}")
        raise
