import { motion } from 'framer-motion';
import {
  User,
  Activity,
  Smile,
  Scan,
  Droplet,
  TrendingUp,
  Download,
  AlertCircle,
  CheckCircle
} from 'lucide-react';
import HealthIndexCard from './HealthIndexCard';
import { generatePDF } from '../utils/pdfGenerator';

export default function AnalysisResults({ results, faceImage }) {
  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: (i) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * 0.1,
        duration: 0.5,
      },
    }),
  };

  const getEmotionColor = (emotion) => {
    const colors = {
      Happy: 'text-green-600 dark:text-green-400',
      Neutral: 'text-blue-600 dark:text-blue-400',
      Sad: 'text-gray-600 dark:text-gray-400',
      Angry: 'text-red-600 dark:text-red-400',
      Surprised: 'text-yellow-600 dark:text-yellow-400',
    };
    return colors[emotion] || 'text-gray-600 dark:text-gray-400';
  };

  const getSkinConditionColor = (condition) => {
    if (!condition) return 'text-gray-600 dark:text-gray-400';
    if (condition === 'Normal') return 'text-green-600 dark:text-green-400';
    if (['Melanoma', 'Basal Cell Carcinoma', 'Squamous Cell Carcinoma'].some(c => condition.includes(c))) {
      return 'text-red-600 dark:text-red-400';
    }
    return 'text-yellow-600 dark:text-yellow-400';
  };

  const handleDownloadPDF = () => {
    generatePDF(results, faceImage);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-gray-800 dark:text-gray-100">
          Analysis Results
        </h2>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleDownloadPDF}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white rounded-lg font-medium shadow-lg transition-all"
        >
          <Download className="w-5 h-5" />
          Download Report
        </motion.button>
      </div>

      <HealthIndexCard healthIndex={results.health_index} />

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <motion.div
          custom={0}
          variants={cardVariants}
          initial="hidden"
          animate="visible"
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-blue-100 dark:bg-blue-900 p-3 rounded-lg">
              <User className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
              Age & Gender
            </h3>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400">Age:</span>
              <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {results.age} years
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400">Gender:</span>
              <span className="text-xl font-semibold text-gray-800 dark:text-gray-200">
                {results.gender}
              </span>
            </div>
            <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Confidence: {(results.confidence_scores?.age * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          custom={1}
          variants={cardVariants}
          initial="hidden"
          animate="visible"
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-purple-100 dark:bg-purple-900 p-3 rounded-lg">
              <Activity className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
              Fatigue Status
            </h3>
          </div>
          <div className="space-y-3">
            <div className={`text-2xl font-bold ${
              results.fatigue.includes('Not')
                ? 'text-green-600 dark:text-green-400'
                : 'text-red-600 dark:text-red-400'
            }`}>
              {results.fatigue}
            </div>
            <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Confidence: {(results.confidence_scores?.fatigue * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          custom={2}
          variants={cardVariants}
          initial="hidden"
          animate="visible"
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-yellow-100 dark:bg-yellow-900 p-3 rounded-lg">
              <Smile className={`w-6 h-6 ${getEmotionColor(results.emotion)}`} />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
              Emotion
            </h3>
          </div>
          <div className="space-y-3">
            <div className={`text-2xl font-bold ${getEmotionColor(results.emotion)}`}>
              {results.emotion}
            </div>
            <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Confidence: {(results.confidence_scores?.emotion * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          custom={3}
          variants={cardVariants}
          initial="hidden"
          animate="visible"
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow md:col-span-2"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-teal-100 dark:bg-teal-900 p-3 rounded-lg">
              <Scan className="w-6 h-6 text-teal-600 dark:text-teal-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
              Facial Symmetry
            </h3>
          </div>
          <div className="space-y-3">
            {results.symmetry.error ? (
              <div className="text-red-600 dark:text-red-400">{results.symmetry.error}</div>
            ) : (
              <>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Asymmetry Score:</span>
                  <span className="text-xl font-bold text-teal-600 dark:text-teal-400">
                    {results.symmetry.asymmetry_score}
                  </span>
                </div>
                <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-3">
                  <p className="text-sm font-medium text-gray-800 dark:text-gray-200">
                    {results.symmetry.predicted_condition}
                  </p>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    Confidence: {(results.symmetry.confidence * 100).toFixed(0)}%
                  </div>
                </div>
              </>
            )}
          </div>
        </motion.div>

        {results.skin_condition && (
          <motion.div
            custom={4}
            variants={cardVariants}
            initial="hidden"
            animate="visible"
            className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="bg-pink-100 dark:bg-pink-900 p-3 rounded-lg">
                <Droplet className="w-6 h-6 text-pink-600 dark:text-pink-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
                Skin Condition
              </h3>
            </div>
            <div className="space-y-3">
              <div className={`text-xl font-bold ${getSkinConditionColor(results.skin_condition)}`}>
                {results.skin_condition}
              </div>
              <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  Confidence: {(results.confidence_scores?.skin * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {results.recommendations && results.recommendations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-orange-100 dark:bg-orange-900 p-3 rounded-lg">
              <TrendingUp className="w-6 h-6 text-orange-600 dark:text-orange-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-100">
              Recommendations
            </h3>
          </div>
          <ul className="space-y-3">
            {results.recommendations.map((rec, idx) => (
              <motion.li
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 + idx * 0.1 }}
                className="flex items-start gap-3 text-gray-700 dark:text-gray-300"
              >
                <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                <span>{rec}</span>
              </motion.li>
            ))}
          </ul>
        </motion.div>
      )}
    </motion.div>
  );
}
