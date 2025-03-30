from mcp.server.fastmcp import FastMCP
from stock_utils import StockDataFetcher, format_date, get_date_range
import datetime
import logging
import argparse
from typing import Dict, List

# 初始化MCP和日志
mcp = FastMCP('stock-info')
 
logger = logging.getLogger('stock-info')

@mcp.tool('get_stock_info')
async def get_stock_info(stock_code: str, fromdate: str, todate: str) -> Dict:
    '''
    获取指定股票代码、指定日期范围的股价信息
    :param stock_code: 股票代码 (如: '601890')
    :param fromdate: 开始日期 (格式: YYYYMMDD)
    :param todate: 结束日期 (格式: YYYYMMDD)
    :return: 股价信息列表或错误信息
    '''
    return await StockDataFetcher.get_history_data(
        stock_code=stock_code,
        start_date=format_date(fromdate),
        end_date=format_date(todate)
    )

@mcp.tool('get_stock_price_monthly')
async def get_stock_price_monthly(stock_code: str) -> Dict:
    '''
    获取指定股票代码的最近30天的股价信息
    :param stock_code: 股票代码
    :return: 股价信息列表或错误信息
    '''
    start_date, end_date = get_date_range(30)
    return await StockDataFetcher.get_history_data(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date
    )

@mcp.tool('stock_individual_basic_info')
async def stock_individual_basic_info(stock_code: str) -> Dict:
    '''
    获取指定股票代码的基本信息
    :param stock_code: 股票代码
    :return: 基本信息列表或错误信息
    '''
    return await StockDataFetcher.get_basic_info(stock_code)

@mcp.tool('risk_stocks')
async def risk_stocks() -> Dict:
    '''
    获取股票风险警示板
    :return: 风险信息列表或错误信息
    '''
    return await StockDataFetcher.get_risk_stocks()

@mcp.tool('stock_merito_data')
async def stock_merito_data(stock_code: str) -> Dict:
    '''
    获取指定股票的主营介绍数据
    :param stock_code: 股票代码
    :return: 主营介绍数据列表或错误信息
    '''
    return await StockDataFetcher.get_merito_data(stock_code)

@mcp.tool('get_stock_news')
async def get_stock_news(stock_code: str) -> Dict:
    '''
    获取指定股票代码的新闻数据
    :param stock_code: 股票代码
    :return: 新闻数据列表或错误信息
    '''
    return await StockDataFetcher.get_news(stock_code)

@mcp.tool('get_finance_news')
async def get_finance_news(page: int = 1, page_size: int = 10) -> Dict:
    '''
    获取财经精选新闻数据，支持分页
    :param page: 页码，从1开始
    :param page_size: 每页条数，默认10条
    :return: 新闻数据列表或错误信息
    '''
    try:
        # 获取全部新闻数据
        all_news = await StockDataFetcher.get_finance_news()
        
        # 计算分页
        total = len(all_news)
        start = (page - 1) * page_size
        end = start + page_size
        
        # 截取当前页数据
        paginated_data = all_news[start:end]
        
        # 返回带分页信息的结果
        return {
            'data': paginated_data,
            'pagination': {
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
        }
    except Exception as e:
        logger.error(f"获取财经新闻失败: {e}")
        return {"error": str(e), "message": "获取财经新闻失败"}

def configure_logging(log_level: str = 'info') -> None:
    '''配置日志级别'''
    level = getattr(logging, log_level.upper())
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        filename='stock-info.log'
    )

def parse_arguments():
    '''解析命令行参数'''
    parser = argparse.ArgumentParser(description='股票数据服务')
    parser.add_argument('--transport', 
                       choices=['stdio', 'http'], 
                       default='stdio', 
                       help='传输协议: stdio(默认)或http')
    parser.add_argument('--port', 
                       type=int, 
                       default=8080, 
                       help='HTTP服务器端口(默认8080)')
    parser.add_argument('--log-level',
                       choices=['debug', 'info', 'warning', 'error'],
                       default='info',
                       help='日志级别(默认info)')
    return parser.parse_args()

async def test():
    response =await get_finance_news()
    print(response)

if __name__ == "__main__":
    # import asyncio
    # asyncio.run(test())
    # input("Press Enter to continue...")
    # exit()

    args = parse_arguments()
    configure_logging(args.log_level)
    
    try:
        logger.info("启动MCP服务...")
        if args.transport == 'http':
            mcp.run_http(port=args.port)
        else:
            mcp.run()
    except Exception as e:
        logger.error(f"MCP服务启动失败: {e}")