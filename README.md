# Face Health Analyzer 2.0

A modern, full-stack web application that analyzes facial features to provide comprehensive health insights using AI and machine learning.

![Face Health Analyzer](https://img.shields.io/badge/Status-Production%20Ready-green)
![React](https://img.shields.io/badge/React-19.1-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal)
![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)

## Features

### Core Analysis Features
- **Age & Gender Detection** - Predicts age and gender from facial images
- **Fatigue Analysis** - Detects fatigue status from facial features
- **Emotion Recognition** - Identifies emotions (Happy, Sad, Neutral, Angry, Surprised)
- **Facial Symmetry Analysis** - Analyzes facial symmetry and detects potential conditions
- **Skin Disease Classification** - Identifies various skin conditions from close-up images

### New Features in 2.0
- **Face Health Index** - Comprehensive health score (0-100) with detailed component breakdown
- **Interactive Dashboard** - Modern, responsive UI with smooth animations
- **Real-time Webcam Capture** - Capture photos directly from your webcam
- **Drag & Drop Upload** - Easy image upload with preview
- **Dark/Light Theme** - Toggle between dark and light modes
- **PDF Report Generation** - Download detailed health reports as PDF
- **Report History** - Store and retrieve past analysis reports via Supabase
- **Personalized Recommendations** - AI-generated health recommendations based on analysis

## Tech Stack

### Frontend
- **React 19** with Vite for fast development
- **TailwindCSS** for modern, responsive styling
- **Framer Motion** for smooth animations
- **Recharts** for data visualization
- **Lucide React** for beautiful icons
- **react-webcam** for camera integration
- **jsPDF** for PDF generation

### Backend
- **FastAPI** for high-performance API
- **TensorFlow/Keras** for ML model inference
- **MediaPipe** for facial landmark detection
- **OpenCV** for image processing
- **Pydantic** for data validation

### Database & Storage
- **Supabase** for PostgreSQL database and real-time features
- Row Level Security (RLS) for data protection
- Automatic report storage and retrieval

## Architecture

```
face-health-analyzer/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── WebcamCapture.jsx
│   │   │   ├── AnalysisResults.jsx
│   │   │   ├── HealthIndexCard.jsx
│   │   │   └── ThemeToggle.jsx
│   │   ├── lib/             # Supabase client
│   │   ├── utils/           # Utility functions
│   │   └── App.jsx          # Main app component
│   ├── package.json
│   └── vite.config.js
│
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API application
│   ├── models/             # ML model loader
│   │   └── model_loader.py
│   ├── services/           # Business logic
│   │   ├── face_analysis.py
│   │   └── health_index.py
│   └── requirements.txt
│
├── saved_models/           # Pre-trained ML models
│   ├── age_model.keras
│   ├── gender_model.keras
│   ├── best_fatigue_model.keras
│   └── mobilenet_skin.keras
│
└── README.md
```

## Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- Supabase account (free tier works)

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the FastAPI server:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment variables:**
Create a `.env` file in the frontend directory:
```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_API_URL=http://localhost:8000
```

4. **Run the development server:**
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Supabase Setup

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. The database migration will run automatically when the frontend connects
4. Copy your project URL and anon key to the `.env` file

## Usage

### Analyzing a Face

1. **Choose Input Method:**
   - Click "Upload Image" to upload a photo from your device
   - Click "Use Webcam" to capture a live photo

2. **Upload Images:**
   - **Face Image (Required):** Upload or capture a clear frontal face image
   - **Skin Image (Optional):** Upload a close-up of skin for detailed analysis

3. **Generate Report:**
   - Click "Generate Health Report" button
   - Wait for AI analysis to complete
   - View detailed results with visualizations

4. **Download Report:**
   - Click "Download Report" to save as PDF
   - Reports are automatically saved to your history

### Understanding Results

#### Face Health Index
- **Score:** 0-100 overall health score
- **Rating:** Excellent (90+), Good (75-89), Fair (60-74), Poor (45-59), Needs Attention (<45)
- **Component Scores:** Individual scores for symmetry, fatigue, skin, and emotion

#### Analysis Components
- **Age & Gender:** Predicted age and gender with confidence scores
- **Fatigue Status:** Current fatigue level (Not Fatigued, Slightly Fatigued, Fatigued)
- **Emotion:** Detected emotion state
- **Facial Symmetry:** Asymmetry score and potential conditions
- **Skin Condition:** Detected skin conditions (if skin image provided)

## Model Details

### Supported Models

| Model | Purpose | Input Shape | Output |
|-------|---------|-------------|--------|
| Age Model | Age prediction | (224, 224, 3) | Integer age |
| Gender Model | Gender classification | (224, 224, 3) | Male/Female |
| Fatigue Model | Fatigue detection | (100, 100, 1) | Fatigued/Not Fatigued |
| Skin Model | Skin condition classification | (224, 224, 3) | 10 skin conditions |

### Skin Conditions Detected
1. Acne
2. Actinic Keratosis
3. Basal Cell Carcinoma
4. Dermatofibroma
5. Melanocytic Nevi
6. Melanoma
7. Seborrheic Keratoses
8. Squamous Cell Carcinoma
9. Vascular Lesion
10. Normal

## API Endpoints

### Health Check
```
GET /health
```
Returns API and model status

### Complete Analysis
```
POST /api/analyze
Content-Type: multipart/form-data

Parameters:
- face_image: File (required)
- skin_image: File (optional)
```

### Individual Analysis Endpoints
- `POST /api/analyze/age-gender` - Age and gender only
- `POST /api/analyze/fatigue` - Fatigue analysis only
- `POST /api/analyze/symmetry` - Symmetry analysis only
- `POST /api/analyze/skin` - Skin analysis only
- `POST /api/analyze/emotion` - Emotion detection only

## Deployment

### Frontend Deployment (Vercel/Netlify)

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Deploy the `dist` folder to your hosting platform

3. Configure environment variables in your hosting dashboard

### Backend Deployment (Railway/Render)

1. Create a new service
2. Connect your GitHub repository
3. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy

### Environment Variables for Production

Frontend:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_SUPABASE_ANON_KEY`
- `VITE_API_URL` (your backend URL)

Backend:
- `MODELS_PATH` (optional, defaults to ../saved_models)

## Security & Privacy

- All analysis is performed in real-time and not stored on servers (except in Supabase if enabled)
- Images are processed client-side before being sent to the API
- Supabase uses Row Level Security (RLS) for data protection
- No personal data is collected beyond analysis results
- All communications use HTTPS in production

## Disclaimer

**IMPORTANT:** This application provides health-related information for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

- Always seek the advice of qualified healthcare providers with questions about medical conditions
- Never disregard professional medical advice or delay seeking it because of something you have read or seen in this application
- If you think you may have a medical emergency, call your doctor or emergency services immediately

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- TensorFlow and Keras for ML framework
- MediaPipe for facial landmark detection
- FastAPI for the excellent web framework
- React team for the amazing UI library
- Supabase for the backend infrastructure

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review closed issues for solutions

---

**Built with by the Face Health Analyzer Team**

Made with React, FastAPI, TensorFlow, and Supabase
