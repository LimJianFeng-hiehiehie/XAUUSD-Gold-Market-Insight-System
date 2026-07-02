import pandas as pd
import numpy as np
from typing import Dict, Any
from .security import sanitize_formula

def SMA(df: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.Series:
    """Calculates Simple Moving Average (SMA)"""
    return df[column].rolling(window=period).mean()

def EMA(df: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.Series:
    """Calculates Exponential Moving Average (EMA)"""
    return df[column].ewm(span=period, adjust=False).mean()

def RSI(df: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.Series:
    """Calculates Relative Strength Index (RSI) using Wilder's EMA smoothing"""
    delta = df[column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    # Use exponential moving average
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    
    # Avoid division by zero
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)  # Default neutral RSI for NaN rows

def MACD(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9, column: str = 'close') -> Dict[str, pd.Series]:
    """Calculates MACD indicators"""
    ema_fast = EMA(df, fast, column)
    ema_slow = EMA(df, slow, column)
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return {
        "macd": macd_line,
        "signal": signal_line,
        "hist": hist
    }

class QuantSandbox:
    """
    Executes technical formulas and indicators in a sandbox environment,
    ensuring security and access control over imports and evaluation context.
    """
    def __init__(self, data: pd.DataFrame):
        self.df = data.copy()
        
    def execute_indicator(self, name: str, formula: str) -> pd.Series:
        """
        Executes a user or agent-defined python expression safely and inserts the result
        as a new column into the sandbox data.
        
        Example formula: "SMA(df, 20) - SMA(df, 50)"
        """
        sanitized = sanitize_formula(formula)
        
        # Build strict execution context
        # We explicitly restrict global builtins and provide safe math and pandas symbols
        safe_globals = {
            "__builtins__": {
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "len": len,
                "float": float,
                "int": int,
                "str": str,
                "range": range,
                "list": list,
                "dict": dict
            },
            "pd": pd,
            "np": np,
            "df": self.df,
            "SMA": SMA,
            "EMA": EMA,
            "RSI": RSI,
            "MACD": MACD
        }
        
        try:
            # Evaluate expression in restricted globals environment
            result = eval(sanitized, safe_globals, {})
            
            if not isinstance(result, (pd.Series, np.ndarray, list)):
                raise TypeError(f"Formula evaluation did not return a pandas Series, returned {type(result)}")
                
            series_res = pd.Series(result, index=self.df.index)
            self.df[name] = series_res
            return series_res
            
        except Exception as e:
            raise RuntimeError(f"Sandbox Execution Error in formula '{formula}': {str(e)}")
            
    def get_dataframe(self) -> pd.DataFrame:
        """Returns the current state of sandbox dataframe with calculated columns"""
        return self.df
