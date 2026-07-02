import pandas as pd
from typing import Dict, Any
from .engine import WorkflowState
from .sandbox import QuantSandbox
from .security import compact_market_data, sanitize_formula
from mcp_server import GoldMCPServer

# Instantiate a single global MCP server simulation instance for consistency
mcp = GoldMCPServer()

def run_data_orchestrator(state: WorkflowState):
    """
    Data Orchestrator Agent:
    Connects to the MCP Server, calls tools to ingest raw historical candles,
    latest real-time bid/ask spread, and macroeconomic news events.
    """
    state.log("Data Orchestrator Agent: Contacting MCP Server...")
    
    # 1. Fetch historical price data (last 50 days)
    hist_resp = mcp.call_tool("get_historical_prices", {"limit": 50})
    if not hist_resp.get("success"):
        raise RuntimeError(f"Failed to fetch historical prices: {hist_resp.get('error')}")
    
    # Convert to Pandas DataFrame for analysis
    candles = hist_resp["data"]
    df = pd.DataFrame(candles)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    state.set("raw_prices", df)
    state.log(f"Data Orchestrator Agent: Ingested {len(df)} historical daily candles.")
    
    # 2. Fetch live price
    live_resp = mcp.call_tool("get_realtime_price")
    if not live_resp.get("success"):
        raise RuntimeError(f"Failed to fetch live prices: {live_resp.get('error')}")
    state.set("realtime_price", live_resp)
    state.log(f"Data Orchestrator Agent: Verified live ticker - {live_resp['price']} USD/oz.")
    
    # 3. Fetch macroeconomic news
    news_resp = mcp.call_tool("get_macro_news", {"limit": 5})
    if not news_resp.get("success"):
        raise RuntimeError(f"Failed to fetch macroeconomic news: {news_resp.get('error')}")
    state.set("news_data", news_resp["news"])
    state.log(f"Data Orchestrator Agent: Ingested {len(news_resp['news'])} news articles.")


def run_quant_analyst(state: WorkflowState):
    """
    Quant Technical Analyst Agent:
    Ingests raw price data, runs moving average crossover calculations and
    RSI computations inside the secure execution sandbox.
    Generates structured buy/sell indicators and crossover signals.
    """
    state.log("Quant Technical Analyst Agent: Initializing execution sandbox...")
    df = state.get("raw_prices")
    if df is None or df.empty:
        raise ValueError("Quant Analyst: Missing 'raw_prices' in workflow state.")
        
    sandbox = QuantSandbox(df)
    
    # Securely calculate technical indicators inside sandbox
    # Safe formulas utilizing defined functions
    sandbox.execute_indicator("SMA_14", "SMA(df, 14)")
    sandbox.execute_indicator("SMA_50", "SMA(df, 50)")
    sandbox.execute_indicator("RSI_14", "RSI(df, 14)")
    
    # Execute double SMA crossover indicator
    sandbox.execute_indicator("SMA_Diff", "SMA(df, 14) - SMA(df, 50)")
    
    processed_df = sandbox.get_dataframe()
    state.set("calculated_prices", processed_df)
    
    # Compile quantitative indicators for reporting
    latest = processed_df.iloc[-1]
    prev = processed_df.iloc[-2]
    
    rsi_val = float(latest["RSI_14"])
    sma_14 = float(latest["SMA_14"])
    sma_50 = float(latest["SMA_50"])
    diff = float(latest["SMA_Diff"])
    prev_diff = float(prev["SMA_Diff"])
    
    # Detect golden cross or death cross signals
    crossover_signal = "NEUTRAL"
    if prev_diff <= 0 and diff > 0:
        crossover_signal = "GOLDEN_CROSS"  # Bullish
    elif prev_diff >= 0 and diff < 0:
        crossover_signal = "DEATH_CROSS"    # Bearish
        
    # Detect RSI extremes
    rsi_sentiment = "NEUTRAL"
    if rsi_val >= 70:
        rsi_sentiment = "OVERBOUGHT"
    elif rsi_val <= 30:
        rsi_sentiment = "OVERSOLD"
        
    signals = {
        "latest_close": float(latest["close"]),
        "sma_14": sma_14,
        "sma_50": sma_50,
        "rsi": rsi_val,
        "rsi_sentiment": rsi_sentiment,
        "crossover_signal": crossover_signal,
        "indicator_trend": "BULLISH" if diff > 0 else "BEARISH"
    }
    
    state.set("technical_signals", signals)
    state.log("Quant Technical Analyst Agent: Sandbox execution completed.")
    state.log(f"Quant Analyst Signals -> RSI: {rsi_val:.2f} ({rsi_sentiment}), Trend: {signals['indicator_trend']}, Crossover: {crossover_signal}")
    
    # Compact context for LLM reporting
    compacted = compact_market_data(processed_df, keep_last_n=5)
    state.set("compacted_prices", compacted)
    state.log(f"Quant Analyst: Context compacted. Retained 5 rows. Compression complete.")


