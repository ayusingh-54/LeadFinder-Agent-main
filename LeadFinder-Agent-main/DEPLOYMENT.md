# 🚀 LeadFinder AI - Complete Deployment Guide

Deploy LeadFinder AI to **Vercel** (Frontend) and **Railway/Render** (Backend) using GitHub.

---

## 📋 Table of Contents

1. [Project Structure](#project-structure)
2. [Prerequisites](#prerequisites)
3. [Step 1: Prepare Your Code](#step-1-prepare-your-code)
4. [Step 2: Push to GitHub](#step-2-push-to-github)
5. [Step 3: Deploy Backend to Railway](#step-3-deploy-backend-to-railway)
6. [Step 4: Deploy Frontend to Vercel](#step-4-deploy-frontend-to-vercel)
7. [Step 5: Connect Frontend to Backend](#step-5-connect-frontend-to-backend)
8. [Alternative: Deploy Backend to Render](#alternative-deploy-backend-to-render)
9. [Troubleshooting](#troubleshooting)

---

## 📁 Project Structure

```
LeadFinder-Agent/
├── main.py                    # FastAPI backend entry point
├── requirements.txt           # Python dependencies
├── api/                       # API routes
├── lead_generation/           # Core business logic
├── config/                    # Configuration
├── vercel.json               # Vercel config (for serverless)
└── lead-generation-dashboard/ # React frontend
    ├── package.json
    ├── vite.config.js
    └── src/
```

---

## ✅ Prerequisites

Before deploying, ensure you have:

- [ ] **GitHub Account** - [Sign up here](https://github.com/signup)
- [ ] **Vercel Account** - [Sign up here](https://vercel.com/signup) (free tier available)
- [ ] **Railway Account** - [Sign up here](https://railway.app/) (free tier: $5/month credit)
- [ ] **API Keys**:
  - OpenAI API Key - [Get here](https://platform.openai.com/api-keys)
  - Firecrawl API Key - [Get here](https://firecrawl.dev/)

---

## 🔧 Step 1: Prepare Your Code

### 1.1 Create Backend Configuration Files

Create `vercel.json` in the root directory (for serverless deployment):

```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

### 1.2 Create `runtime.txt` for Python version:

```
python-3.11
```

### 1.3 Update Frontend API URL

Edit `lead-generation-dashboard/src/App.jsx`:

```javascript
// Replace localhost with environment variable
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Update axios calls to use API_URL
const response = await axios.post(`${API_URL}/generate-leads`, {
  query: searchQuery,
  num_links: numLinks,
});
```

### 1.4 Create Frontend Environment File

Create `lead-generation-dashboard/.env.example`:

```
VITE_API_URL=https://your-backend-url.railway.app
```

---

## 📤 Step 2: Push to GitHub

### 2.1 Initialize Git Repository

```bash
cd LeadFinder-Agent-main

# Initialize git if not already done
git init

# Create .gitignore
echo ".env
__pycache__/
*.pyc
node_modules/
.venv/
venv/
dist/
.vercel/
" > .gitignore
```

### 2.2 Commit Your Code

```bash
git add .
git commit -m "Initial commit: LeadFinder AI with multi-source search"
```

### 2.3 Create GitHub Repository

1. Go to [GitHub](https://github.com) → Click **"+"** → **"New repository"**
2. Name: `leadfinder-ai`
3. Set to **Public** or **Private**
4. Click **"Create repository"**

### 2.4 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/leadfinder-ai.git
git branch -M main
git push -u origin main
```

---

## 🚂 Step 3: Deploy Backend to Railway

Railway is recommended for Python FastAPI backends (free $5/month credit).

### 3.1 Sign Up & Connect GitHub

1. Go to [Railway.app](https://railway.app/)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your `leadfinder-ai` repository

### 3.2 Configure Railway Project

1. After importing, Railway will detect Python automatically
2. Click on your service → **"Settings"**
3. Set **Root Directory**: `/` (leave empty for root)
4. Set **Start Command**:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### 3.3 Add Environment Variables

Go to **"Variables"** tab and add:

| Variable            | Value                   |
| ------------------- | ----------------------- |
| `OPENAI_API_KEY`    | `sk-your-openai-key`    |
| `FIRECRAWL_API_KEY` | `fc-your-firecrawl-key` |
| `PORT`              | `8000`                  |

### 3.4 Deploy

1. Click **"Deploy"**
2. Wait for build to complete (2-5 minutes)
3. Copy your **Railway URL**: `https://leadfinder-ai-production.up.railway.app`

### 3.5 Test Backend

```bash
curl -X POST https://YOUR-RAILWAY-URL/generate-leads \
  -H "Content-Type: application/json" \
  -d '{"query": "AI startups", "num_links": 3}'
```

---

## ▲ Step 4: Deploy Frontend to Vercel

### 4.1 Sign Up & Connect GitHub

1. Go to [Vercel.com](https://vercel.com/)
2. Click **"Add New..."** → **"Project"**
3. Import your `leadfinder-ai` repository

### 4.2 Configure Vercel Project

Set these options:

| Setting              | Value                       |
| -------------------- | --------------------------- |
| **Framework Preset** | Vite                        |
| **Root Directory**   | `lead-generation-dashboard` |
| **Build Command**    | `npm run build`             |
| **Output Directory** | `dist`                      |

### 4.3 Add Environment Variables

Click **"Environment Variables"** and add:

| Variable       | Value                      |
| -------------- | -------------------------- |
| `VITE_API_URL` | `https://YOUR-RAILWAY-URL` |

### 4.4 Deploy

1. Click **"Deploy"**
2. Wait for build (1-2 minutes)
3. Your frontend URL: `https://leadfinder-ai.vercel.app`

---

## 🔗 Step 5: Connect Frontend to Backend

### 5.1 Update CORS in Backend

Edit `api/routes.py` to allow your Vercel domain:

```python
from fastapi.middleware.cors import CORSMiddleware

def create_app():
    app = FastAPI()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "https://leadfinder-ai.vercel.app",  # Your Vercel URL
            "https://*.vercel.app",  # All Vercel preview URLs
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ... rest of your routes
```

### 5.2 Redeploy Backend

Push the CORS update to GitHub:

```bash
git add .
git commit -m "Add CORS for Vercel frontend"
git push
```

Railway will automatically redeploy.

### 5.3 Test Full Application

1. Visit your Vercel URL: `https://leadfinder-ai.vercel.app`
2. Enter a search query
3. Verify leads are returned from the backend

---

## 🎨 Alternative: Deploy Backend to Render

If you prefer Render over Railway:

### Render Setup

1. Go to [Render.com](https://render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Configure:

| Setting            | Value                                          |
| ------------------ | ---------------------------------------------- |
| **Name**           | `leadfinder-api`                               |
| **Root Directory** | `/`                                            |
| **Runtime**        | Python 3                                       |
| **Build Command**  | `pip install -r requirements.txt`              |
| **Start Command**  | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

5. Add Environment Variables (same as Railway)
6. Click **"Create Web Service"**

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Module not found" errors on Railway/Render

Ensure all dependencies are in `requirements.txt`:

```
firecrawl-py
phidata
pydantic
openai
python-dotenv
fastapi
uvicorn
pydantic-settings
beautifulsoup4
```

#### 2. CORS errors in browser console

Add your Vercel domain to CORS `allow_origins` in `api/routes.py`

#### 3. Environment variables not working

- **Vercel**: Must prefix with `VITE_` for frontend
- **Railway/Render**: No prefix needed for backend

#### 4. Build fails on Vercel

Check that `lead-generation-dashboard` is set as **Root Directory**

#### 5. API returns 500 errors

Check Railway/Render logs for Python errors. Common issues:

- Missing API keys
- Incorrect import paths

### View Logs

- **Railway**: Click service → "Deployments" → "View Logs"
- **Render**: Dashboard → Service → "Logs"
- **Vercel**: Project → "Deployments" → Click deployment → "Functions" tab

---

## 📊 Cost Estimation

| Service       | Free Tier             | Paid              |
| ------------- | --------------------- | ----------------- |
| **Vercel**    | 100GB bandwidth/month | $20/month Pro     |
| **Railway**   | $5 free credit/month  | Pay as you go     |
| **Render**    | 750 hours/month       | $7/month starter  |
| **OpenAI**    | None                  | ~$0.002/1K tokens |
| **Firecrawl** | Limited               | $19/month starter |

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed to Railway/Render
- [ ] Backend environment variables configured
- [ ] Frontend deployed to Vercel
- [ ] Frontend `VITE_API_URL` configured
- [ ] CORS updated to allow Vercel domain
- [ ] Full application tested end-to-end

---

## 🎉 Success!

Your LeadFinder AI is now live at:

- **Frontend**: `https://leadfinder-ai.vercel.app`
- **Backend API**: `https://leadfinder-api.railway.app`

Share your deployment with others and start finding leads! 🚀

---

## 📞 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review Railway/Render/Vercel logs
3. Open an issue on GitHub

Happy deploying! 🎊
