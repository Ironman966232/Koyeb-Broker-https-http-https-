# Quick Start Guide

## 📋 What This Does

Converts HTTPS requests from your Vercel frontend to HTTP calls to your VPS backend.

```
Vercel (HTTPS) → Koyeb Proxy (This App) → VPS Backend (HTTP:81)
```

## 🚀 Deploy in 5 Minutes

### 1. **Update Configuration**
Edit `BACKEND_URL` in Koyeb environment variables:
```
BACKEND_URL=http://YOUR_VPS_IP:81
```

### 2. **Deploy to Koyeb**
- Connect GitHub repo to Koyeb
- Add environment variables
- Click "Deploy"

### 3. **Test**
```bash
curl https://your-koyeb-app.koyeb.app/health
# Response: {"status": "healthy", "proxy": "active"}
```

### 4. **Update Frontend**
**Old:**
```javascript
fetch('http://127.0.0.1:81/api/users')  // ❌ Fails
```

**New:**
```javascript
fetch('https://your-koyeb-app.koyeb.app/api/users')  // ✅ Works
```

## 📁 Project Structure

```
├── main.py                      # FastAPI proxy (the magic ✨)
├── requirements.txt             # Dependencies
├── Procfile                     # Koyeb deployment config
├── Dockerfile                   # Docker config
├── docker-compose.yml           # Local testing
├── .env.example                 # Environment template
├── example_client.py            # How to use the proxy
├── SETUP.md                     # Detailed setup guide
├── KOYEB_DEPLOYMENT.md          # Step-by-step deployment
└── QUICK_START.md              # This file
```

## 🧪 Test Locally

### Option 1: Direct Python
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export BACKEND_URL=http://YOUR_VPS_IP:81

# Run
python main.py
```

### Option 2: Docker
```bash
# Start proxy + test backend
docker-compose up
```

Access at: `http://localhost:8000`

## 🔗 API Endpoints

| URL | Purpose |
|-----|---------|
| `/{path}` | Proxy to any backend endpoint |
| `/health` | Health check |
| `/api/backend-status` | Check if backend is reachable |

## 📍 Example Workflow

1. **Frontend calls proxy** (from Vercel):
   ```javascript
   fetch('https://your-koyeb-app.koyeb.app/api/users')
   ```

2. **Proxy forwards to backend** (HTTP):
   ```
   GET http://YOUR_VPS_IP:81/api/users
   ```

3. **Backend responds**:
   ```json
   {"users": [...]}
   ```

4. **Proxy returns to frontend**:
   ```json
   {"users": [...]}
   ```

## ⚙️ Environment Variables

| Variable | Example | Notes |
|----------|---------|-------|
| `BACKEND_URL` | `http://123.45.67.89:81` | Your VPS backend HTTP URL |
| `BACKEND_TIMEOUT` | `30` | Request timeout in seconds |
| `PORT` | `8000` | Proxy port (auto on Koyeb) |

## ✅ Verification Checklist

```bash
# 1. Check proxy is running
curl https://your-koyeb-app.koyeb.app/health

# 2. Check backend is reachable
curl https://your-koyeb-app.koyeb.app/api/backend-status

# 3. Test a real API call
curl https://your-koyeb-app.koyeb.app/api/users
```

## 🎯 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Backend unreachable | Verify VPS IP and port in BACKEND_URL |
| CORS errors | Proxy adds headers automatically, check if frontend URL is correct |
| Timeout errors | Increase BACKEND_TIMEOUT in environment |
| HTTPS redirect errors | Make sure frontend calls HTTPS proxy URL, not HTTP |

## 📚 Full Documentation

- [Detailed Setup Guide](SETUP.md)
- [Koyeb Deployment Guide](KOYEB_DEPLOYMENT.md)
- [Example Client Code](example_client.py)

## 🆘 Still Need Help?

1. Check the logs: `https://app.koyeb.com > Your App > Logs`
2. Read [SETUP.md](SETUP.md) for detailed troubleshooting
3. Review [example_client.py](example_client.py) for usage examples

## 🎉 You're Ready!

Your HTTPS → HTTP proxy is ready to use. Go ahead and:
1. Deploy to Koyeb
2. Update your Vercel frontend URLs
3. Start making calls! 🚀
