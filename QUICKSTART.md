# Quick Start Guide

Get your Face Health Analyzer up and running in 5 minutes!

## Prerequisites

- Python 3.9+
- Node.js 18+
- Supabase account (free)

## Step 1: Clone and Setup

```bash
cd project
```

## Step 2: Backend Setup (Terminal 1)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend will start at `http://localhost:8000`

## Step 3: Frontend Setup (Terminal 2)

```bash
cd frontend
npm install
```

Create `.env` file:
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_SUPABASE_ANON_KEY=your_supabase_key
```

```bash
npm run dev
```

Frontend will start at `http://localhost:5173`

## Step 4: Use the App

1. Open `http://localhost:5173` in your browser
2. Click "Upload Image" or "Use Webcam"
3. Upload a face photo
4. Click "Generate Health Report"
5. View your comprehensive health analysis!

## Using the Startup Scripts

### Linux/Mac:
```bash
./start-backend.sh   # Terminal 1
./start-frontend.sh  # Terminal 2
```

### Windows:
```bash
cd backend && python main.py    # Terminal 1
cd frontend && npm run dev       # Terminal 2
```

## Features to Try

- Upload a face image and get instant analysis
- Capture a photo using your webcam
- Upload a skin close-up for detailed skin analysis
- Toggle between dark and light themes
- Download your report as PDF
- View your Face Health Index score

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.9+)
- Activate virtual environment first
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't build
- Check Node version: `node --version` (need 18+)
- Delete `node_modules` and run `npm install` again
- Make sure `.env` file exists with correct values

### Models not loading
- Check that `saved_models/` directory contains all 4 model files
- Models should be in `.keras` format
- Check backend logs for specific errors

### Supabase errors
- Verify your Supabase URL and anon key in `.env`
- Check that the database migration ran successfully
- Test connection at `http://localhost:8000/health`

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Deploy to production (Vercel + Railway)
3. Add authentication for multi-user support
4. Train custom models for better accuracy

## Support

- Check the [README.md](README.md) for full documentation
- Review backend logs at `http://localhost:8000/docs`
- Test API endpoints using FastAPI's built-in docs

---

**Ready to analyze some faces!**
