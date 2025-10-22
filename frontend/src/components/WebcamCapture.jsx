import { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { motion } from 'framer-motion';
import { Camera, RotateCcw } from 'lucide-react';

export default function WebcamCapture({ faceImage, setFaceImage }) {
  const webcamRef = useRef(null);
  const [hasPermission, setHasPermission] = useState(false);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      setFaceImage(imageSrc);
    }
  }, [webcamRef, setFaceImage]);

  const retake = () => {
    setFaceImage(null);
  };

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: 'user',
  };

  return (
    <div className="space-y-4">
      {faceImage ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative"
        >
          <img
            src={faceImage}
            alt="Captured"
            className="w-full rounded-xl shadow-lg"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={retake}
            className="mt-4 w-full flex items-center justify-center gap-2 px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors"
          >
            <RotateCcw className="w-5 h-5" />
            Retake Photo
          </motion.button>
        </motion.div>
      ) : (
        <div className="space-y-4">
          <div className="rounded-xl overflow-hidden shadow-lg bg-gray-900">
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              onUserMedia={() => setHasPermission(true)}
              className="w-full"
            />
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={capture}
            disabled={!hasPermission}
            className={`w-full flex items-center justify-center gap-2 px-6 py-4 rounded-lg font-medium transition-all ${
              hasPermission
                ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg'
                : 'bg-gray-400 text-gray-200 cursor-not-allowed'
            }`}
          >
            <Camera className="w-5 h-5" />
            Capture Photo
          </motion.button>
        </div>
      )}
    </div>
  );
}
