import re
import pandas as pd

def sanitize_formula(formula: str) -> str:
    """
    Sanitizes user/quant technical indicator formula to prevent code injection.
    Allows only pandas dataframe operations, basic math, and standard pandas methods.
    """
    if not formula:
        return ""
    
    # Strip whitespace
    formula = formula.strip()
    
    # Check for suspicious keywords that might indicate code injection
    blacklisted_keywords = [
        'import', 'eval', 'exec', 'os', 'sys', 'subprocess', 'builtins', 
        '__import__', 'getattr', 'setattr', 'globals', 'locals', 'open', 
        'read', 'write', 'socket', 'urllib', 'requests', 'shutil'
    ]
    
    for kw in blacklisted_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', formula):
            raise ValueError(f"Security Warning: Blacklisted keyword '{kw}' detected in formula.")
            
    # Allow only safe characters: alphanumeric, spaces, math symbols, parenthesis, brackets, dots, commas, underscores, and single/double quotes.
    safe_pattern = re.compile(r'^[a-zA-Z0-9\s\+\-\*\/\%\=\<\>\!\&\|\~\.\,\[\]\(\)\_\'\"]+$')
    if not safe_pattern.match(formula):
        raise ValueError("Security Warning: Formula contains illegal characters.")
        
    return formula

def compact_market_data(df: pd.DataFrame, keep_last_n: int = 5) -> dict:
    """
    Compacts large historical market data to fit within LLM context window limits.
    Returns general stats and only the last few rows.
    """
    if df.empty:
        return {"status": "empty", "records": [], "summary": {}}
        
    # Standard statistics
    summary = {
        "count": len(df),
        "min_price": float(df['close'].min()) if 'close' in df.columns else 0.0,
        "max_price": float(df['close'].max()) if 'close' in df.columns else 0.0,
        "avg_price": float(df['close'].mean()) if 'close' in df.columns else 0.0,
        "start_date": str(df.index[0]) if isinstance(df.index, pd.DatetimeIndex) else str(df.iloc[0].get('timestamp', '')),
        "end_date": str(df.index[-1]) if isinstance(df.index, pd.DatetimeIndex) else str(df.iloc[-1].get('timestamp', ''))
    }
    
    # Calculate simple trend direction (Start Close vs End Close)
    if 'close' in df.columns:
        start_val = df.iloc[0]['close']
        end_val = df.iloc[-1]['close']
        change = end_val - start_val
        change_pct = (change / start_val) * 100 if start_val != 0 else 0
        summary["price_change"] = float(change)
        summary["price_change_pct"] = float(change_pct)
        summary["overall_trend"] = "BULLISH" if change > 0 else "BEARISH" if change < 0 else "NEUTRAL"
        
    # Get last N records as simple dict list
    recent_records = df.tail(keep_last_n).reset_index().to_dict(orient='records')
    for record in recent_records:
        # Convert timestamp or pandas timestamps to string representation
        for k, v in record.items():
            if hasattr(v, 'isoformat'):
                record[k] = v.isoformat()
            elif isinstance(v, float) and pd.isna(v):
                record[k] = None
                
    return {
        "status": "success",
        "summary": summary,
        "recent_records": recent_records
    }
