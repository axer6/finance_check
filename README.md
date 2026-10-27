# Stock Monitor

A股 + 美股行情监控与可视化看板。基于 Streamlit + AKShare + yfinance + SQLite。

## 功能

- A 股日线行情（AKShare，前复权）
- 美股日线行情（yfinance）
- K 线图 + MA5/20/60 + MACD + RSI 联动展示
- 自选股配置（YAML）
- 一键刷新数据

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 首次拉取数据
python -m src.scheduler.jobs

# 3. 启动看板
streamlit run app.py
```

打开浏览器访问 http://localhost:8501

## 配置自选股

编辑 `config/watchlist.yaml`：

```yaml
a_share:
  - code: "600519"
    name: "贵州茅台"

us_share:
  - code: "AAPL"
    name: "苹果"
```

## 项目结构

```
stock-monitor/
├── app.py                  # Streamlit 主入口
├── config/
│   └── watchlist.yaml      # 自选股配置
├── src/
│   ├── fetcher/           # 数据采集
│   │   ├── a_share.py     #   A股 (AKShare)
│   │   └── us_share.py    #   美股 (yfinance)
│   ├── storage/
│   │   └── db.py          # SQLite 读写
│   ├── indicators/
│   │   └── technical.py   # MA/MACD/RSI
│   └── scheduler/
│       └── jobs.py         # 批量拉取任务
└── data/                   # SQLite 数据库（自动生成）
```

## 后续路线

- [ ] 实时行情 WebSocket（盘中监控）
- [ ] 价格阈值告警（企业微信/钉钉推送）
- [ ] PostgreSQL + TimescaleDB 替换 SQLite
- [ ] 技术指标回测
- [ ] Docker Compose 一键部署
