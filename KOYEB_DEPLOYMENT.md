# Koyeb Deployment Guide

This guide will help you deploy the HTTPS-to-HTTP proxy to Koyeb in minutes.

## Prerequisites

- Koyeb account (sign up at https://app.koyeb.com)
- GitHub account with this repository
- Your VPS backend URL (e.g., `http://127.0.0.1:81`)

## Step 1: Push to GitHub

Make sure your code is pushed to GitHub:

```bash
git add .
git commit -m "Initial commit: FastAPI HTTPS-to-HTTP proxy"
git push origin main
```

## Step 2: Connect to Koyeb

### Option A: Using Koyeb Dashboard (Recommended)

1. **Log in to Koyeb**: https://app.koyeb.com
2. **Create a new App**:
   - Click "Create App" or "Create Web Service"
3. **Select GitHub**:
   - Click "GitHub" as the deployment method
   - Authorize GitHub access
   - Select your `Koyeb-Broker-https-http-https-` repository
   - Select branch: `main`
4. **Configure the Service**:
   - **Service name**: `https-http-proxy`
   - **Builder**: Select "Buildpack" (Koyeb auto-detects Python)
5. **Build Configuration**:
   - Koyeb will auto-detect your Procfile
   - Python version: should auto-detect from code
6. **Environment Variables**:
   - Click "Env" or "Environment variables"
   - Add these variables:
     ```
     BACKEND_URL=http://YOUR_VPS_IP:81
     BACKEND_TIMEOUT=30
     ```
   - Replace `YOUR_VPS_IP` with your actual VPS IP (e.g., `127.123.45.23`)

7. **Ports & Exposure**:
   - HTTP port: `8000` (auto-detected from Procfile)
   - Enable public exposure

8. **Deploy**:
   - Click "Create Service"
   - Wait for deployment (usually 1-2 minutes)

### Option B: Using Koyeb CLI

```bash
# Install Koyeb CLI first (if not already installed)
# https://koye.sb/docs/cli/getting-started

# Deploy the app
koyeb app create https-http-proxy \
  --git github.com/YOUR_USERNAME/Koyeb-Broker-https-http-https- \
  --git-branch main \
  --buildpack \
  --env BACKEND_URL=http://YOUR_VPS_IP:81 \
  --env BACKEND_TIMEOUT=30
```

## Step 3: Verify Deployment

Once deployed, you'll get a Koyeb URL like: `https://https-http-proxy-<username>.koyeb.app`

### Test your deployment:

```bash
# Health check
curl https://https-http-proxy-<username>.koyeb.app/health

# Check backend status
curl https://https-http-proxy-<username>.koyeb.app/api/backend-status
```

Expected response:
```json
{"status": "healthy", "proxy": "active"}
```

## Step 4: Update Your Frontend

In your Vercel frontend, replace backend calls:

### Before (❌ HTTPS error):
```javascript
// This will fail due to mixed content (HTTPS to HTTP)
fetch('http://127.123.45.23:81/api/users')
```

### After (✅ Works):
```javascript
// Now you call through the proxy (HTTPS to HTTPS)
fetch('https://https-http-proxy-<username>.koyeb.app/api/users')
```

### React Example:
```javascript
// In your React component
const API_URL = 'https://https-http-proxy-<username>.koyeb.app';

useEffect(() => {
  const fetchData = async () => {
    const response = await fetch(`${API_URL}/api/users`);
    const data = await response.json();
    setUsers(data);
  };
  
  fetchData();
}, []);
```

### Next.js Example:
```javascript
// .env.local (or environment variables in Vercel)
NEXT_PUBLIC_PROXY_URL=https://https-http-proxy-<username>.koyeb.app
```

```javascript
// In your API route or component
const proxyUrl = process.env.NEXT_PUBLIC_PROXY_URL;
const response = await fetch(`${proxyUrl}/api/users`);
```

## Step 5: Monitor & Manage

### View Logs:
```bash
# Using Koyeb dashboard:
# - Go to your app
# - Click "Logs"
# - Watch real-time logs

# Using CLI:
koyeb service logs https-http-proxy
```

### Update Environment Variables:
1. Go to your Koyeb app dashboard
2. Click "Settings" → "Environment"
3. Edit variables as needed
4. Click "Deploy" to redeploy with new variables

### Stop/Start Service:
```bash
# Using CLI:
koyeb service stop https-http-proxy
koyeb service start https-http-proxy
```

## Troubleshooting

### Issue: "Backend unreachable"
**Solution**: 
- Verify VPS IP and port are correct
- Check firewall rules on your VPS allow connections from Koyeb
- Check if your VPS backend is running

### Issue: CORS errors in browser
**Solution**:
- The proxy should handle CORS automatically
- Check browser console for specific error
- Verify Koyeb app is running (check logs)

### Issue: Timeout errors
**Solution**:
- Increase `BACKEND_TIMEOUT` environment variable
- Check VPS backend response time
- Ensure VPS is accessible from Koyeb region

### Issue: Deployment fails
**Solution**:
- Check that `Procfile` exists in root directory
- Verify `requirements.txt` is in root directory
- Check Koyeb deployment logs for errors
- Ensure GitHub access is authorized

## Performance Optimization

### Koyeb Instance Selection:
- Default instance size should be fine for most use cases
- If you get slowdowns, upgrade instance size in dashboard

### Example Production Update:
```bash
# Environment variables for production
BACKEND_URL=http://YOUR_ACTUAL_VPS:81
BACKEND_TIMEOUT=60  # Longer timeout for stability
```

## Security Checkpoints

✅ Verify before going live:
- [ ] HTTPS enabled on Koyeb (automatic)
- [ ] BACKEND_URL is correct
- [ ] Health check passes: `/health`
- [ ] Backend status passes: `/api/backend-status`
- [ ] Frontend can call proxy without CORS errors
- [ ] VPS firewall allows Koyeb → VPS communication

## Next Steps

1. ✅ Deploy to Koyeb
2. ✅ Update frontend URLs
3. ✅ Test all API endpoints
4. ✅ Monitor logs in Koyeb dashboard
5. ✅ Set up alerts (optional)

## Support

- Koyeb Docs: https://koye.sb/docs
- FastAPI Docs: https://fastapi.tiangolo.com/
- GitHub Issues: Create an issue in this repository

---

**You're all set! 🚀** Your HTTPS → HTTP proxy is now running on Koyeb!
