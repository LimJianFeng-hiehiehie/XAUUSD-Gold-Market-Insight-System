import os
import sys
import argparse

# Include backend in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from adk.engine import WorkflowGraph, WorkflowState
from adk.agents import run_data_orchestrator, run_quant_analyst, run_macro_sentiment, run_reporting_agent

def main():
    parser = argparse.ArgumentParser(description="XAUUSD Gold Market Insight CLI Tool")
    parser.add_argument("--rsi-period", type=int, default=14, help="RSI period (default: 14)")
    parser.add_argument("--sma-fast", type=int, default=14, help="SMA fast period (default: 14)")
    parser.add_argument("--sma-slow", type=int, default=50, help="SMA slow period (default: 50)")
    parser.add_argument("--output", type=str, default="xauusd_briefing.md", help="Output filepath for report")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("      XAUUSD Gold Market Insight System CLI")
    print("=" * 60)
    
    # 1. Setup multi-agent graph
    graph = WorkflowGraph()
    graph.add_node("data_orchestrator", run_data_orchestrator)
    graph.add_node("quant_analyst", run_quant_analyst)
    graph.add_node("macro_sentiment", run_macro_sentiment)
    graph.add_node("reporting_agent", run_reporting_agent)
    
    graph.set_execution_order(["data_orchestrator", "quant_analyst", "macro_sentiment", "reporting_agent"])
    
    state = WorkflowState()
    state.set("rsi_period", args.rsi_period)
    state.set("sma_fast", args.sma_fast)
    state.set("sma_slow", args.sma_slow)
    
    # 2. Run graph workflow
    print("\nRunning ADK 2.0 multi-agent workflow...")
    try:
        final_state = graph.run(state)
        
        # 3. Print Logs
        print("\n--- Execution Logs ---")
        for log in final_state.logs:
            print(log)
            
        # 4. Save and report briefing
        briefing = final_state.get("briefing_report")
        if briefing:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(briefing)
            print("-" * 60)
            print(f"Success! Briefing report written to: {os.path.abspath(args.output)}")
            print("-" * 60)
            
            # Print snapshot
            live = final_state.get("realtime_price")
            signals = final_state.get("technical_signals")
            sentiment = final_state.get("macro_sentiment")
            print(f"Live Price: ${live['price']} | Daily Change: {live['change_pct']:+.2f}%")
            print(f"Quant Trend: {signals['indicator_trend']} (RSI: {signals['rsi']:.2f})")
            print(f"Macro Sentiment: {sentiment['sentiment_label']} (Score: {sentiment['average_sentiment_score']:+.2f})")
            print("=" * 60)
        else:
             print("\nError: Briefing report was not generated.")
             
    except Exception as e:
        print(f"\nExecution Failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
