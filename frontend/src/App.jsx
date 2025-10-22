import { useState } from 'react';
import { motion } from 'framer-motion';
import Dashboard from './components/Dashboard';
import ThemeToggle from './components/ThemeToggle';
import { Brain } from 'lucide-react';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
      <div className="bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100 dark:from-gray-900 dark:via-blue-950 dark:to-gray-900 min-h-screen">
        <header className="border-b border-gray-200 dark:border-gray-800 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-3"
              >
                <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-2 rounded-lg shadow-lg">
                  <Brain className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 dark:from-blue-400 dark:to-blue-600 bg-clip-text text-transparent">
                    Face Health Analyzer
                  </h1>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    AI-Powered Health Insights
                  </p>
                </div>
              </motion.div>

              <ThemeToggle darkMode={darkMode} toggleTheme={toggleTheme} />
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-8">
          <Dashboard />
        </main>

        <footer className="border-t border-gray-200 dark:border-gray-800 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm mt-16">
          <div className="container mx-auto px-4 py-6">
            <div className="text-center text-sm text-gray-600 dark:text-gray-400">
              <p className="font-medium mb-2">Disclaimer</p>
              <p>
                This application provides health-related information for educational purposes only.
                It is not a substitute for professional medical advice, diagnosis, or treatment.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
