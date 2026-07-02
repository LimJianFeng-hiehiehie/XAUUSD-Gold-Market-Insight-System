import datetime
import random
from typing import Dict, Any, List

class GoldMCPServer:
    """
    Model Context Protocol (MCP) Server for XAUUSD Gold market data.
    Exposes tools for fetching historical prices, real-time prices, and macroeconomic news.
    """
    def __init__(self):
        self.historical_data = self._generate_historical_data()
        self.news_database = self._generate_macro_news()
        
    def _generate_historical_data(self) -> List[Dict[str, Any]]:
        """Generates 60 days of synthetic daily XAUUSD historical data with realistic volatility"""
        data = []
        base_date = datetime.datetime.now() - datetime.timedelta(days=70)
        current_price = 2320.0  # Starting base price for gold
        
        # Seed for reproducibility
        random.seed(42)
        
        for i in range(70):
            date_val = base_date + datetime.timedelta(days=i)
            # Skip weekends
            if date_val.weekday() in (5, 6):
                continue
                
            # Random daily movements between -1.5% and +1.7%
            pct_change = random.uniform(-0.015, 0.017)
            price_change = current_price * pct_change
            
            open_p = current_price
            close_p = current_price + price_change
            high_p = max(open_p, close_p) + random.uniform(2.0, 15.0)
            low_p = min(open_p, close_p) - random.uniform(2.0, 12.0)
            volume = int(random.uniform(150000, 350000))
            
            data.append({
                "timestamp": date_val.strftime("%Y-%m-%d"),
                "open": round(open_p, 2),
                "high": round(high_p, 2),
                "low": round(low_p, 2),
                "close": round(close_p, 2),
                "volume": volume
            })
            current_price = close_p
            
        return data

    def _generate_macro_news(self) -> List[Dict[str, Any]]:
        """Generates a database of macro news articles impacting the Gold Market"""
        now = datetime.datetime.now()
        
        articles = [
            {
                "id": 1,
                "title": "US CPI Inflation Cools to 3.3%, Boosting Rate Cut Hopes",
                "source": "Financial Times",
                "timestamp": (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
                "content": "US consumer price index rises less than expected, prompting traders to increase bets on Federal Reserve interest rate cuts. Lower interest rates decrease the opportunity cost of holding non-yielding Gold, triggering a $25 surge in spot XAUUSD.",
                "impact": "BULLISH",
                "sentiment_score": 0.85
            },
            {
                "id": 2,
                "title": "Federal Reserve Holds Rates Steady, Projects Single Cut for 2026",
                "source": "Bloomberg",
                "timestamp": (now - datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
                "content": "The Federal Open Market Committee (FOMC) maintains interest rates at 5.25%-5.5%. Policymakers present a hawkish stance, trimming rate cut forecasts. The US Dollar Index (DXY) climbs to 105.2, creating downward pressure on precious metals.",
                "impact": "BEARISH",
                "sentiment_score": -0.65
            },
            {
                "id": 3,
                "title": "Safe-Haven Flows Intensify Amid Escalating Middle East Geopolitical Risks",
                "source": "Reuters",
                "timestamp": (now - datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M"),
                "content": "Escalating military exchanges and stalled cease-fire negotiations drive investors to safe-haven assets. Central banks and retail investors are purchasing physical gold, sustaining prices despite higher-for-longer yields.",
                "impact": "BULLISH",
                "sentiment_score": 0.90
            },
            {
                "id": 4,
                "title": "US Retail Sales Rise Modestly, Suggesting Economic Softening",
                "source": "Wall Street Journal",
                "timestamp": (now - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M"),
                "content": "US retail sales grew by 0.1% last month, signaling consumer spending moderation. Bond yields slide as 10-year Treasury yields drop to 4.22%. Gold traders react positively to signs of slowing growth which might prompt a Fed pivot.",
                "impact": "BULLISH",
                "sentiment_score": 0.40
            },
            {
                "id": 5,
                "title": "China's Central Bank Pauses Gold Buying After 18-Month Spree",
                "source": "CNBC",
                "timestamp": (now - datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M"),
                "content": "The People's Bank of China (PBOC) reported unchanged gold holdings at 72.8 million ounces, pausing purchases for the first time since late 2022. Analysts note high gold prices are discouraging official buying, leading to temporary profit-taking in the spot market.",
                "impact": "BEARISH",
                "sentiment_score": -0.75
            },
            {
                "id": 6,
                "title": "Gold ETF Outflows Slow Down; European Inflows Pick Up Pace",
                "source": "World Gold Council",
                "timestamp": (now - datetime.timedelta(days=12)).strftime("%Y-%m-%d %H:%M"),
                "content": "Global gold exchange-traded funds (ETFs) witnessed slower outflows this month. Notably, European-listed gold funds saw significant inflows, driven by interest rate cuts from the European Central Bank (ECB) and the Swiss National Bank.",
                "impact": "NEUTRAL",
                "sentiment_score": 0.15
            }
        ]
        return articles

    # --- Tool Endpoints ---
    
    def get_historical_prices(self, limit: int = 50) -> Dict[str, Any]:
        """Tool: Retrieve historical daily candles for XAUUSD"""
        try:
            result = self.historical_data[-limit:]
            return {
                "success": True,
                "data": result,
                "count": len(result),
                "units": "USD per Troy Ounce"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_realtime_price(self) -> Dict[str, Any]:
        """Tool: Get the latest current price of XAUUSD"""
        try:
            last_close = self.historical_data[-1]["close"]
            # Simulate a live tick fluctuations within +/- $3.50
            live_price = last_close + round(random.uniform(-3.50, 3.50), 2)
            bid = round(live_price - 0.25, 2)
            ask = round(live_price + 0.25, 2)
            
            return {
                "success": True,
                "symbol": "XAUUSD",
                "price": round(live_price, 2),
                "bid": bid,
                "ask": ask,
                "change_daily": round(live_price - last_close, 2),
                "change_pct": round(((live_price - last_close) / last_close) * 100, 2),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_macro_news(self, limit: int = 5) -> Dict[str, Any]:
        """Tool: Fetch latest macroeconomic and financial news relevant to gold"""
        try:
            result = self.news_database[:limit]
            return {
                "success": True,
                "news": result,
                "count": len(result)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # --- Model Context Protocol Unified Interface ---
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executes tool requests dynamically via string labels"""
        args = arguments or {}
        if tool_name == "get_historical_prices":
            return self.get_historical_prices(limit=args.get("limit", 50))
        elif tool_name == "get_realtime_price":
            return self.get_realtime_price()
        elif tool_name == "get_macro_news":
            return self.get_macro_news(limit=args.get("limit", 5))
        else:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found on this MCP server."
            }
            
    def list_tools(self) -> List[Dict[str, Any]]:
        """Lists metadata of all registered tools"""
        return [
            {
                "name": "get_historical_prices",
                "description": "Fetches daily historical candles for XAUUSD including Open, High, Low, Close, and Volume.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Number of days to retrieve (max 70)"}
                    }
                }
            },
            {
                "name": "get_realtime_price",
                "description": "Returns current live bid, ask, price, and daily change metrics for XAUUSD.",
                "parameters": {}
            },
            {
                "name": "get_macro_news",
                "description": "Returns the latest macroeconomic news headlines, details, and initial sentiments affecting gold markets.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Number of news articles to retrieve"}
                    }
                }
            }
        ]
