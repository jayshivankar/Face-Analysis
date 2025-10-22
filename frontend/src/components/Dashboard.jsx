import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ImageUpload from './ImageUpload';
import WebcamCapture from './WebcamCapture';
import AnalysisResults from './AnalysisResults';
import { Camera, Upload } from 'lucide-react';
import { saveAnalysisReport } from '../lib/supabase';

export default function Dashboard() {
  const [activeMode, setActiveMode] = useState('upload');
  const [faceImage, setFaceImage] = useState(null);
  const [skinImage, setSkinImage] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!faceImage) {
      alert('Please upload or capture a face image first');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();

      const faceBlob = await fetch(faceImage).then(r => r.blob());
      formData.append('face_image', faceBlob, 'face.jpg');

      if (skinImage) {
        const skinBlob = await fetch(skinImage).then(r => r.blob());
        formData.append('skin_image', skinBlob, 'skin.jpg');
      }

      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setAnalysisResults(data);

      const saveResult = await saveAnalysisReport(data);
      if (saveResult.success) {
        console.log('Report saved successfully:', saveResult.data);
      } else {
        console.error('Failed to save report:', saveResult.error);
      }
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Failed to analyze image. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
      >
        <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">
          Capture or Upload Image
        </h2>

        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setActiveMode('upload')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
              activeMode === 'upload'
                ? 'bg-blue-600 text-white shadow-lg scale-105'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
          >
            <Upload className="w-5 h-5" />
            Upload Image
          </button>
          <button
            onClick={() => setActiveMode('webcam')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
              activeMode === 'webcam'
                ? 'bg-blue-600 text-white shadow-lg scale-105'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
          >
            <Camera className="w-5 h-5" />
            Use Webcam
          </button>
        </div>

        <AnimatePresence mode="wait">
          {activeMode === 'upload' ? (
            <motion.div
              key="upload"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
            >
              <ImageUpload
                faceImage={faceImage}
                setFaceImage={setFaceImage}
                skinImage={skinImage}
                setSkinImage={setSkinImage}
              />
            </motion.div>
          ) : (
            <motion.div
              key="webcam"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
            >
              <WebcamCapture
                faceImage={faceImage}
                setFaceImage={setFaceImage}
              />
            </motion.div>
          )}
        </AnimatePresence>

        <div className="mt-6">
          <button
            onClick={handleAnalyze}
            disabled={!faceImage || loading}
            className={`w-full py-4 px-6 rounded-lg font-semibold text-white text-lg transition-all ${
              !faceImage || loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 shadow-lg hover:shadow-xl transform hover:scale-105'
            }`}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Analyzing...
              </span>
            ) : (
              'Generate Health Report'
            )}
          </button>
        </div>
      </motion.div>

      {analysisResults && (
        <AnalysisResults results={analysisResults} faceImage={faceImage} />
      )}
    </div>
  );
}
