"""Shared httpx client with connection pooling.

Reuses TCP connections across requests to eliminate per-request
TLS handshake overhead when calling Eigen AI APIs.
"""

import httpx

from app.config import settings

_client: httpx.AsyncClient | None = None


def get_http_client() -> httpx.AsyncClient:
    """Return a shared httpx.AsyncClient with connection pooling."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            timeout=httpx.Timeout(60.0, connect=10.0),
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=10,
                keepalive_expiry=30,
            ),
            http2=True,
        )
    return _client


async def close_http_client() -> None:
    """Close the shared client (call on app shutdown)."""
    global _client
    if _client is not None and not _client.is_closed:
        await _client.aclose()
        _client = None
