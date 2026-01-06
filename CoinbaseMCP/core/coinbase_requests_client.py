# core/coinbase_requests_client.py

from typing import Optional, Dict, List, Any
import requests
from auth.jwt_generator import build_jwt
from requests.adapters import HTTPAdapter, Retry

BASE_URL = "https://api.coinbase.com/api/v3/brokerage"
PUBLIC_BASE_URL = "https://api.coinbase.com/api/v3/brokerage/market"

# Setup requests session with retries
session = requests.Session()
retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

def _headers(method: str, path: str) -> dict:
    """
    Generate JWT token with the correct URI path for the specific endpoint.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        path: The full API path starting with /api/v3/brokerage/...
    """
    jwt = build_jwt(method=method, path=path)
    return {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }

def _public_headers() -> dict:
    """Headers for public endpoints (no authentication required)."""
    return {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"  # Bypass 1s cache for real-time data
    }

def _get(url: str, path: str, params: dict = None, is_public: bool = False):
    headers = _public_headers() if is_public else _headers("GET", path)
    response = session.get(url, headers=headers, params=params)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code, "body": response.text}

def _post(url: str, path: str, data: dict = None):
    headers = _headers("POST", path)
    response = session.post(url, headers=headers, json=data)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code, "body": response.text}

def _put(url: str, path: str, data: dict = None):
    headers = _headers("PUT", path)
    response = session.put(url, headers=headers, json=data)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code, "body": response.text}

def _delete(url: str, path: str, data: dict = None):
    headers = _headers("DELETE", path)
    response = session.delete(url, headers=headers, json=data)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code, "body": response.text}

# =============================================================================
# ACCOUNT MANAGEMENT ENDPOINTS
# =============================================================================

def list_accounts(limit: int = 100):
    """List all accounts (portfolio overview) from Coinbase Advanced Trade API."""
    path = "/api/v3/brokerage/accounts"
    url = f"{BASE_URL}/accounts"
    all_accounts = []
    cursor = None
    while True:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        result = _get(url, path, params)
        if "accounts" in result:
            all_accounts.extend(result["accounts"])
        else:
            break
        cursor = result.get("cursor")
        if not result.get("has_next"):
            break
    return {"accounts": all_accounts}

def get_account(account_id: str):
    """Get a specific account by account_id (UUID)."""
    path = f"/api/v3/brokerage/accounts/{account_id}"
    url = f"{BASE_URL}/accounts/{account_id}"
    return _get(url, path)

# =============================================================================
# ORDER MANAGEMENT ENDPOINTS
# =============================================================================

def create_order(client_order_id: str, product_id: str, side: str, order_configuration: dict, retail_portfolio_id: Optional[str] = None, **kwargs):
    """Create an order on Coinbase Advanced Trade API."""
    path = "/api/v3/brokerage/orders"
    url = f"{BASE_URL}/orders"
    payload = {
        "client_order_id": client_order_id,
        "product_id": product_id,
        "side": side.upper(),
        "order_configuration": order_configuration,
    }
    if retail_portfolio_id:
        payload["retail_portfolio_id"] = retail_portfolio_id
    payload.update(kwargs)
    return _post(url, path, data=payload)

def cancel_orders(order_ids: List[str]):
    """Cancel multiple orders at once."""
    path = "/api/v3/brokerage/orders/batch_cancel"
    url = f"{BASE_URL}/orders/batch_cancel"
    payload = {"order_ids": order_ids}
    return _post(url, path, data=payload)

def list_orders(product_id: Optional[str] = None, order_status: Optional[str] = None, limit: int = 100, start_date: Optional[str] = None, end_date: Optional[str] = None):
    """List historical orders with optional filtering."""
    path = "/api/v3/brokerage/orders/historical/batch"
    url = f"{BASE_URL}/orders/historical/batch"
    params = {"limit": limit}
    if product_id:
        params["product_id"] = product_id
    if order_status:
        params["order_status"] = order_status
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return _get(url, path, params)

def get_historical_fills(product_id: Optional[str] = None, limit: int = 100):
    """Get historical fills (completed trades) from Coinbase Advanced Trade API."""
    path = "/api/v3/brokerage/orders/historical/fills"
    url = f"{BASE_URL}/orders/historical/fills"
    params = {}
    if product_id:
        params["product_id"] = product_id
    if limit:
        params["limit"] = limit
    return _get(url, path, params)

