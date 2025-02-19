from flask import Blueprint, render_template, jsonify, Response, stream_with_context
from flask_login import login_required
from .utils import get_volatility_price, subscribe_to_price
import json
import asyncio

core_bp = Blueprint("core", __name__)

@core_bp.route("/")
@login_required
def home():
    """Render the homepage"""
    return render_template("core/index.html")

@core_bp.route("/api/price", methods=["GET"])
def get_price():
    """Fetch the latest price"""
    price = get_volatility_price()
    return jsonify({"price": price})

@core_bp.route("/api/subscribe", methods=["GET"])
def subscribe():
    """Stream real-time price updates using SSE"""

    async def event_stream():
        async for price in subscribe_to_price():
            yield f"data: {json.dumps({'price': price})}\n\n"

    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")
