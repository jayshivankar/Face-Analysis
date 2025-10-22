import { motion } from 'framer-motion';
import { TrendingUp, Award } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

export default function HealthIndexCard({ healthIndex }) {
  const { overall_score, rating, component_scores } = healthIndex;

  const getRatingColor = (rating) => {
    const colors = {
      Excellent: 'text-green-600 dark:text-green-400',
      Good: 'text-blue-600 dark:text-blue-400',
      Fair: 'text-yellow-600 dark:text-yellow-400',
      Poor: 'text-orange-600 dark:text-orange-400',
      'Needs Attention': 'text-red-600 dark:text-red-400',
    };
    return colors[rating] || 'text-gray-600';
  };

  const getRatingBgColor = (rating) => {
    const colors = {
      Excellent: 'from-green-500 to-green-600',
      Good: 'from-blue-500 to-blue-600',
      Fair: 'from-yellow-500 to-yellow-600',
      Poor: 'from-orange-500 to-orange-600',
      'Needs Attention': 'from-red-500 to-red-600',
    };
    return colors[rating] || 'from-gray-500 to-gray-600';
  };

  const chartData = [
    { name: 'Symmetry', value: component_scores.symmetry, color: '#0ea5e9' },
    { name: 'Fatigue', value: component_scores.fatigue, color: '#8b5cf6' },
    { name: 'Skin', value: component_scores.skin, color: '#ec4899' },
    { name: 'Emotion', value: component_scores.emotion, color: '#f59e0b' },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 rounded-2xl shadow-2xl p-8 border border-gray-200 dark:border-gray-700"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className={`bg-gradient-to-br ${getRatingBgColor(rating)} p-3 rounded-xl shadow-lg`}>
          <Award className="w-8 h-8 text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">
            Face Health Index
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Comprehensive health assessment
          </p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="flex flex-col justify-center">
          <div className="mb-6">
            <div className="flex items-baseline gap-2 mb-2">
              <motion.span
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.3, type: 'spring', stiffness: 200 }}
                className="text-6xl font-bold text-gray-800 dark:text-gray-100"
              >
                {overall_score}
              </motion.span>
              <span className="text-2xl text-gray-500 dark:text-gray-400">/100</span>
            </div>
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className={`inline-block px-4 py-2 rounded-full bg-gradient-to-r ${getRatingBgColor(
                rating
              )} text-white font-semibold text-lg shadow-lg`}
            >
              {rating}
            </motion.div>
          </div>

          <div className="space-y-3">
            {chartData.map((item, idx) => (
              <motion.div
                key={item.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + idx * 0.1 }}
                className="space-y-1"
              >
                <div className="flex justify-between text-sm">
                  <span className="font-medium text-gray-700 dark:text-gray-300">
                    {item.name}
                  </span>
                  <span className="text-gray-600 dark:text-gray-400">
                    {item.value.toFixed(0)}/100
                  </span>
                </div>
                <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${item.value}%` }}
                    transition={{ delay: 0.6 + idx * 0.1, duration: 0.8 }}
                    className="h-full rounded-full"
                    style={{ backgroundColor: item.color }}
                  />
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="flex items-center justify-center">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
                animationBegin={600}
                animationDuration={1000}
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(0, 0, 0, 0.8)',
                  border: 'none',
                  borderRadius: '8px',
                  color: 'white',
                }}
              />
              <Legend
                verticalAlign="bottom"
                height={36}
                iconType="circle"
                formatter={(value) => (
                  <span className="text-sm text-gray-700 dark:text-gray-300">{value}</span>
                )}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </motion.div>
  );
}
