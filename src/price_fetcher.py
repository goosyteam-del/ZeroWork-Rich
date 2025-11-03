"""
Price Fetcher Module
Fetches real-time cryptocurrency prices from CoinGecko API
"""

import requests
import time
from typing import Dict, List
from src.config import COINGECKO_API, TOKEN_PRICE_IDS
from src.logger_config import setup_logger

logger = setup_logger("PriceFetcher")


class PriceFetcher:
    """Fetch real-time cryptocurrency prices"""
    
    def __init__(self):
        """Initialize price fetcher"""
        self.cache = {}
        self.cache_duration = 60  # Cache for 60 seconds
        self.last_fetch_time = {}
    
    def get_price(self, token_symbol: str) -> float:
        """
        Get current USD price for a token
        
        Args:
            token_symbol: Token symbol (e.g., 'ETH', 'BTC')
            
        Returns:
            Current price in USD, or 0 if not found
        """
        # Check cache first
        if token_symbol in self.cache:
            if time.time() - self.last_fetch_time.get(token_symbol, 0) < self.cache_duration:
                return self.cache[token_symbol]
        
        # Get CoinGecko ID for token
        token_id = TOKEN_PRICE_IDS.get(token_symbol.upper())
        if not token_id:
            logger.warning(f"Token {token_symbol} not found in price mapping")
            return 0.0
        
        try:
            # Fetch from CoinGecko
            url = f"{COINGECKO_API}/simple/price"
            params = {
                "ids": token_id,
                "vs_currencies": "usd"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            price = data.get(token_id, {}).get("usd", 0.0)
            
            # Update cache
            self.cache[token_symbol] = price
            self.last_fetch_time[token_symbol] = time.time()
            
            logger.debug(f"Fetched price for {token_symbol}: ${price:.2f}")
            return price
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching price for {token_symbol}: {str(e)}")
            # Return cached value if available
            return self.cache.get(token_symbol, 0.0)
    
    def get_multiple_prices(self, token_symbols: List[str]) -> Dict[str, float]:
        """
        Get prices for multiple tokens in one API call
        
        Args:
            token_symbols: List of token symbols
            
        Returns:
            Dictionary mapping token symbols to prices
        """
        # Get CoinGecko IDs
        token_ids = []
        symbol_to_id = {}
        
        for symbol in token_symbols:
            token_id = TOKEN_PRICE_IDS.get(symbol.upper())
            if token_id:
                token_ids.append(token_id)
                symbol_to_id[token_id] = symbol.upper()
        
        if not token_ids:
            return {}
        
        try:
            # Fetch from CoinGecko
            url = f"{COINGECKO_API}/simple/price"
            params = {
                "ids": ",".join(token_ids),
                "vs_currencies": "usd"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Map back to symbols and update cache
            prices = {}
            for token_id, symbol in symbol_to_id.items():
                price = data.get(token_id, {}).get("usd", 0.0)
                prices[symbol] = price
                self.cache[symbol] = price
                self.last_fetch_time[symbol] = time.time()
            
            logger.info(f"Fetched prices for {len(prices)} tokens")
            return prices
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching multiple prices: {str(e)}")
            # Return cached values
            return {symbol: self.cache.get(symbol, 0.0) for symbol in token_symbols}
    
    def clear_cache(self):
        """Clear price cache"""
        self.cache.clear()
        self.last_fetch_time.clear()
        logger.info("Price cache cleared")


# Global price fetcher instance
_price_fetcher = None

def get_price_fetcher() -> PriceFetcher:
    """Get global price fetcher instance"""
    global _price_fetcher
    if _price_fetcher is None:
        _price_fetcher = PriceFetcher()
    return _price_fetcher
