"""
Emotion Detection Module
Uses OpenCV for facial detection and emotion analysis
"""

import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

class EmotionDetector:
    """Detect emotions from facial images"""
    
    def __init__(self):
        """Initialize emotion detector with Haar Cascade"""
        # Load Haar Cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.face_alt_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        )
        self.profile_face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_profileface.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        self.smile_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_smile.xml'
        )

        if (
            self.face_cascade.empty()
            or self.face_alt_cascade.empty()
            or self.profile_face_cascade.empty()
            or self.eye_cascade.empty()
            or self.smile_cascade.empty()
        ):
            print("Warning: One or more Haar cascades failed to load")
    
    def decode_base64_image(self, base64_string):
        """Decode base64 image to OpenCV format"""
        try:
            # Remove header if present
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64
            img_data = base64.b64decode(base64_string)
            img = Image.open(BytesIO(img_data))
            
            # Ensure consistent color mode
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')

            # Convert to OpenCV format
            img_array = np.array(img)
            
            # Convert to BGR for OpenCV
            if len(img_array.shape) == 3 and img_array.shape[2] == 4:
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
            elif len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            elif len(img_array.shape) == 2:
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
            else:
                img_bgr = img_array
            
            return img_bgr
        except Exception as e:
            print(f"Error decoding image: {e}")
            return None
    
    def detect_face(self, image):
        """Detect face in image"""
        if image is None:
            return None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        h, w = gray.shape[:2]
        min_dynamic = max(24, int(min(h, w) * 0.08))

        detector_runs = [
            (self.face_cascade, gray, 1.1, 5, (min_dynamic, min_dynamic)),
            (self.face_alt_cascade, gray, 1.08, 4, (min_dynamic, min_dynamic)),
            (self.profile_face_cascade, gray, 1.1, 4, (min_dynamic, min_dynamic)),
            (self.profile_face_cascade, cv2.flip(gray, 1), 1.1, 4, (min_dynamic, min_dynamic)),
        ]

        candidates = []
        for cascade, frame_gray, scale, neighbors, min_size in detector_runs:
            faces = cascade.detectMultiScale(
                frame_gray,
                scaleFactor=scale,
                minNeighbors=neighbors,
                minSize=min_size
            )

            if len(faces) == 0:
                continue

            # If detected on flipped image, unflip x coordinate
            if frame_gray is not gray:
                for fx, fy, fw, fh in faces:
                    unflipped_x = w - (fx + fw)
                    candidates.append((int(unflipped_x), int(fy), int(fw), int(fh)))
            else:
                candidates.extend([tuple(map(int, face)) for face in faces])

        if not candidates:
            upscale_factor = 1.6
            enlarged = cv2.resize(
                gray,
                None,
                fx=upscale_factor,
                fy=upscale_factor,
                interpolation=cv2.INTER_CUBIC
            )
            up_min = max(30, int(min(enlarged.shape[0], enlarged.shape[1]) * 0.08))

            up_faces = self.face_cascade.detectMultiScale(
                enlarged,
                scaleFactor=1.08,
                minNeighbors=4,
                minSize=(up_min, up_min)
            )

            if len(up_faces) > 0:
                for ux, uy, uw, uh in up_faces:
                    candidates.append((
                        int(ux / upscale_factor),
                        int(uy / upscale_factor),
                        int(uw / upscale_factor),
                        int(uh / upscale_factor)
                    ))

        if not candidates:
            return None

        return max(candidates, key=lambda rect: rect[2] * rect[3])
    
    def analyze_facial_features(self, image, face_rect):
        """Analyze facial features for emotion detection"""
        x, y, w, h = face_rect

        if w <= 0 or h <= 0:
            return {
                'face_area': 0,
                'face_ratio': 1,
                'eyes_detected': 0,
                'eye_positions': [],
                'smiles_detected': 0,
                'smile_area_ratio': 0.0
            }
        
        # Extract face ROI
        face_roi = image[y:y+h, x:x+w]
        if face_roi is None or face_roi.size == 0:
            return {
                'face_area': w * h,
                'face_ratio': w / h if h > 0 else 1,
                'eyes_detected': 0,
                'eye_positions': [],
                'smiles_detected': 0,
                'smile_area_ratio': 0.0
            }

        gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        gray_face = cv2.equalizeHist(gray_face)
        
        # Detect eyes in face region
        eyes = self.eye_cascade.detectMultiScale(
            gray_face,
            scaleFactor=1.08,
            minNeighbors=4,
            minSize=(max(12, int(w * 0.08)), max(12, int(h * 0.08)))
        )

        # Detect smile mostly in lower face region for better precision
        lower_face = gray_face[int(h * 0.45):, :]
        if lower_face is None or lower_face.size == 0:
            smiles = []
        else:
            smiles = self.smile_cascade.detectMultiScale(
                lower_face,
                scaleFactor=1.35,
                minNeighbors=10,
                minSize=(max(20, int(w * 0.2)), max(20, int(h * 0.08)))
            )

        smile_area_ratio = 0.0
        if len(smiles) > 0:
            largest_smile = max(smiles, key=lambda rect: rect[2] * rect[3])
            smile_area_ratio = (largest_smile[2] * largest_smile[3]) / max(1, (w * h))
        
        # Calculate features
        features = {
            'face_area': w * h,
            'face_ratio': w / h if h > 0 else 1,
            'eyes_detected': len(eyes),
            'eye_positions': eyes.tolist() if len(eyes) > 0 else [],
            'smiles_detected': len(smiles),
            'smile_area_ratio': round(smile_area_ratio, 4)
        }
        
        return features
    
    def estimate_emotion(self, features, has_face):
        """
        Estimate emotion based on facial features
        Uses heuristic rules for emotion classification
        """
        if not has_face:
            return {
                'emotion': 'not_detected',
                'confidence': 0.0,
                'description': 'No face detected'
            }
        
        # Initialize emotion scores
        emotion_scores = {
            'confident': 0.1,
            'neutral': 0.2,
            'nervous': 0.1,
            'anxious': 0.1
        }
        
        # Rule-based emotion estimation
        
        # Eyes detection indicates engagement
        if features['eyes_detected'] >= 2:
            emotion_scores['confident'] += 0.25
            emotion_scores['neutral'] += 0.2
        elif features['eyes_detected'] == 1:
            emotion_scores['neutral'] += 0.15
        else:
            emotion_scores['nervous'] += 0.25
            emotion_scores['anxious'] += 0.2

        # Smile strongly indicates confidence/positive engagement
        if features.get('smiles_detected', 0) > 0:
            emotion_scores['confident'] += 0.45
            emotion_scores['neutral'] += 0.1
            emotion_scores['nervous'] = max(0.05, emotion_scores['nervous'] - 0.08)
            emotion_scores['anxious'] = max(0.05, emotion_scores['anxious'] - 0.08)
        elif features.get('smile_area_ratio', 0) < 0.006:
            emotion_scores['neutral'] += 0.1
        
        # Face ratio analysis
        if features['face_ratio'] > 0.85:
            emotion_scores['confident'] += 0.1
        elif features['face_ratio'] < 0.75:
            emotion_scores['nervous'] += 0.12
            emotion_scores['anxious'] += 0.08
        
        # Face area (too small can indicate poor framing/engagement)
        if features['face_area'] > 40000:
            emotion_scores['confident'] += 0.08
        elif features['face_area'] < 20000:
            emotion_scores['nervous'] += 0.15
            emotion_scores['anxious'] += 0.12
        
        # Normalize scores
        total = sum(emotion_scores.values())
        if total > 0:
            emotion_scores = {k: v/total for k, v in emotion_scores.items()}
        
        # Get dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[dominant_emotion]
        
        # Map emotion to description
        emotion_descriptions = {
            'confident': 'Confident and engaged',
            'neutral': 'Calm and composed',
            'nervous': 'Slightly nervous',
            'anxious': 'Anxious or uncomfortable'
        }
        
        return {
            'emotion': dominant_emotion,
            'confidence': round(confidence * 100, 2),
            'all_scores': {k: round(v * 100, 2) for k, v in emotion_scores.items()},
            'description': emotion_descriptions[dominant_emotion]
        }
    
    def analyze_emotion_from_base64(self, base64_image):
        """Main function to analyze emotion from base64 image"""
        # Decode image
        image = self.decode_base64_image(base64_image)
        
        if image is None:
            return {
                'emotion': 'error',
                'confidence': 0,
                'description': 'Failed to decode image',
                'face_detected': False
            }
        
        # Detect face
        face_rect = self.detect_face(image)
        
        if face_rect is None:
            return {
                'emotion': 'not_detected',
                'confidence': 0,
                'description': 'No face detected in frame',
                'face_detected': False
            }
        
        # Analyze features
        features = self.analyze_facial_features(image, face_rect)
        
        # Estimate emotion
        emotion_result = self.estimate_emotion(features, True)
        emotion_result['face_detected'] = True
        emotion_result['features'] = features
        
        return emotion_result
    
    def calculate_confidence_from_emotions(self, emotion_timeline):
        """Calculate overall confidence score from emotion timeline"""
        if not emotion_timeline:
            return 5.0  # Neutral score
        
        # Define emotion weights for confidence
        emotion_weights = {
            'confident': 1.0,
            'neutral': 0.6,
            'nervous': 0.3,
            'anxious': 0.1,
            'not_detected': 0.5
        }
        
        # Calculate weighted average
        total_weight = 0
        weighted_sum = 0
        
        for entry in emotion_timeline:
            emotion = entry.get('emotion', 'neutral')
            weight = emotion_weights.get(emotion, 0.5)
            confidence = entry.get('confidence', 50) / 100
            
            weighted_sum += weight * confidence
            total_weight += confidence
        
        if total_weight == 0:
            return 5.0
        
        # Scale to 0-10
        confidence_score = (weighted_sum / total_weight) * 10
        return round(confidence_score, 2)
    
    def generate_emotion_insights(self, emotion_timeline):
        """Generate insights from emotion timeline"""
        if not emotion_timeline:
            return {
                'dominant_emotion': 'unknown',
                'consistency': 0,
                'suggestions': ['Unable to analyze - no emotion data available']
            }
        
        # Count emotions
        emotion_counts = {}
        for entry in emotion_timeline:
            emotion = entry.get('emotion', 'neutral')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Find dominant emotion
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        total_readings = len(emotion_timeline)
        consistency = (emotion_counts[dominant_emotion] / total_readings) * 100
        
        # Generate suggestions
        suggestions = []
        
        if dominant_emotion == 'confident':
            suggestions.append('Great job! You maintained confidence throughout')
            suggestions.append('Your body language and engagement were excellent')
        elif dominant_emotion == 'neutral':
            suggestions.append('You remained calm and composed')
            suggestions.append('Try to show more enthusiasm and engagement')
        elif dominant_emotion == 'nervous':
            suggestions.append('Practice mock interviews to build confidence')
            suggestions.append('Take deep breaths before answering')
            suggestions.append('Maintain eye contact with the camera')
        elif dominant_emotion == 'anxious':
            suggestions.append('Prepare thoroughly to reduce anxiety')
            suggestions.append('Remember to pause and think before answering')
            suggestions.append('Focus on your strengths and experiences')
        
        if consistency < 50:
            suggestions.append('Your emotions varied - try to maintain consistency')
        
        return {
            'dominant_emotion': dominant_emotion,
            'consistency': round(consistency, 2),
            'emotion_distribution': emotion_counts,
            'suggestions': suggestions
        }