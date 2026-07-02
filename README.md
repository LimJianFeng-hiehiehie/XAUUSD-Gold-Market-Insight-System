# XAUUSD Gold Market Insight System

A full-stack, modular AI agent system built with **ADK 2.0 (graph workflow agent project)**, a robust simulated **MCP Server architecture** (handling historical and real-time gold market data), a **Secure Python code execution sandbox**, and a premium **glassmorphic dashboard interface**.

---

## 🚀 System Architecture Overview

The system includes multiple collaborative agents running inside an execution graph workflow:
1. **Data Orchestrator Agent**: Handles fetching historical daily candlestick data, live tick quotes (bid/ask), and macroeconomic financial news.
2. **Quant Technical Analyst Agent**: Performs mathematical calculation of technical indicators (Simple Moving Averages, RSI oscillator, and double SMA crossover signals) inside a secure sandboxed workspace.
3. **Macroeconomic Sentiment Agent**: Aggregates news articles, extracts sentiment score vectors, and maps macro market indicators (inflation CPI, interest rates, geopolitics) to a net sentiment momentum value.
4. **Gold Market Reporting Agent**: Consolidates quantitative and sentiment outputs to generate a formatted markdown briefing report.

```
       [Dashboard UI] <--- FastAPI (Port 3000) ---> [ADK 2.0 Workflow Engine]
                                                             |
            +------------------------------------------------+
            |
            v
   [Data Orchestrator] <---------------------> [MCP Server (XAUUSD prices, news)]
            |
            v (Writes price frames)
      [Workflow State]
            |
            v (Ingests prices)
     [Quant Analyst] <------ executes indicator scripts ------> [Restricted Sandbox]
            |                                                      (Pandas / math)
            v (Writes indicators & crossover signals)
      [Workflow State]
            |
            v (Ingests macro news)
    [Macro Sentiment] <-------- computes momentum score --------> [Heuristics Classifier]
            |
            v (Writes consolidated sentiment)
      [Workflow State]
            |
            v (Consolidates all signals)
     [Reporting Agent] --------> generates final briefing report ---> [Daily Briefing Output]
```

---

## 🗂 GitHub-Ready Project Template

The project is structured to support local deployment and CI/CD pipelines out-of-the-box:

```text
.
├── backend/
│   ├── adk/
│   │   ├── __init__.py
│   │   ├── agents.py       # Collaborative agent tasks (Orchestrator, Quant, Sentiment, Reporting)
│   │   ├── engine.py       # Stateful Graph Workflow Coordinator (ADK 2.0 workflow)
│   │   ├── sandbox.py      # Secure Python Pandas execution sandbox for indicators
│   │   └── security.py     # Parameter validation, sanitization, and data context compaction
│   ├── app.py              # Main FastAPI application server (routes, static assets, workflow endpoint)
│   ├── cli.py              # Command-line utility to run workflow and output briefing report
│   ├── adk_eval.py         # Sandbox security validation, compaction testing & performance benchmarks
│   └── mcp_server.py       # MCP Server simulator supplying prices and macroeconomic news
├── frontend/
│   ├── index.html          # Dashboard HTML wireframe
│   ├── style.css           # Premium glassmorphic styling
│   └── app.js              # Live metrics loading, Chart.js mapping, and log stream animation
├── requirements.txt        # Backend dependencies
├── xauusd_briefing.md      # Generated AI Market Insight briefing report
└── README.md               # Product Documentation
```

---

## 🛠 MCP Server Code Structure

The **Model Context Protocol (MCP)** server simulator in `backend/mcp_server.py` implements the standard protocol tool structure:

```python
class GoldMCPServer:
    def list_tools(self) -> List[Dict[str, Any]]:
        # Exposes tools: "get_historical_prices", "get_realtime_price", "get_macro_news"
        ...
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        # Dispatches requests to internal tool functions
        ...
        
    def get_historical_prices(self, limit: int) -> Dict[str, Any]:
        # Generates and filters synthetic daily candle array (Date, O, H, L, C, Vol)
        ...

    def get_realtime_price(self) -> Dict[str, Any]:
        # Generates live spot price tick, bid, ask spreads, and percentage changes
        ...

    def get_macro_news(self, limit: int) -> Dict[str, Any]:
        # Returns macroeconomic headlines (CPI cooling, FOMC decisions, geopolitical safe-haven demands)
        ...
```

---

## 🖥 Dashboard Wireframe & Layout

The front-end user interface is designed using responsive vanilla CSS layouts:

```text
+-----------------------------------------------------------------------------------------+
| ✨ XAUUSD: Gold Market Insight System                           [Live status] [15:54:02] |
+-----------------------------------------------------------------------------------------+
|  ORCHESTRATION CONTROLS           |  XAUUSD SPOT PRICE CHART OVERLAYS                   |
|  Quant RSI Period:   [ 14 ]       |  $2397.14 (+0.14%)                                  |
|  Fast SMA (Days):    [ 14 ]       |  +-----------------------------------------------+  |
|  Slow SMA (Days):    [ 50 ]       |  |  (Candlesticks/Line charts overlaying Fast/   |  |
|  [Execute Workflow Button]        |  |  Slow Simple Moving Averages)                 |  |
|                                   |  +-----------------------------------------------+  |
|  CORE AGENT LATENCIES             |  XAUUSD RSI OSCILLATOR (Sub-chart)                  |
|  Data Orchestrator:  0.0038s      |  +-----------------------------------------------+  |
|  Quant Analyst:      0.0202s      |  |  [RSI Line oscillating between 30 and 70]     |  |
|  Macro Sentiment:    0.0000s      |  +-----------------------------------------------+  |
|  Reporting Agent:    0.0000s      |                                                     |
|  Total Core Time:    0.0240s      |                                                     |
+-----------------------------------+-----------------------------------------------------+
|  LIVE SPOT PRICE CARD             |  SENTIMENT CARD              |  TECHNICAL SIGNALS   |
|  $2397.14 (+0.14%)                |  NEUTRAL                     |  BEARISH             |
|  Bid: $2396.89 | Ask: $2397.39    |  Avg: +0.15 (Bull: 3, Bear: 2) |  RSI: 41.00          |
+-----------------------------------+-----------------------------------------------------+
|  WORKFLOW EXECUTION LOGS TERMINAL                                                       |
|  [2026-07-02 15:56:46] Starting execution of Node: 'data_orchestrator'...               |
|  [2026-07-02 15:56:46] Ingested 50 historical daily candles...                          |
|  [2026-07-02 15:56:46] Quant Technical Analyst Agent: Sandbox execution completed...    |
+-----------------------------------------------------------------------------------------+
|  MACROECONOMIC NEWS STREAM                                                              |
|  - US CPI Inflation Cools to 3.3% (Financial Times) [BULLISH]                           |
|  - Federal Reserve Holds Rates Steady (Bloomberg) [BEARISH]                             |
+-----------------------------------------------------------------------------------------+
|  UNIFIED DAILY BRIEFING REPORT                                                          |
|  # XAUUSD Gold Market Daily Briefing                                                    |
|  **Executive Summary**: Spot gold is trading at $2397.14...                             |
|  **Quantitative Analysis**: SMA Crossover Signal is Neutral...                          |
+-----------------------------------------------------------------------------------------+
```

---

## ⚡ Step-by-Step Antigravity Workflow Explanation

When you execute the workflow via the UI Dashboard or CLI, the end-to-end processing pipeline triggers:

1. **Step 1: Data Ingestion**
   - The **Data Orchestrator Agent** connects to the **MCP Server** simulator, calling `get_historical_prices`, `get_realtime_price`, and `get_macro_news`. It converts the historical JSON arrays into a Pandas DataFrame and writes them to the workflow state.
2. **Step 2: Technical calculation Sandbox**
   - The **Quant Analyst Agent** reads the raw prices from the state, sanitizes calculation configurations, and initiates `QuantSandbox`.
   - The sandbox runs the mathematical operations (SMA, EMA, RSI) inside a restricted workspace, generating indicator series.
   - The agent detects crossover points and RSI overbought/oversold boundaries, writes these indicators and signals to the state, and runs **Context Compaction** (reducing 50 rows of raw candlestick data down to the last 5 rows and aggregate stats) to prune the context window.
3. **Step 3: Sentiment Vector Consolidation**
   - The **Macro Sentiment Agent** parses the headlines retrieved in Step 1, scores their sentiment weights (e.g. inflation cools = bullish, hawkish Fed = bearish), computes a consolidated net score index (-1.0 to +1.0), and classifies the net market momentum.
4. **Step 4: Report Compiling**
   - The **Gold Market Reporting Agent** reads all computed technical signals, live price spreads, macroeconomic sentiment scores, and node latency metrics. It formats them into a comprehensive Markdown Daily Briefing document.
5. **Step 5: Front-end Rendering**
   - The FastAPI backend returns this structured payload to the browser.
   - The client-side `app.js` runs a scrolling typewriter log animation, updates the live card widgets (price, spread, sentiment index), plots price curves and RSI oscillators on Chart.js canvases, and translates the markdown report into HTML.

---

## ⚙️ Quick Start Installation

### Prerequisites
- Python 3.11.x installed on your system.

### Step 1: Install Dependencies
Navigate to the root project directory and install the necessary dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Run Evaluation Tests
Validate sandbox protection limits, context compression ratios, and processing latency:
```bash
python backend/adk_eval.py
```

### Step 3: Run the CLI Tool
Trigger a multi-agent workflow compile and write the briefing report directly from terminal:
```bash
python backend/cli.py
```

### Step 4: Run the FastAPI server
Launch the local web server:
```bash
python backend/app.py
```
Open [http://localhost:3000](http://localhost:3000) in your web browser.
#   X A U U S D - G o l d - M a r k e t - I n s i g h t - S y s t e m  
 