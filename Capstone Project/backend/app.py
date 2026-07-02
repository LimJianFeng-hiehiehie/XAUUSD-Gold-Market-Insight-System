import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, Any

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from adk.engine import WorkflowGraph, WorkflowState
from adk.agents import run_data_orchestrator, run_quant_analyst, run_macro_sentiment, run_reporting_agent
from mcp_server import GoldMCPServer

app = FastAPI(title="XAUUSD Gold Market Insight System API", version="2.0.0")

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

# Global MCP server instance for independent direct queries
mcp_server = GoldMCPServer()

class RunWorkflowRequest(BaseModel):
    custom_rsi_period: Optional[int] = 14
    custom_sma_fast: Optional[int] = 14
    custom_sma_slow: Optional[int] = 50

@app.post("/api/run-workflow")
async def run_workflow(payload: RunWorkflowRequest):
    """
    Triggers the ADK multi-agent workflow graph.
    Runs Data Orchestration, Quant Analysis, Sentiment Analysis, and Report Generation.
    """
    try:
        # 1. Initialize Graph
        graph = WorkflowGraph()
        graph.add_node("data_orchestrator", run_data_orchestrator)
        graph.add_node("quant_analyst", run_quant_analyst)
        graph.add_node("macro_sentiment", run_macro_sentiment)
        graph.add_node("reporting_agent", run_reporting_agent)
        
        graph.set_execution_order(["data_orchestrator", "quant_analyst", "macro_sentiment", "reporting_agent"])
        
        # 2. Setup initial state with parameters
        state = WorkflowState()
        # Pass custom parameters if any
        state.set("rsi_period", payload.custom_rsi_period)
        state.set("sma_fast", payload.custom_sma_fast)
        state.set("sma_slow", payload.custom_sma_slow)
        
        # 3. Execute Workflow
        final_state = graph.run(state)
        
        # 4. Gather results
        raw_prices_df = final_state.get("calculated_prices")
        # Format prices data for the charts (convert DatetimeIndex to string list)
        chart_data = []
        if raw_prices_df is not None:
            chart_df = raw_prices_df.tail(30).reset_index()
            for _, row in chart_df.iterrows():
                chart_data.append({
                    "date": row["timestamp"].strftime("%Y-%m-%d") if hasattr(row["timestamp"], "strftime") else str(row["timestamp"]),
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "sma_14": float(row["SMA_14"]) if "SMA_14" in row and not pd_isna(row["SMA_14"]) else None,
                    "sma_50": float(row["SMA_50"]) if "SMA_50" in row and not pd_isna(row["SMA_50"]) else None,
                    "rsi": float(row["RSI_14"]) if "RSI_14" in row and not pd_isna(row["RSI_14"]) else None
                })
                
        return {
            "success": True,
            "realtime_price": final_state.get("realtime_price"),
            "technical_signals": final_state.get("technical_signals"),
            "macro_sentiment": final_state.get("macro_sentiment"),
            "briefing_report": final_state.get("briefing_report"),
            "logs": final_state.logs,
            "performance": final_state.get("performance"),
            "chart_data": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow Execution Failed: {str(e)}")

# Helper to check pandas nan
def pd_isna(val):
    import pandas as pd
    return pd.isna(val)

@app.get("/api/prices/historical")
async def get_historical_prices(limit: int = 50):
    """Directly queries MCP Server for historical daily candles"""
    result = mcp_server.get_historical_prices(limit=limit)
    if not result.get("success"):
         raise HTTPException(status_code=500, detail=result.get("error"))
    return result

@app.get("/api/prices/realtime")
async def get_realtime_price():
    """Directly queries MCP Server for current live gold price and change metric"""
    result = mcp_server.get_realtime_price()
    if not result.get("success"):
         raise HTTPException(status_code=500, detail=result.get("error"))
    return result

@app.get("/api/news")
async def get_news(limit: int = 5):
    """Directly queries MCP Server for macro news feeds"""
    result = mcp_server.get_macro_news(limit=limit)
    if not result.get("success"):
         raise HTTPException(status_code=500, detail=result.get("error"))
    return result

# --- STATIC FRONTEND ASSETS ROUTES ---

@app.get("/")
async def read_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail=f"Frontend Index not found at {index_path}")
    return FileResponse(index_path)

@app.get("/style.css")
async def read_style():
    style_path = os.path.join(FRONTEND_DIR, "style.css")
    if not os.path.exists(style_path):
        raise HTTPException(status_code=404, detail="Frontend CSS not found")
    return FileResponse(style_path, media_type="text/css")

@app.get("/app.js")
async def read_js():
    js_path = os.path.join(FRONTEND_DIR, "app.js")
    if not os.path.exists(js_path):
        raise HTTPException(status_code=404, detail="Frontend JS not found")
    return FileResponse(js_path, media_type="application/javascript")

if __name__ == "__main__":
    print(f"Starting server. Frontend directory: {FRONTEND_DIR}")
    uvicorn.run("app:app", host="127.0.0.1", port=3000, reload=True)