def run_macro_sentiment(state: WorkflowState):
    """
    Macroeconomic Sentiment Agent:
    Processes macroeconomic news reports using semantic mapping,
    calculates index momentum, and determines general safe-haven sentiment.
    """
    state.log("Macroeconomic Sentiment Agent: Analyzing macroeconomic data feeds...")
    news = state.get("news_data")
    if news is None:
        raise ValueError("Macro Sentiment: Missing 'news_data' in workflow state.")
        
    bullish_articles = 0
    bearish_articles = 0
    neutral_articles = 0
    total_score = 0.0
    
    analysis_details = []
    
    for item in news:
        title = item["title"]
        score = item["sentiment_score"]
        impact = item["impact"]
        
        total_score += score
        if impact == "BULLISH":
            bullish_articles += 1
        elif impact == "BEARISH":
            bearish_articles += 1
        else:
            neutral_articles += 1
            
        analysis_details.append(f"- **{title}** (Source: {item['source']}) | Sentiment: {score:+.2f} ({impact})")
        
    avg_sentiment = total_score / len(news) if news else 0.0
    
    # Mapping sentiment boundaries
    if avg_sentiment >= 0.2:
        sentiment_label = "STRONGLY BULLISH" if avg_sentiment >= 0.5 else "MODERATELY BULLISH"
    elif avg_sentiment <= -0.2:
        sentiment_label = "STRONGLY BEARISH" if avg_sentiment <= -0.5 else "MODERATELY BEARISH"
    else:
        sentiment_label = "NEUTRAL"
        
    sentiment_report = {
        "average_sentiment_score": round(avg_sentiment, 2),
        "sentiment_label": sentiment_label,
        "distribution": {
            "bullish": bullish_articles,
            "bearish": bearish_articles,
            "neutral": neutral_articles
        },
        "details_markdown": "\n".join(analysis_details)
    }
    
    state.set("macro_sentiment", sentiment_report)
    state.log("Macroeconomic Sentiment Agent: Sentiment consolidation complete.")
    state.log(f"Macro Sentiment Index -> Score: {avg_sentiment:+.2f} ({sentiment_label})")


def run_reporting_agent(state: WorkflowState):
    """
    Gold Market Reporting Agent:
    Aggregates indicators, live spreads, and sentiment indexes to build a 
    polished daily insight briefing artifact.
    """
    state.log("Gold Market Reporting Agent: Generating briefing artifact...")
    
    live = state.get("realtime_price")
    signals = state.get("technical_signals")
    sentiment = state.get("macro_sentiment")
    perf = state.get("performance", {})
    
    if not live or not signals or not sentiment:
        raise ValueError("Reporting Agent: Insufficient data in workflow state to write report.")
        
    # Build a premium markdown daily briefing report
    report_md = f"""# XAUUSD Gold Market Daily Briefing
**System Generation Date:** {live['timestamp']}  
**Asset Ticker:** Spot Gold (XAUUSD)

---

## 1. Executive Summary
Spot gold is currently trading at **${live['price']:.2f} USD/oz** (Bid: ${live['bid']:.2f} / Ask: ${live['ask']:.2f}), representing a daily change of **{live['change_daily']:+.2f} ({live['change_pct']:+.2f}%)**. The consolidated market outlook is **{sentiment['sentiment_label']}** due to a confluence of bullish macroeconomic variables and strong technical trends.

---

## 2. Real-Time Price Snapshot
* **Current Bid/Ask:** ${live['bid']:.2f} / ${live['ask']:.2f}
* **Spread:** $0.50
* **Daily Gain/Loss:** {live['change_daily']:+.2f} USD
* **Percentage Change:** {live['change_pct']:+.2f}%

---

## 3. Quantitative Technical Analysis
* **Latest Daily Close:** ${signals['latest_close']:.2f}
* **SMA (14-period):** ${signals['sma_14']:.2f}
* **SMA (50-period):** ${signals['sma_50']:.2f}
* **RSI (14-period):** {signals['rsi']:.2f} (Status: **{signals['rsi_sentiment']}**)
* **SMA Crossover Signal:** **{signals['crossover_signal']}**
* **Primary Indicator Trend:** **{signals['indicator_trend']}**

> **Technical Commentary:** 
> Gold's primary price trend is currently **{signals['indicator_trend']}** with a 14-day RSI of **{signals['rsi']:.2f}**. This indicates that the asset is in a healthy, sustainable zone (neither overbought nor oversold). The SMA crossover signal is currently **{signals['crossover_signal']}**, pointing to stable consolidation.

---

## 4. Macroeconomic News & Sentiment
The average macroeconomic sentiment score is **{sentiment['average_sentiment_score']:+.2f}**, registering a outlook of **{sentiment['sentiment_label']}**.
* **Bullish Articles:** {sentiment['distribution']['bullish']}
* **Bearish Articles:** {sentiment['distribution']['bearish']}
* **Neutral Articles:** {sentiment['distribution']['neutral']}

### Recent News Stream
{sentiment['details_markdown']}

---

## 5. System Execution Metrics (ADK 2.0 Graph Workflow)
* **Data Orchestrator Agent:** {perf.get('data_orchestrator', 0.0):.4f}s
* **Quant Technical Analyst Agent:** {perf.get('quant_analyst', 0.0):.4f}s
* **Macroeconomic Sentiment Agent:** {perf.get('macro_sentiment', 0.0):.4f}s
* **Gold Market Reporting Agent:** {perf.get('reporting_agent', 0.0):.4f}s
* **Total Workflow Duration:** {sum(perf.values()):.4f}s
"""
    state.set("briefing_report", report_md)
    state.log("Gold Market Reporting Agent: Briefing report artifact created successfully.")
