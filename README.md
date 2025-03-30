# Stock Info Service

这是一个基于 FastMCP 的股票数据服务，提供了股票历史数据、基本面信息、新闻资讯等功能。

## 项目结构

```
stock-info/
├── src/
│   ├── config/           # 配置管理
│   │   └── settings.py
│   ├── core/            # 核心功能
│   │   └── exceptions.py
│   ├── models/          # 数据模型
│   │   └── stock.py
│   ├── repository/      # 数据访问层
│   │   └── stock_repository.py
│   ├── service/         # 业务逻辑层
│   │   └── stock_service.py
│   └── server.py        # 服务入口
├── pyproject.toml       # 项目配置
└── README.md           # 项目文档
```

## 功能特性

- 获取股票历史数据
- 查询股票基本信息
- 获取风险警示股票列表
- 查看个股新闻
- 获取财经新闻（支持分页）
- 获取股票主营业务信息
- .....后续逐渐增加

## MCP客户端配置步骤
- 1. 拉取代码
- 2. 使用uv建立虚拟环境 python 1.10+
- 3. 使用本地目录方式配置MCP服务
```json
{
  "mcpServers": {
     "stock-info": {
      "isActive": true,
      "command": "uv",
      "args": [
        "--directory",
        "\\path\\to\\sock_info\\src",
        "run",
        "server.py"
      ]
    }
  }
```

## 环境要求

- Python >= 3.10
- 依赖包：
  - fastmcp
  - akshare
  - pandas
  - pydantic
  - pydantic-settings

## 安装部署

1. 创建虚拟环境:
```bash
python -m venv .venv
```

2. 激活虚拟环境:
```bash
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. 安装依赖:
```bash
pip install -e .
```

## 启动服务

```bash
# 使用默认配置启动
python src/server.py

# 使用 HTTP 传输协议启动
python src/server.py --transport http --port 8080

# 设置日志级别
python src/server.py --log-level debug
```

## 工具说明

1. `get_stock_info`: 获取指定股票代码、指定日期范围的股价信息
2. `get_stock_price_monthly`: 获取指定股票最近30天的股价信息
3. `stock_individual_basic_info`: 获取指定股票的基本信息
4. `risk_stocks`: 获取风险警示板股票列表
5. `stock_merito_data`: 获取指定股票的主营业务信息
6. `get_stock_news`: 获取指定股票的新闻资讯
7. `get_finance_news`: 获取财经精选新闻（支持分页）

## 项目特点

1. **模块化设计**：采用清晰的分层架构，便于维护和扩展
2. **统一异常处理**：使用自定义异常体系，提供友好的错误提示
3. **配置集中管理**：使用 pydantic-settings 进行配置管理
4. **类型提示**：全面使用 Python 类型注解，提高代码可读性
5. **数据验证**：使用 Pydantic 模型进行数据验证和序列化

## 开发规范

1. 使用 ruff 进行代码格式化和 lint
2. 遵循 PEP 8 编码规范
3. 保持完整的类型注解
4. 编写清晰的文档字符串

## 错误处理

服务统一返回以下格式的错误信息：

```json
{
    "error": "错误代码",
    "message": "错误描述",
    "details": {
        "额外信息": "值"
    }
}
```

## 主要错误代码

- `STOCK_NOT_FOUND`: 股票代码不存在
- `INVALID_DATE_FORMAT`: 日期格式错误
- `DATA_FETCH_ERROR`: 数据获取失败
- `INVALID_PAGINATION`: 分页参数错误
- `SYSTEM_ERROR`: 系统内部错误
