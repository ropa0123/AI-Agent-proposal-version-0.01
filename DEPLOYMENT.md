# ZIMSEC Assistant - Deployment Guide

## Prerequisites
- Google Gemini API Key
- Python 3.11+ or Docker installed

## Setup Instructions

### 1. Environment Variables
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
HOST=0.0.0.0
PORT=8080
```

### 2. Local Deployment

#### Option A: Direct Python
```bash
pip install -r requirements.txt
python Zimsec_agent_web.py
```

#### Option B: Docker
```bash
docker build -t zimsec-assistant .
docker run -p 8080:8080 --env-file .env zimsec-assistant
```

Access the app at: `http://localhost:8080`

---

## Cloud Deployment Options

### Railway (Recommended - Easy)
1. Push code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Add environment variables in Railway dashboard:
   - `GEMINI_API_KEY`
   - `PORT` (Railway provides this automatically)
5. Deploy!

### Render
1. Push code to GitHub
2. Go to [Render.com](https://render.com)
3. New → Web Service
4. Connect your repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python Zimsec_agent_web.py`
6. Add environment variable `GEMINI_API_KEY`
7. Deploy!

### Google Cloud Run
```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT/zimsec-assistant

# Deploy
gcloud run deploy zimsec-assistant \
  --image gcr.io/YOUR_PROJECT/zimsec-assistant \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key_here
```

### Heroku
```bash
# Login and create app
heroku login
heroku create your-app-name

# Set environment variable
heroku config:set GEMINI_API_KEY=your_key_here

# Deploy
git push heroku main
```

### AWS Elastic Beanstalk
1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init -p python-3.11 zimsec-assistant`
3. Create environment: `eb create zimsec-env`
4. Set env vars: `eb setenv GEMINI_API_KEY=your_key_here`
5. Deploy: `eb deploy`

---

## Default Credentials
**Username**: `admin`  
**Password**: `zimsadmin`

⚠️ **Important**: Change these credentials in `Zimsec_agent_web.py` before production deployment!

## Security Notes
- Never commit `.env` or `creds.py` to version control
- Use strong passwords in production
- Consider implementing proper authentication (OAuth, JWT)
- Enable HTTPS in production
- Rotate API keys regularly

## Troubleshooting
- **Port already in use**: Change `PORT` in `.env`
- **API key error**: Verify `GEMINI_API_KEY` is set correctly
- **Module not found**: Run `pip install -r requirements.txt`
