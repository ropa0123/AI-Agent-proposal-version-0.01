# Deploy to Railway - Step by Step Guide

## Prerequisites
✅ A GitHub account
✅ Git installed (we'll set this up)
✅ Your Gemini API key (already in .env file)

---

## Step 1: Install Git (if not installed)
Since git is not found on your system, download and install it:
1. Go to: https://git-scm.com/download/win
2. Download and run the installer
3. Use default settings during installation
4. Restart your terminal after installation

---

## Step 2: Initialize Git Repository
Open your terminal in the project folder and run:

```bash
cd "C:\Users\USER\Desktop\AI project\zim sec"
git init
git add .
git commit -m "Initial commit - ZIMSEC Assistant"
```

---

## Step 3: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `zimsec-assistant` (or any name you prefer)
3. Keep it **Private** (recommended for security)
4. **DO NOT** initialize with README, .gitignore, or license
5. Click "Create repository"

---

## Step 4: Push Code to GitHub
Copy the commands from GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/zimsec-assistant.git
git branch -M main
git push -u origin main
```

**Note:** You may need to authenticate with GitHub. Use a Personal Access Token:
- Go to: https://github.com/settings/tokens
- Generate new token (classic)
- Select `repo` scope
- Use the token as your password when pushing

---

## Step 5: Deploy on Railway

### 5.1 Create Railway Account
1. Go to https://railway.app
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### 5.2 Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `zimsec-assistant` repository
4. Railway will automatically detect it's a Python app

### 5.3 Add Environment Variables
1. Click on your deployed service
2. Go to "Variables" tab
3. Click "Add Variable" and add:
   ```
   GEMINI_API_KEY = AIzaSyA85osCjS4Tse_vyhA-Sur4CjvfIdQdHq4
   ```
4. Railway automatically provides `PORT` variable

### 5.4 Deploy!
- Railway will automatically build and deploy
- Wait 2-3 minutes for the first deployment
- You'll get a public URL like: `https://your-app.up.railway.app`

---

## Step 6: Access Your App
1. Click "Settings" tab in Railway
2. Scroll to "Networking"
3. Click "Generate Domain"
4. Your app will be live at the generated URL!

**Login with:**
- Username: `admin`
- Password: `zimsadmin`

---

## Important Security Notes

⚠️ **Before making your app public:**

1. **Change default credentials** in `Zimsec_agent_web.py`:
   ```python
   USERS = {
       "admin": "YOUR_STRONG_PASSWORD_HERE"
   }
   ```

2. **Consider removing your API key from .env** since it's in the file:
   - The .gitignore should prevent it from being committed
   - But verify with: `git status` (should NOT show .env)

3. **Keep your GitHub repo private** to protect your API key

---

## Troubleshooting

### Build Failed
- Check "Logs" tab in Railway
- Verify requirements.txt has all dependencies

### App Not Starting
- Check that PORT environment variable exists
- Look at deployment logs for errors

### Can't Push to GitHub
- Make sure git is installed: `git --version`
- Use Personal Access Token instead of password
- Check your internet connection

---

## Next Steps After Deployment

1. Test the live app thoroughly
2. Monitor usage in Railway dashboard
3. Set up custom domain (optional)
4. Configure production passwords
5. Monitor API usage on Google Cloud Console

---

## Railway Pricing
- **Free Tier**: $5 credit/month, $0.000463/GB-hour
- Typically enough for small apps with moderate traffic
- Upgrade if needed at https://railway.app/pricing

---

Need help? Check Railway docs: https://docs.railway.app
