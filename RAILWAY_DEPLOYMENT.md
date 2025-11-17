# Railway Deployment Guide

## Prerequisites
- Railway account (sign up at https://railway.app)
- Git installed and repository initialized

## Step 1: Initialize Git Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit"
```

## Step 2: Deploy to Railway

### Option A: Deploy via Railway CLI
1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize and deploy:
   ```bash
   railway init
   railway up
   ```

### Option B: Deploy via GitHub
1. Push your code to GitHub:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo.git
   git branch -M main
   git push -u origin main
   ```

2. Go to https://railway.app/new
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect the configuration

### Option C: Deploy via Railway Dashboard
1. Go to https://railway.app/new
2. Select "Deploy from GitHub repo" or "Empty Project"
3. Connect your repository or upload files

## Step 3: Configure Environment Variables

In Railway Dashboard:
1. Go to your project
2. Click on "Variables" tab
3. Add the following variable:
   - `GOOGLE_API_KEY`: Your Google Generative AI API key

**IMPORTANT**: Never commit your `.env` file to git. The `.gitignore` file already excludes it.

## Step 4: Verify Deployment

1. Railway will automatically build and deploy your app
2. Once deployed, Railway will provide a public URL
3. Access your app at: `https://your-app-name.railway.app`

## Default Credentials

- Username: `zimsec`
- Password: `admin123`

**Security Note**: Change these credentials in production by modifying the `USERS` dictionary in `Zim_sec_GUI.PY`.

## Files Created for Railway

- **Procfile**: Defines how Railway should start your app
- **railway.json**: Railway-specific configuration
- **runtime.txt**: Specifies Python version
- **.gitignore**: Updated to exclude sensitive files and history

## Troubleshooting

### App not starting?
- Check Railway logs in the dashboard
- Verify all environment variables are set
- Ensure `GOOGLE_API_KEY` is valid

### Port binding issues?
The app now automatically uses Railway's `PORT` environment variable (defaults to 8080 locally).

### Session issues?
CherryPy sessions are file-based. For production, consider using a database-backed session store.

## Local Testing

Test the deployment configuration locally:
```bash
PORT=8080 python "Zim_sec_GUI.PY"
```

Then visit: http://localhost:8080

## Next Steps

1. Set up a custom domain in Railway (optional)
2. Configure database for persistent storage (optional)
3. Set up monitoring and alerts
4. Review and update security credentials
