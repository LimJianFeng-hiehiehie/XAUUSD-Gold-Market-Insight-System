<div align="center">

# ✨ XAUUSD Gold Market Insight System

### *A Multi-Agent AI Workflow for Real-Time Gold Market Intelligence*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![ADK 2.0](https://img.shields.io/badge/ADK-2.0_Workflow_Engine-FF6F00?style=for-the-badge)](#)
[![MCP](https://img.shields.io/badge/MCP-Server_Architecture-6E56CF?style=for-the-badge)](#)
[![Chart.js](https://img.shields.io/badge/Chart.js-Visualization-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)](#)

**A full-stack, modular AI agent system** built with **ADK 2.0 graph workflow orchestration**, a simulated **MCP Server** for market data, a **secure sandboxed Python execution layer**, and a **premium glassmorphic dashboard** — designed to deliver institutional-grade gold (XAUUSD) market briefings in real time.

[Overview](#-system-architecture-overview) •
[Architecture](#-mcp-server-code-structure) •
[Dashboard](#-dashboard-preview) •
[Workflow](#-step-by-step-workflow-explanation) •
[Quick Start](#️-quick-start-installation) •
[Project Structure](#-project-structure)

</div>

---

## 🧭 Overview

The **XAUUSD Gold Market Insight System** is a collaborative multi-agent pipeline that fuses **quantitative technical analysis**, **macroeconomic sentiment intelligence**, and **live market data** into a single, automatically generated daily briefing — rendered through a premium, real-time analytics dashboard.
<img width="930" height="213" alt="Image" src="https://github.com/user-attachments/assets/cc054dba-c134-4a8e-97c0-921b6c904699" />
<img width="915" height="419" alt="Image" src="https://github.com/user-attachments/assets/2e612e74-ce80-4881-baf9-d5ba473275cf" />
<img width="919" height="421" alt="Image" src="https://github.com/user-attachments/assets/64a28a83-feb6-4f61-8d48-33c24b3a359a" />
Four specialized agents operate inside a stateful graph workflow, each contributing a distinct layer of market insight:

| Agent | Role | Output |
|---|---|---|
| 🛰️ **Data Orchestrator** | Fetches historical candles, live tick quotes, and macro news via the MCP Server | Structured market data frames |
| 📊 **Quant Technical Analyst** | Computes SMA, RSI, and crossover signals inside a secure sandbox | Indicator series + technical signals |
| 🌍 **Macroeconomic Sentiment** | Scores macro headlines and derives net sentiment momentum | Sentiment index (-1.0 → +1.0) |
| 📝 **Gold Market Reporting** | Consolidates all signals into a polished markdown briefing | Daily Briefing Report |

---

## 🚀 System Architecture Overview

The system runs as a **stateful, directed execution graph** — each agent reads from and writes to a shared workflow state, enabling composable, auditable, and low-latency multi-agent orchestration.

```
       ┌────────────────┐        FastAPI (Port 3000)        ┌──────────────────────────┐
       │  Dashboard UI  │ ───────────────────────────────── │  ADK 2.0 Workflow Engine │
       └────────────────┘                                   └────────────┬─────────────┘
                                                                           │
                                                                           ▼
                                                          ┌─────────────────────────────┐
                                                          │      Data Orchestrator       │
                                                          └───────────────┬─────────────┘
                                                                          │  live prices · candles · news
                                                                          ▼
                                                          ┌─────────────────────────────┐
                                                          │   MCP Server (XAUUSD feed)   │
                                                          └───────────────┬─────────────┘
                                                                          │  writes price frames
                                                                          ▼
                                                          ┌─────────────────────────────┐
                                                          │        Workflow State        │
                                                          └───────────────┬─────────────┘
                                                                          │ ingests prices
                                                                          ▼
                                       executes indicator scripts   ┌───────────────┐
                                  ┌───────────────────────────────▶ │ Quant Analyst │
                                  │                                 └───────┬───────┘
                        ┌─────────────────────┐                            │ writes indicators + signals
                        │ Restricted Sandbox   │◀───────────────────────────┘
                        │ (Pandas / math)      │
                        └─────────────────────┘                            ▼
                                                          ┌─────────────────────────────┐
                                                          │        Workflow State        │
                                                          └───────────────┬─────────────┘
                                                                          │ ingests macro news
                                       computes momentum score           ▼
                                  ┌───────────────────────────────▶ ┌───────────────┐
                                  │                                 │ Macro Sentiment│
                        ┌─────────────────────┐                    └───────┬───────┘
                        │ Heuristics Classifier│◀───────────────────────────┘
                        └─────────────────────┘                            │ writes sentiment
                                                                            ▼
                                                          ┌─────────────────────────────┐
                                                          │        Workflow State        │
                                                          └───────────────┬─────────────┘
                                                                          │ consolidates all signals
                                                                          ▼
                                                          ┌─────────────────────────────┐
                                                          │       Reporting Agent        │
                                                          └───────────────┬─────────────┘
                                                                          │
                                                                          ▼
                                                             📄 Daily Briefing Output
```

---

## 🛠 MCP Server Code Structure

The **Model Context Protocol (MCP)** server simulator, implemented in `backend/mcp_server.py`, exposes a standard protocol tool interface for market data retrieval:

```python
class GoldMCPServer:
    def list_tools(self) -> List[Dict[str, Any]]:
        """Exposes tools: get_historical_prices, get_realtime_price, get_macro_news"""
        ...

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches requests to internal tool functions"""
        ...

    def get_historical_prices(self, limit: int) -> Dict[str, Any]:
        """Generates and filters synthetic daily candle array (Date, O, H, L, C, Vol)"""
        ...

    def get_realtime_price(self) -> Dict[str, Any]:
        """Generates live spot price tick, bid/ask spreads, and percentage change"""
        ...

    def get_macro_news(self, limit: int) -> Dict[str, Any]:
        """Returns macroeconomic headlines (CPI, FOMC decisions, geopolitical risk)"""
        ...
```

> 💡 **Why it matters:** modeling data access through MCP's `list_tools` / `call_tool` contract keeps the agent layer fully decoupled from the data layer — swap the simulator for a live broker feed with zero changes to the agent logic.

---

## 🖥 Dashboard Preview

A responsive, **glassmorphic** interface surfaces every layer of the pipeline — from raw orchestration controls to the final AI-generated briefing — in a single real-time view.

```
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║ ✨ XAUUSD: Gold Market Insight System                    ● Live      15:56:46           ║
╠═══════════════════════════════════════════════════════════╦════════════════════════════╣
║  ORCHESTRATION CONTROLS                                    ║  XAUUSD SPOT PRICE CHART    ║
║  Quant RSI Period    [ 14 ]                                ║  $2,397.14  ▲ +0.14%        ║
║  Fast SMA (Days)     [ 14 ]                                ║  ┌──────────────────────┐   ║
║  Slow SMA (Days)     [ 50 ]                                ║  │  Candles + Fast/Slow │   ║
║  [ ▶ Execute Workflow ]                                    ║  │  SMA overlay chart   │   ║
║                                                              ║  └──────────────────────┘   ║
║  CORE AGENT LATENCIES                                       ║  XAUUSD RSI OSCILLATOR       ║
║  Data Orchestrator     0.0038s                              ║  ┌──────────────────────┐   ║
║  Quant Analyst         0.0202s                              ║  │  RSI oscillating      │   ║
║  Macro Sentiment       0.0000s                              ║  │  between 30 – 70      │   ║
║  Reporting Agent       0.0000s                               ║  └──────────────────────┘   ║
║  Total Core Time       0.0240s                              ║                              ║
╠═══════════════════════════╦═══════════════════════════════╦════════════════════════════╣
║  LIVE SPOT PRICE           ║  SENTIMENT                    ║  TECHNICAL SIGNALS          ║
║  $2,397.14  ▲ +0.14%       ║  🟡 NEUTRAL                    ║  🔴 BEARISH                  ║
║  Bid 2396.89 · Ask 2397.39 ║  Avg +0.15 (Bull 3 · Bear 2)  ║  RSI 41.00                   ║
╠═══════════════════════════╩═══════════════════════════════╩════════════════════════════╣
║  WORKFLOW EXECUTION LOGS                                                                 ║
║  [15:56:46] Starting execution of node 'data_orchestrator'...                            ║
║  [15:56:46] Ingested 50 historical daily candles...                                      ║
║  [15:56:46] Quant Analyst: sandbox execution completed...                                ║
╠═══════════════════════════════════════════════════════════════════════════════════════╣
║  MACROECONOMIC NEWS STREAM                                                               ║
║  • US CPI Inflation Cools to 3.3% — Financial Times          🟢 BULLISH                  ║
║  • Federal Reserve Holds Rates Steady — Bloomberg             🔴 BEARISH                  ║
╠═══════════════════════════════════════════════════════════════════════════════════════╣
║  UNIFIED DAILY BRIEFING REPORT                                                           ║
║  # XAUUSD Gold Market Daily Briefing                                                     ║
║  **Executive Summary** — Spot gold is trading at $2,397.14...                            ║
║  **Quantitative Analysis** — SMA crossover signal is Neutral...                          ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
```

**Design language:** frosted-glass panels, soft depth shadows, live blinking status indicator, animated typewriter log stream, and Chart.js-powered candlestick + RSI visualizations — tuned for a premium fintech aesthetic.

---

## ⚡ Step-by-Step Workflow Explanation

Executing the workflow — via the dashboard or CLI — triggers a five-stage pipeline:

### 1️⃣ Data Ingestion
The **Data Orchestrator Agent** connects to the **MCP Server**, calling `get_historical_prices`, `get_realtime_price`, and `get_macro_news`. Historical JSON arrays are converted into a Pandas DataFrame and written to the workflow state.

### 2️⃣ Technical Calculation Sandbox
The **Quant Analyst Agent** reads raw prices from state, sanitizes calculation parameters, and spins up `QuantSandbox` — a **restricted execution workspace** running SMA, EMA, and RSI computations. It detects crossover points and overbought/oversold RSI boundaries, then runs **Context Compaction**, pruning 50 rows of candle data down to the last 5 rows plus aggregate stats to keep the context window lean.

### 3️⃣ Sentiment Vector Consolidation
The **Macro Sentiment Agent** parses the headlines from Step 1, assigns sentiment weights (e.g. *cooling inflation → bullish*, *hawkish Fed → bearish*), and computes a consolidated net sentiment score from **-1.0 to +1.0**, classifying overall market momentum.

### 4️⃣ Report Compiling
The **Gold Market Reporting Agent** reads all technical signals, live price spreads, sentiment scores, and per-node latency metrics, formatting them into a comprehensive **Markdown Daily Briefing**.

### 5️⃣ Front-End Rendering
FastAPI returns the structured payload to the browser. `app.js` drives a scrolling typewriter log animation, updates live metric cards, plots price/RSI charts via Chart.js, and renders the markdown briefing as HTML.

---

## 📂 Project Structure

```text
.
├── backend/
│   ├── adk/
│   │   ├── __init__.py
│   │   ├── agents.py        # Collaborative agent tasks (Orchestrator, Quant, Sentiment, Reporting)
│   │   ├── engine.py        # Stateful graph workflow coordinator (ADK 2.0)
│   │   ├── sandbox.py       # Secure Python/Pandas execution sandbox for indicators
│   │   └── security.py      # Parameter validation, sanitization & context compaction
│   ├── app.py                # Main FastAPI app (routes, static assets, workflow endpoint)
│   ├── cli.py                 # CLI utility to run the workflow and output a briefing report
│   ├── adk_eval.py            # Sandbox security, compaction ratio & latency benchmarks
│   └── mcp_server.py          # MCP Server simulator (prices + macroeconomic news)
├── frontend/
│   ├── index.html             # Dashboard HTML wireframe
│   ├── style.css               # Premium glassmorphic styling
│   └── app.js                   # Live metrics, Chart.js rendering, animated log stream
├── requirements.txt            # Backend dependencies
├── xauusd_briefing.md           # Generated AI market insight briefing
└── README.md                     # Product documentation
```

---

## ⚙️ Quick Start Installation

### Prerequisites
- Python **3.11.x**

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run evaluation tests
Validates sandbox protection limits, context-compression ratios, and processing latency:
```bash
python backend/adk_eval.py
```

### 3. Run the CLI tool
Triggers a full multi-agent workflow run and writes the briefing report to disk:
```bash
python backend/cli.py
```

### 4. Launch the FastAPI server
```bash
python backend/app.py
```
Then open **[http://localhost:3000](http://localhost:3000)** in your browser. 🎉

---

## 🏆 Why This Stands Out

- **Composable multi-agent graph** — each agent is independently testable and swappable via the ADK 2.0 workflow engine.
- **Security-first sandboxing** — indicator math executes in a restricted Pandas/math-only workspace, validated by `security.py` and benchmarked in `adk_eval.py`.
- **Context-aware engineering** — automatic compaction keeps state lean without losing analytical fidelity.
- **Protocol-driven data access** — MCP's `list_tools`/`call_tool` contract cleanly separates data source from agent logic, ready to swap in a live broker feed.
- **Production-grade UI polish** — glassmorphic design, live log streaming, and Chart.js visual analytics deliver a genuinely premium demo experience.

---

<div align="center">

**Built for traders, analysts, and AI engineers who want quant + macro + LLM synthesis in one pipeline.**

</div>
