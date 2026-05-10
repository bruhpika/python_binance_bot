import hashlib
import hmac
import time
import requests
from urllib.parse import urlencode
from typing import Dict, Any
from .logging_config import get_logger

logger = get_logger(__name__)

class BinanceAPIError(Exception):
    """Exception raised when Binance returns a non-200 HTTP response or error JSON."""
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"BinanceAPIError(code={code}): {message}")

class BinanceClient:
    """Client for Binance Futures Testnet API."""
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    def place_order(self, params: dict) -> dict:
        """Places an order on Binance Futures."""
        params['timestamp'] = int(time.time() * 1000)
        
        # Sort params by key for determinism
        sorted_params = dict(sorted(params.items()))
        
        # Build query string
        query_string = urlencode(sorted_params)
        
        # Compute HMAC-SHA256 signature
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Append signature
        query_string += f"&signature={signature}"
        
        url = f"{self.base_url}/fapi/v1/order?{query_string}"
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        
        # Log request params without secret
        log_params = sorted_params.copy()
        logger.debug(f"Placing order with params: {log_params}")
        
        try:
            response = requests.post(url, headers=headers)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException during place_order: {e}")
            raise
            
        if response.status_code != 200:
            try:
                error_data = response.json()
                code = error_data.get('code', response.status_code)
                msg = error_data.get('msg', response.text)
            except ValueError:
                code = response.status_code
                msg = response.text
            
            logger.error(f"Binance API error: code={code}, msg={msg}")
            raise BinanceAPIError(code, msg)
            
        data = response.json()
        logger.info(f"Order placed successfully: {data}")
        return data
