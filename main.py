"""
FastAPI HTTPS-to-HTTP Proxy Server
This proxy accepts HTTPS requests from your frontend and forwards them to your HTTP backend.
"""

import os
import logging
import json
from typing import Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="HTTPS-to-HTTP Proxy",
    description="Proxy server that converts HTTPS requests to HTTP for backend",
    version="1.0.0"
)

# Add CORS middleware to allow requests from your Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict this to your Vercel domain in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration from environment variables
BACKEND_URL = os.getenv("BACKEND_URL", "http://159.195.146.143:81")
BACKEND_TIMEOUT = int(os.getenv("BACKEND_TIMEOUT", "30"))

# Remove trailing slash from backend URL if present
BACKEND_URL = BACKEND_URL.rstrip("/")

logger.info(f"Proxy configured to forward requests to: {BACKEND_URL}")


def get_forwarded_headers(request: Request) -> dict:
    """
    Extract and prepare headers to forward to the backend.
    Remove hop-by-hop headers that shouldn't be forwarded.
    """
    hop_by_hop_headers = {
        "connection",
        "keep-alive",
        "transfer-encoding",
        "upgrade",
        "te",
        "trailer",
        "host",
        "content-encoding",
        "content-length",
    }

    headers = {}
    for key, value in request.headers.items():
        if key.lower() not in hop_by_hop_headers:
            headers[key] = value

    # Add X-Forwarded headers for backend context
    headers["X-Forwarded-For"] = request.client.host if request.client else "unknown"
    headers["X-Forwarded-Proto"] = "https"  # Original protocol from client
    headers["X-Forwarded-Host"] = request.headers.get("host", "unknown")

    return headers


async def proxy_request(
    request: Request,
    path: str,
    method: str,
) -> Response:
    """
    Generic function to proxy requests to the backend.
    """
    # Construct the full backend URL
    backend_url = f"{BACKEND_URL}/{path}"

    # Prepare the request body
    body = None
    if method in ["POST", "PUT", "PATCH"]:
        body = await request.body()

    # Get forwarded headers
    forwarded_headers = get_forwarded_headers(request)

    # Preserve query parameters
    query_params = dict(request.query_params)

    logger.info(
        f"Proxying {method} request to {backend_url} with query: {query_params}"
    )

    try:
        async with httpx.AsyncClient(
            timeout=BACKEND_TIMEOUT,
            verify=False,  # SSL verification disabled for HTTP backend
        ) as client:
            backend_response = await client.request(
                method=method,
                url=backend_url,
                headers=forwarded_headers,
                content=body,
                params=query_params,
                follow_redirects=True,
            )

            # Create response with backend status code
            response_headers = {
                key: value
                for key, value in backend_response.headers.items()
                if key.lower() not in {"transfer-encoding", "content-encoding"}
            }

            # Add CORS headers to response
            response_headers["Access-Control-Allow-Origin"] = "*"
            response_headers["X-Proxy-By"] = "Koyeb-HTTPS-HTTP-Proxy"

            logger.info(f"Backend responded with status: {backend_response.status_code}")

            return Response(
                content=backend_response.content,
                status_code=backend_response.status_code,
                headers=response_headers,
            )

    except httpx.TimeoutException:
        logger.error(f"Timeout connecting to backend: {backend_url}")
        return JSONResponse(
            content={"error": "Backend request timeout"},
            status_code=504,
        )
    except Exception as e:
        logger.error(f"Error proxying request to {backend_url}: {str(e)}")
        return JSONResponse(
            content={"error": f"Proxy error: {str(e)}"},
            status_code=502,
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Koyeb monitoring.
    """
    return {"status": "healthy", "proxy": "active"}


@app.get("/api/backend-status")
async def backend_status():
    """
    Check if backend is reachable.
    """
    try:
        async with httpx.AsyncClient(timeout=5, verify=False) as client:
            response = await client.get(f"{BACKEND_URL}/health", follow_redirects=True)
            return {
                "backend": "reachable",
                "url": BACKEND_URL,
                "status_code": response.status_code,
            }
    except Exception as e:
        return {
            "backend": "unreachable",
            "url": BACKEND_URL,
            "error": str(e),
        }


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def proxy(request: Request, path: str):
    """
    Main proxy endpoint that forwards all HTTP methods to the backend.
    """
    method = request.method

    # Handle OPTIONS requests (CORS preflight)
    if method == "OPTIONS":
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
            },
        )

    return await proxy_request(request, path, method)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
