from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class HealthIndexCalculator:
    def __init__(self):
        self.weights = {
            'symmetry': 0.25,
            'fatigue': 0.25,
            'skin': 0.30,
            'emotion': 0.20
        }

    def calculate_health_index(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        scores = {}

        symmetry_score = self._calculate_symmetry_score(analysis_result.get('symmetry', {}))
        scores['symmetry'] = symmetry_score

        fatigue_score = self._calculate_fatigue_score(analysis_result.get('fatigue', 'Unknown'))
        scores['fatigue'] = fatigue_score

        skin_score = self._calculate_skin_score(
            analysis_result.get('skin_condition'),
            analysis_result.get('confidence_scores', {}).get('skin', 0)
        )
        scores['skin'] = skin_score

        emotion_score = self._calculate_emotion_score(analysis_result.get('emotion', 'Neutral'))
        scores['emotion'] = emotion_score

        overall_score = (
            scores['symmetry'] * self.weights['symmetry'] +
            scores['fatigue'] * self.weights['fatigue'] +
            scores['skin'] * self.weights['skin'] +
            scores['emotion'] * self.weights['emotion']
        )

        overall_score = round(overall_score, 2)

        rating = self._get_rating(overall_score)

        return {
            'overall_score': overall_score,
            'rating': rating,
            'component_scores': scores,
            'max_score': 100
        }

    def _calculate_symmetry_score(self, symmetry_data: Dict[str, Any]) -> float:
        if 'error' in symmetry_data or not symmetry_data:
            return 50.0

        asymmetry_score = symmetry_data.get('asymmetry_score', 0.04)
        condition = symmetry_data.get('predicted_condition', '')

        if 'Very Symmetrical' in condition:
            return 100.0
        elif 'Slight Asymmetry' in condition or 'normal' in condition.lower():
            return 85.0
        elif 'Bell\'s Palsy' in condition or 'Stroke' in condition:
            return 40.0
        elif 'Asymmetry Detected' in condition:
            return 60.0
        else:
            score = max(0, 100 - (asymmetry_score * 1000))
            return min(100, max(0, score))

    def _calculate_fatigue_score(self, fatigue_status: str) -> float:
        if 'Not Fatigued' in fatigue_status:
            return 100.0
        elif 'Slightly Fatigued' in fatigue_status:
            return 70.0
        elif 'Fatigued' in fatigue_status:
            return 40.0
        else:
            return 60.0

    def _calculate_skin_score(self, condition: str, confidence: float) -> float:
        if not condition:
            return 70.0

        dangerous_conditions = ['Melanoma', 'Basal Cell Carcinoma', 'Squamous Cell Carcinoma']
        moderate_conditions = ['Actinic Keratosis', 'Acne', 'Seborrheic Keratoses']
        mild_conditions = ['Melanocytic Nevi', 'Dermatofibroma', 'Vascular Lesion']

        if condition == 'Normal':
            return 100.0
        elif any(dc in condition for dc in dangerous_conditions):
            return max(30.0, 50.0 - (confidence * 20))
        elif any(mc in condition for mc in moderate_conditions):
            return max(50.0, 70.0 - (confidence * 10))
        elif any(mc in condition for mc in mild_conditions):
            return max(70.0, 85.0 - (confidence * 5))
        else:
            return 70.0

    def _calculate_emotion_score(self, emotion: str) -> float:
        emotion_scores = {
            'Happy': 100.0,
            'Neutral': 75.0,
            'Surprised': 80.0,
            'Sad': 50.0,
            'Angry': 45.0
        }
        return emotion_scores.get(emotion, 70.0)

    def _get_rating(self, score: float) -> str:
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 45:
            return "Poor"
        else:
            return "Needs Attention"

    def generate_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        recommendations = []

        fatigue = analysis_result.get('fatigue', '')
        if 'Fatigued' in fatigue and 'Not' not in fatigue:
            recommendations.append("Consider getting more rest and improving sleep quality")
            recommendations.append("Stay hydrated throughout the day")

        symmetry = analysis_result.get('symmetry', {})
        condition = symmetry.get('predicted_condition', '')
        if 'Palsy' in condition or 'Stroke' in condition:
            recommendations.append("Consult a healthcare professional immediately for facial asymmetry evaluation")
        elif 'Asymmetry Detected' in condition:
            recommendations.append("Monitor facial symmetry changes and consult a doctor if symptoms persist")

        skin_condition = analysis_result.get('skin_condition', '')
        dangerous_conditions = ['Melanoma', 'Basal Cell Carcinoma', 'Squamous Cell Carcinoma']
        if any(dc in skin_condition for dc in dangerous_conditions):
            recommendations.append("Seek immediate dermatological consultation for skin examination")
            recommendations.append("Avoid excessive sun exposure and use sunscreen daily")
        elif skin_condition == 'Acne':
            recommendations.append("Maintain a consistent skincare routine and consider consulting a dermatologist")
        elif skin_condition and skin_condition != 'Normal':
            recommendations.append("Consider scheduling a dermatology checkup for skin evaluation")

        emotion = analysis_result.get('emotion', '')
        if emotion in ['Sad', 'Angry']:
            recommendations.append("Consider stress management techniques or speaking with a mental health professional")

        age = analysis_result.get('age', 0)
        if age > 40:
            recommendations.append("Regular health checkups are recommended for your age group")

        if not recommendations:
            recommendations.append("Maintain a healthy lifestyle with proper sleep, nutrition, and exercise")
            recommendations.append("Stay hydrated and protect your skin from sun damage")

        return recommendations
