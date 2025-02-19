import asyncio
import json
import logging
import websockets

DERIV_API_URL = "wss://ws.deriv.com/websockets/v3"
APP_ID = 1234  # Replace with your Deriv app ID
logging.basicConfig(level=logging.INFO)

async def fetch_volatility_price():
    """Fetch the latest Volatility 100 (1s) Index price from Deriv API"""
    try:
        async with websockets.connect(DERIV_API_URL) as websocket:
            request = {
                "ticks": "R_100",  # Volatility 100 (1s) Index symbol
                "subscribe": 1
            }
            await websocket.send(json.dumps(request))

            while True:
                response = await websocket.recv()
                data = json.loads(response)
                if "tick" in data:
                    return data["tick"]["quote"]
    except websockets.exceptions.WebSocketException as e:
        logging.error(f"WebSocket error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def get_volatility_price():
    """Sync wrapper for Flask to fetch WebSocket data"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_volatility_price())

# Optimized Subscription function
async def subscribe_to_price():
    """Subscribe to Volatility 100 (1s) Index and yield live data"""
    try:
        async with websockets.connect(DERIV_API_URL) as websocket:
            request = {
                "ticks": "R_100",
                "subscribe": 1
            }
            await websocket.send(json.dumps(request))

            async for message in websocket:
                data = json.loads(message)
                if "tick" in data:
                    yield data["tick"]["quote"]
    except websockets.exceptions.WebSocketException as e:
        logging.error(f"Subscription error: {e}")
