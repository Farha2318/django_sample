import json
import asyncio
import requests
from channels.generic.websocket import AsyncWebsocketConsumer

class CryptoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("✅ WebSocket connected")
        await self.accept()
        self.is_connected = True
        asyncio.create_task(self.send_prices())

    async def disconnect(self, close_code):
        self.is_connected = False
        print("❌ WebSocket disconnected")

    async def send_prices(self):
        while self.is_connected:
            try:
                prices = self.fetch_prices()
                print("⏳ Sending prices:", prices)
                await self.send(text_data=json.dumps(prices))
            except Exception as e:
                print("❌ Error sending prices:", e)
            await asyncio.sleep(5)

    def fetch_prices(self):
        symbols = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT']
        result = {}
        for symbol in symbols:
            url = f"https://api.coindcx.com/exchange/ticker"
            try:
                res = requests.get(url)
                data = res.json()
                for item in data:
                    if item['market'] == symbol:
                        result[symbol] = item['last_price']
            except Exception as e:
                result[symbol] = "Error"
        return result