def get_order(order_id: str):
    """Get a specific order by order_id."""
    path = f"/api/v3/brokerage/orders/historical/{order_id}"
    url = f"{BASE_URL}/orders/historical/{order_id}"
    return _get(url, path)

def preview_order(product_id: str, side: str, order_configuration: dict, commission_rate: Optional[dict] = None):
    """Preview an order before placing it."""
    path = "/api/v3/brokerage/orders/preview"
    url = f"{BASE_URL}/orders/preview"
    payload = {
        "product_id": product_id,
        "side": side.upper(),
        "order_configuration": order_configuration
    }
    if commission_rate:
        payload["commission_rate"] = commission_rate
    return _post(url, path, data=payload)

# =============================================================================
# MARKET DATA ENDPOINTS
# =============================================================================

def get_best_bid_ask(product_ids: List[str]):
    """Get best bid/ask for specified products."""
    path = "/api/v3/brokerage/best_bid_ask"
    url = f"{BASE_URL}/best_bid_ask"
    params = {"product_ids": ",".join(product_ids)}
    return _get(url, path, params)

def get_product_book(product_id: str, limit: Optional[int] = None):
    """Get order book for a product."""
    path = f"/api/v3/brokerage/product_book"
    url = f"{BASE_URL}/product_book"
    params = {"product_id": product_id}
    if limit is not None and isinstance(limit, int) and limit > 0:
        params["limit"] = limit
    return _get(url, path, params=params)

def list_products(product_type: Optional[str] = None, product_ids: Optional[List[str]] = None, contract_expiry_type: Optional[str] = None):
    """List all available products."""
    path = "/api/v3/brokerage/products"
    url = f"{BASE_URL}/products"
    params = {}
    if product_type:
        params["product_type"] = product_type
    if product_ids:
        params["product_ids"] = ",".join(product_ids)
    if contract_expiry_type:
        params["contract_expiry_type"] = contract_expiry_type
    return _get(url, path, params)

def get_product(product_id: str):
    """Get details for a specific product."""
    path = f"/api/v3/brokerage/products/{product_id}"
    url = f"{BASE_URL}/products/{product_id}"
    return _get(url, path)

def get_candles(product_id: str, start: str, end: str, granularity: str):
    """Get product candles (OHLCV data)."""
    path = f"/api/v3/brokerage/products/{product_id}/candles"
    url = f"{BASE_URL}/products/{product_id}/candles"
    params = {
        "start": start,
        "end": end,
        "granularity": granularity
    }
    return _get(url, path, params)

def get_market_trades(product_id: str, limit: int = 100):
    """Get recent market trades for a product."""
    path = f"/api/v3/brokerage/products/{product_id}/ticker"
    url = f"{BASE_URL}/products/{product_id}/ticker"
    return _get(url, path, {"limit": limit})

# =============================================================================
# TRANSACTION & FEES ENDPOINTS
# =============================================================================

def get_transactions_summary(start_date: Optional[str] = None, end_date: Optional[str] = None, user_native_currency: Optional[str] = None, product_type: Optional[str] = None, contract_expiry_type: Optional[str] = None):
    """Get transaction summary."""
    path = "/api/v3/brokerage/transaction_summary"
    url = f"{BASE_URL}/transaction_summary"
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if user_native_currency:
        params["user_native_currency"] = user_native_currency
    if product_type:
        params["product_type"] = product_type
    if contract_expiry_type:
        params["contract_expiry_type"] = contract_expiry_type
    return _get(url, path, params)

# =============================================================================
# CONVERT ENDPOINTS
# =============================================================================

def create_convert_quote(from_account: str, to_account: str, amount: str):
    """Create a convert quote."""
    path = "/api/v3/brokerage/convert/quote"
    url = f"{BASE_URL}/convert/quote"
    payload = {
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount
    }
    return _post(url, path, data=payload)

def commit_convert_trade(trade_id: str, from_account: str, to_account: str, amount: str):
    """Commit a convert trade."""
    path = f"/api/v3/brokerage/convert/{trade_id}"
    url = f"{BASE_URL}/convert/{trade_id}"
    payload = {
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount
    }
    return _post(url, path, data=payload)

def get_convert_trade(trade_id: str, from_account: str, to_account: str):
    """Get details of a convert trade."""
    path = f"/api/v3/brokerage/convert/{trade_id}"
    url = f"{BASE_URL}/convert/{trade_id}"
    params = {
        "from_account": from_account,
        "to_account": to_account
    }
    return _get(url, path, params)

