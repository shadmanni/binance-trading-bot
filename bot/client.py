import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from typing import Dict, Any, Optional

from bot.logging_config import setup_logger

logger = setup_logger("binance_client")

BASE_URL = "https://demo-fapi.binance.com"


class BinanceClientError(Exception):
    """Raised when Binance returns an API-level error."""
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Binance API Error {code}: {message}")


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key    = api_key
        self.api_secret = api_secret
        self.session    = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #
    def _sign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params["timestamp"] = int(time.time() * 1000)
        query = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode(), query.encode(), hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url    = BASE_URL + endpoint
        signed = self._sign(params)
        logger.debug("POST %s | params: %s", url, {k: v for k, v in signed.items() if k != "signature"})
        try:
            resp = self.session.post(url, data=signed, timeout=10)
        except requests.exceptions.RequestException as exc:
            logger.error("Network error: %s", exc)
            raise

        logger.debug("Response [%s]: %s", resp.status_code, resp.text)

        data = resp.json()
        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            raise BinanceClientError(data["code"], data.get("msg", "Unknown error"))
        return data

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #
    def place_order(
        self,
        symbol:     str,
        side:       str,
        order_type: str,
        quantity:   float,
        price:      Optional[float] = None,
        time_in_force: str = "GTC",
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "symbol":   symbol,
            "side":     side,
            "type":     order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            params["price"]         = price
            params["timeInForce"]   = time_in_force
        elif order_type == "STOP_MARKET":
            params["stopPrice"]     = price

        return self._post("/fapi/v1/order", params)