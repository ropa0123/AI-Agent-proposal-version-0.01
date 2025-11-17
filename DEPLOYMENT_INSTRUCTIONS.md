# Railway Deployment Instructions

## Prerequisites
- A Railway account (sign up at https://railway.app)
- Google API key for Gemini AI (get from https://makersuite.google.com/app/apikey)

## Step 1: Prepare Your Code
Your code is now ready for deployment with the following changes made:
- ✅ Server host changed from `127.0.0.1` to `0.0.0.0` (accepts external connections)
- ✅ Environment variables configured via `.env` file
- ✅ Sensitive data excluded from git via `.gitignore`
- ✅ Procfile configured for Railway
- ✅ Python runtime specified in `runtime.txt`

## Step 2: Deploy to Railway

### Option A: Deploy from GitHub (Recommended)
1. Push your code to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Railway ready"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. Go to https://railway.app and click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect Python and deploy

### Option B: Deploy from CLI
1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login and deploy:
   ```bash
   railway login
   railway init
   railway up
   ```

## Step 3: Configure Environment Variables
After deployment, you MUST set environment variables in Railway:

1. Go to your project in Railway dashboard
2. Click on your service
3. Go to "Variables" tab
4. Add the following variable:
   - **Key**: `GOOGLE_API_KEY`
   - **Value**: Your actual Google API key (from https://makersuite.google.com/app/apikey)

5. Click "Deploy" to restart with new environment variables

## Step 4: Access Your App
1. Railway will provide a public URL (e.g., `https://your-app.railway.app`)
2. Click on the URL or find it in the "Settings" tab
3. Your app should now be live!

## Default Credentials
- **Admin**: username: `admin`, password: `admin123`
- **User**: username: `zimsec`, password: `admin123`

⚠️ **IMPORTANT**: Change these default passwords immediately in production!

## Troubleshooting

### App won't start
- Check logs in Railway dashboard
- Verify `GOOGLE_API_KEY` is set correctly
- Ensure Python version matches `runtime.txt`

### Can't access the app
- Check if Railway assigned a public domain
- Verify server is listening on `0.0.0.0` not `127.0.0.1`
- Check Railway logs for errors

### Database files reset
- JSON files (users.json, history.json, etc.) are ephemeral on Railway
- Consider using Railway's PostgreSQL or MongoDB plugins for persistent storage
- Or use a cloud storage service (AWS S3, Google Cloud Storage, etc.)

## Important Security Notes

1. **Change default passwords** in production
2. **Never commit** `.env` file with real API keys
3. **Enable HTTPS** (Railway provides this automatically)
4. **Hash passwords** instead of storing plain text (current implementation uses plain text)
5. **Use a proper database** for production (PostgreSQL, MongoDB, etc.)

## Persistent Storage Upgrade (Optional)

To make data persist across deployments:

1. Add Railway PostgreSQL plugin:
   - Go to your project → "New" → "Database" → "Add PostgreSQL"
   - Update code to use PostgreSQL instead of JSON files

2. Or use Railway Volumes (for file persistence):
   - Go to Settings → Add Volume
   - Mount to `/app/data`
   - Update code to write JSON files to `/app/data/`

## Support
- Railway docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
