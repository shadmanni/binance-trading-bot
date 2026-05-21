import os
from dotenv import load_dotenv

load_dotenv()


class BinanceFuturesClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_SECRET_KEY")

        if not self.api_key or not self.api_secret:
            raise ValueError("API credentials not found in .env")

        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })