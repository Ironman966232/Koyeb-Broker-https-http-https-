# Koyeb HTTPS-to-HTTP Proxy Broker

A FastAPI-based proxy server that converts HTTPS requests to HTTP, allowing your Vercel frontend to securely communicate with an HTTP-only backend on your VPS.

## Problem Solved

- **Frontend**: Hosted on Vercel (HTTPS)
- **Backend**: Hosted on VPS (HTTP only, port 81)
- **Challenge**: HTTPS → HTTP communication blocked by browser security
- **Solution**: This proxy acts as the bridge, handling HTTPS termination and forwarding to your HTTP backend

## How It Works

```
Vercel Frontend (HTTPS)
          ↓
    Browser Request (HTTPS)
          ↓
    Koyeb Proxy (This App)
          ↓
    VPS Backend (HTTP)
          ↓
    Response returned to Vercel
```

## Features

✅ Forwards all HTTP methods (GET, POST, PUT, DELETE, PATCH)  
✅ Preserves headers and query parameters  
✅ CORS support enabled  
✅ Health check endpoints  
✅ Backend status monitoring  
✅ Comprehensive logging  
✅ Request timeout handling  
✅ X-Forwarded headers for backend context  

## Installation & Setup

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo>
cd Koyeb-Broker-https-http-https-
```

2. **Create Python virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your VPS backend URL
nano .env
```

5. **Run locally**
```bash
python main.py
# Or with uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The proxy will be available at `http://localhost:8000`

### Deployment on Koyeb

#### Method 1: Using Koyeb Dashboard

1. **Connect your Git repository** to Koyeb
2. **Add Environment Variables** in Koyeb settings:
   ```
   BACKEND_URL=http://127.0.0.1:81
   BACKEND_TIMEOUT=30
   ```
3. **Set the Procfile** as your startup command (Koyeb auto-detects Procfile)
4. **Deploy**

#### Method 2: Using Koyeb CLI

```bash
koyeb app create koyeb-https-http-proxy \
  --git github.com/<your-username>/Koyeb-Broker-https-http-https- \
  --git-branch main \
  --env BACKEND_URL=http://127.0.0.1:81 \
  --env BACKEND_TIMEOUT=30 \
  --ports 8000:http
```

## Usage

### From Your Vercel Frontend

Instead of calling your backend directly:
```javascript
// ❌ Old (HTTPS error):
fetch('http://127.0.0.1:81/api/endpoint')

// ✅ New (through proxy):
fetch('https://your-koyeb-app.koyeb.app/api/endpoint')
```

### Example Requests

**GET Request**
```bash
curl https://your-koyeb-app.koyeb.app/api/users
```

**POST Request**
```bash
curl -X POST \
  https://your-koyeb-app.koyeb.app/api/data \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### Health Check

Check if proxy is running:
```bash
curl https://your-koyeb-app.koyeb.app/health
```

Response: `{"status": "healthy", "proxy": "active"}`

### Backend Status

Check if backend is reachable:
```bash
curl https://your-koyeb-app.koyeb.app/api/backend-status
```

## Configuration

Edit `.env` file with the following variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | `http://127.0.0.1:81` | Your VPS backend URL (must be HTTP) |
| `BACKEND_TIMEOUT` | `30` | Request timeout in seconds |
| `PORT` | `8000` | Proxy server port (Koyeb sets this automatically) |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/*` | ANY | Proxy all requests to backend |
| `/health` | GET | Health check |
| `/api/backend-status` | GET | Backend connectivity status |

## CORS Configuration

The proxy allows requests from all origins by default. To restrict to specific origins, modify `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-app.vercel.app"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Headers Forwarded to Backend

The proxy adds these headers for backend context:
- `X-Forwarded-For`: Client IP address
- `X-Forwarded-Proto`: Always `https` (original protocol)
- `X-Forwarded-Host`: Original host header
- All other headers (except hop-by-hop headers)

## Error Handling

| Status Code | Meaning |
|-------------|---------|
| `502` | Backend connection error |
| `504` | Backend request timeout |
| `4xx` | Client error (from backend) |
| `5xx` | Server error (from backend) |

## Troubleshooting

### Backend unreachable error
```
Error proxying request to http://127.0.0.1:81/...
```
**Solution**: Verify your `BACKEND_URL` is correct and your VPS is accessible from Koyeb.

### CORS errors in browser
Ensure the proxy returns correct CORS headers. These should be auto-added by the middleware.

### SSL certificate errors
The proxy uses `verify=False` for backend connections. This is intentional for HTTP backends.

## Architecture

```
┌──────────────────┐
│ Vercel Frontend  │
│ (HTTPS)          │
└────────┬─────────┘
         │ HTTPS Request
         ▼
┌──────────────────────┐
│  Koyeb Proxy         │
│ (FastAPI + HTTPX)    │
│ - Receives HTTPS     │
│ - Forwards HTTP      │
│ - Returns response   │
└────────┬─────────────┘
         │ HTTP Request
         ▼
┌──────────────────┐
│ VPS Backend      │
│ (HTTP Port 81)   │
└──────────────────┘
```

## Files Structure

```
.
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Procfile               # Koyeb deployment config
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Security Notes

⚠️ **Important**:
- This proxy is designed specifically for HTTP backends without SSL
- In production, ensure your VPS backend is only accessible from Koyeb
- Consider using firewall rules or network restrictions
- Never expose sensitive credentials in environment variables
- Always use HTTPS for frontend-to-proxy communication (Koyeb provides this automatically)

## Performance

- Async request handling with HTTPX
- Connection pooling for efficient resource usage
- Configurable timeouts
- Suitable for moderate to high traffic loads

## License

MIT

## Support

For issues or questions, refer to:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Koyeb Documentation](https://koye.sb/docs)
- [HTTPX Documentation](https://www.python-httpx.org/)