# =============================================================================
# PUBLIC ENDPOINTS (NO AUTHENTICATION REQUIRED)
# =============================================================================

def get_server_time():
    """Get server time."""
    path = "/api/v3/brokerage/time"
    url = f"{BASE_URL}/time"
    return _get(url, path, is_public=True)

def get_public_product_book(product_id: str, limit: Optional[int] = None):
    """Get public product book."""
    url = f"{PUBLIC_BASE_URL}/product_book"
    params = {"product_id": product_id}
    if limit:
        params["limit"] = limit
    return _get(url, "", params, is_public=True)

def list_public_products(product_type: Optional[str] = None, product_ids: Optional[List[str]] = None):
    """List public products."""
    url = f"{PUBLIC_BASE_URL}/products"
    params = {}
    if product_type:
        params["product_type"] = product_type
    if product_ids:
        params["product_ids"] = ",".join(product_ids)
    return _get(url, "", params, is_public=True)

def get_public_product(product_id: str):
    """Get public product details."""
    url = f"{PUBLIC_BASE_URL}/products/{product_id}"
    return _get(url, "", is_public=True)

def get_public_candles(product_id: str, start: str, end: str, granularity: str):
    """Get public product candles."""
    url = f"{PUBLIC_BASE_URL}/products/{product_id}/candles"
    params = {
        "start": start,
        "end": end,
        "granularity": granularity
    }
    return _get(url, "", params, is_public=True)

def get_public_market_trades(product_id: str, limit: int = 100):
    """Get public market trades."""
    url = f"{PUBLIC_BASE_URL}/products/{product_id}/ticker"
    params = {"limit": limit}
    return _get(url, "", params, is_public=True)

# =============================================================================
# PORTFOLIO MANAGEMENT ENDPOINTS
# =============================================================================

def list_portfolios():
    """List all portfolios."""
    path = "/api/v3/brokerage/portfolios"
    url = f"{BASE_URL}/portfolios"
    return _get(url, path)

def create_portfolio(name: str):
    """Create a new portfolio."""
    path = "/api/v3/brokerage/portfolios"
    url = f"{BASE_URL}/portfolios"
    payload = {"name": name}
    return _post(url, path, data=payload)

def get_portfolio_breakdown(portfolio_uuid: str):
    """Get breakdown of a specific portfolio."""
    path = f"/api/v3/brokerage/portfolios/{portfolio_uuid}"
    url = f"{BASE_URL}/portfolios/{portfolio_uuid}"
    return _get(url, path)

def move_portfolio_funds(funds: dict, source_portfolio_uuid: str, target_portfolio_uuid: str):
    """Move funds between portfolios."""
    path = "/api/v3/brokerage/portfolios/move_funds"
    url = f"{BASE_URL}/portfolios/move_funds"
    payload = {
        "funds": funds,
        "source_portfolio_uuid": source_portfolio_uuid,
        "target_portfolio_uuid": target_portfolio_uuid
    }
    return _post(url, path, data=payload)

def edit_portfolio(portfolio_uuid: str, name: str):
    """Edit a portfolio's name."""
    path = f"/api/v3/brokerage/portfolios/{portfolio_uuid}"
    url = f"{BASE_URL}/portfolios/{portfolio_uuid}"
    payload = {"name": name}
    return _put(url, path, data=payload)

def delete_portfolio(portfolio_uuid: str):
    """Delete a portfolio."""
    path = f"/api/v3/brokerage/portfolios/{portfolio_uuid}"
    url = f"{BASE_URL}/portfolios/{portfolio_uuid}"
    return _delete(url, path)

# =============================================================================
# PAYMENT METHODS ENDPOINTS
# =============================================================================

def list_payment_methods():
    """List all payment methods."""
    path = "/api/v3/brokerage/payment_methods"
    url = f"{BASE_URL}/payment_methods"
    return _get(url, path)

def get_payment_method(payment_method_id: str):
    """Get a specific payment method by ID."""
    path = f"/api/v3/brokerage/payment_methods/{payment_method_id}"
    url = f"{BASE_URL}/payment_methods/{payment_method_id}"
    return _get(url, path)

# =============================================================================
# API KEY PERMISSIONS
# =============================================================================

def get_api_key_permissions():
    """Get API key permissions."""
    path = "/api/v3/brokerage/key_permissions"
    url = f"{BASE_URL}/key_permissions"
    return _get(url, path)
