# Vercel Deployment Guide

## What Gets Deployed

**Vercel will deploy:** Only the React frontend (UI showcase)
**Not deployed:** Flask backend (stays local)

## Deployment Steps

### 1. Install Vercel CLI (Optional)
```bash
npm install -g vercel
```

### 2. Deploy via Vercel Dashboard (Recommended)

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New Project"
4. Import: `ramandeep-singh77/Voxora.ai`
5. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** Leave as `.` (root)
   - **Build Command:** `cd ASL-Hand-sign-language-translator--main && npm install && npm run build`
   - **Output Directory:** `ASL-Hand-sign-language-translator--main/dist`
   - **Install Command:** `echo 'Skip'`
6. Click "Deploy"

### 3. What Will Work on Vercel

✅ Beautiful React UI
✅ All buttons and controls
✅ Text display interface
❌ Camera feed (requires backend)
❌ Sign recognition (requires backend)

## Local Development (Full Functionality)

To run with full camera functionality:

```bash
# Terminal 1: Start Flask backend
python web_app.py

# Terminal 2: Start React frontend
cd ASL-Hand-sign-language-translator--main
npm run dev
```

Open: http://localhost:3000

## For Hackathon Demo

**Best Approach:**
1. **Show Vercel deployment** - Professional UI showcase
2. **Demo locally** - Full camera functionality
3. **Explain:** "Frontend deployed on Vercel, backend runs locally for camera access"

This shows you understand:
- Frontend/Backend separation
- Deployment strategies
- Hardware limitations in cloud environments

## URLs

- **Local (Full):** http://localhost:3000
- **Vercel (UI Only):** https://voxora-ai.vercel.app (after deployment)
- **GitHub:** https://github.com/ramandeep-singh77/Voxora.ai
