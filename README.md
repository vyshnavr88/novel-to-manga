# novel-to-manga
# Novel to Manga Converter - FREE Edition

Transform light novels into manga using 100% free AI services!

## 🚀 Quick Deploy (5 Minutes)

### Step 1: Get Free API Keys (2 minutes)

1. **Groq** (Free LLM - Super Fast!)
   - Go to: https://console.groq.com
   - Sign up (Google/GitHub)
   - Create API key
   - Copy it

2. **FAL.ai** (Free Image Generation)
   - Go to: https://fal.ai/dashboard
   - Sign up
   - Go to Keys section
   - Create key
   - Copy it

### Step 2: Deploy Backend (2 minutes)

**Option A: Render.com (Recommended - Easiest)**

1. Go to: https://render.com
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Render auto-detects Python
6. Add environment variables:
   - `GROQ_API_KEY`: your_groq_key
   - `FAL_API_KEY`: your_fal_key
7. Click "Create Web Service"
8. Wait 3-5 minutes for deployment
9. Copy your service URL (e.g., https://your-app.onrender.com)

**Option B: Railway.app (Alternative)**

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Add environment variables in Settings
6. Deploy!

**Option C: Fly.io (Alternative)**

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly launch
fly secrets set GROQ_API_KEY=your_key
fly secrets set FAL_API_KEY=your_key
fly deploy
```

### Step 3: Deploy Frontend (1 minute)

**Vercel (Easiest)**

1. Go to: https://vercel.com
2. Sign up with GitHub
3. Click "Import Project"
4. Select your GitHub repo
5. Vercel auto-detects React
6. Add environment variable:
   - `VITE_API_URL`: https://your-backend-url.onrender.com
7. Click "Deploy"
8. Done! Get your URL (e.g., https://your-app.vercel.app)

**Netlify (Alternative)**

1. Go to: https://netlify.com
2. Sign up with GitHub
3. Click "Add new site" → "Import from Git"
4. Select repo
5. Build command: `npm run build`
6. Publish directory: `dist`
7. Deploy!

## 💻 Local Development

### Backend

```bash
# Clone repo
git clone your-repo-url
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Run server
python main.py
# Server runs at: http://localhost:8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Run dev server
npm run dev
# App runs at: http://localhost:5173
```

## 📊 Usage Limits (Free Tier)

| Service | Free Limit | Notes |
|---------|------------|-------|
| Groq | Generous rate limit | Enough for testing |
| FAL.ai | 100 requests/day | Create multiple accounts if needed |
| Render | 750 hours/month | Always-on for free |
| Vercel | Unlimited | Perfect for frontend |

## 🎯 Test It!

1. Open your deployed frontend URL
2. Click "Load Re:Zero Sample"
3. Click "Analyze Novel with AI"
4. Wait 5-10 seconds
5. Review AI-detected scenes
6. Click "Generate Manga Panels"
7. See your manga prompts!

## 🔥 Next Steps

1. Add your FAL.ai key to generate actual images
2. Process your own novel chapters
3. Customize the manga style
4. Share with friends!

## 💡 Tips

- **No API keys?** The demo mode still works for scene analysis
- **Want more images?** Create 2-3 FAL.ai accounts
- **Slow generation?** Free tier has rate limits, be patient
- **Errors?** Check your API keys are correct

## 🆘 Troubleshooting

**Backend won't start:**
- Check your API keys in Render dashboard
- View logs in Render console
- Verify requirements.txt is correct

**Frontend can't connect:**
- Update VITE_API_URL to your backend URL
- Check CORS is enabled in backend
- Verify backend is running (visit /health endpoint)

**Image generation fails:**
- Verify FAL.ai key is correct
- Check you haven't exceeded free tier
- Try again after 1 minute

## 🎉 You're Done!

You now have a fully functional Novel-to-Manga converter running 100% free!

Share your creations and let me know how it goes!

---

Built with ❤️ using:
- FastAPI + Groq + FAL.ai
- React + Tailwind CSS
- Deployed on Render + Vercel (Free!)

## 📧 Support

Having issues? Create an issue on GitHub or check the logs in your deployment dashboard.

Happy manga creating! 🎨📚