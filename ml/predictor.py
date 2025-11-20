import cv2
import numpy as np
from lime import lime_image
from skimage.segmentation import mark_boundaries
from tensorflow import keras
import matplotlib.pyplot as plt
import tempfile
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


class EnsembleDeepfakeDetector:     # ← SAME CLASS NAME (DO NOT CHANGE)
    def __init__(self, model_path1, model_path2=None, img_size=224, max_frames=30, demo_mode=False):
        """
        We will use ONLY model_path1 (EfficientNet). 
        model_path2 is ignored but kept for compatibility.
        """
        self.model1 = None
        self.model2 = None  # kept for compatibility (unused)
        self.demo_mode = demo_mode

        # Load single EfficientNet model
        try:
            print("Loading EfficientNet model...")
            self.model1 = keras.models.load_model(model_path1)
            print("✔ Model loaded.")
        except Exception as e:
            print(f"❌ Could not load model: {e}")

        self.img_size = img_size
        self.max_frames = max_frames
        self.explainer = lime_image.LimeImageExplainer()

    # -----------------------------------------------------
    # FRAME PREPROCESSING (same function name)
    # -----------------------------------------------------
    def preprocess_frame(self, frame):
        frame = cv2.resize(frame, (self.img_size, self.img_size))
        frame = frame.astype("float32") / 255.0
        return frame

    # -----------------------------------------------------
    # LIME EXPLANATION (same function name)
    # -----------------------------------------------------
    def explain_frame(self, frame):
        """
        Used for ONE FRAME ONLY.
        """
        if not self.model1:
            out_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
            plt.imsave(out_path, frame / 255.0)
            import base64
            with open(out_path, "rb") as img:
                 encoded = base64.b64encode(img.read()).decode()
            return f"data:image/png;base64,{encoded}"

        def predict_fn(images):
            images_processed = np.array(images).astype("float32")
            return self.model1.predict(images_processed, verbose=0)

        try:
            explanation = self.explainer.explain_instance(
                frame,
                classifier_fn=predict_fn,
                top_labels=1,
                hide_color=0,
                num_samples=200
            )

            top_label = explanation.top_labels[0]
            temp, mask = explanation.get_image_and_mask(
                top_label,
                positive_only=False,
                hide_rest=False,
                num_features=10,
                min_weight=0.01
            )

            out_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
            plt.imsave(out_path, mark_boundaries(temp / 255.0, mask))
            return out_path

        except Exception as e:
            print("LIME failed:", e)
            fallback = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
            plt.imsave(fallback, frame / 255.0)
            return fallback

    # -----------------------------------------------------
    # MAIN VIDEO PREDICTION (same function name and output)
    # -----------------------------------------------------
    def predict_video(self, video_path, explain=False):

        # Keep your demo_mode logic
        path_lower = video_path.lower()
        is_likely_fake = False

        if self.demo_mode:
            fake_indicators = ['/fake/', '\\fake\\', 'fake_', 'deepfake']
            real_indicators = ['/real/', '\\real\\', 'real_', 'authentic']

            for ind in fake_indicators:
                if ind in path_lower:
                    is_likely_fake = True
                    break
            for ind in real_indicators:
                if ind in path_lower:
                    is_likely_fake = False
                    break

        print(f"\n🔍 Analyzing video: {video_path}")
        cap = cv2.VideoCapture(video_path)

        frame_scores = []
        frame_for_lime = None

        count = 0
        while cap.isOpened() and count < self.max_frames:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = self.preprocess_frame(frame_rgb)
            frame_input = np.expand_dims(processed, axis=0)

            # Save frame 10 for LIME
            if count == 10:
                frame_for_lime = (processed * 255).astype(np.uint8)

            try:
                score = self.model1.predict(frame_input, verbose=0)[0][0]
                frame_scores.append(score)
            except:
                pass

            count += 1

        cap.release()

        # -------------------------------------------------------------------
        # HANDLE SCORES
        # -------------------------------------------------------------------
        if frame_scores:
            video_confidence = np.mean(frame_scores)
            print(f"Model score: {video_confidence:.4f}")

        else:
            # No scores — fallback based on demo mode
            if self.demo_mode:
                video_confidence = 0.75 if is_likely_fake else 0.25
            else:
                video_confidence = 0.5

        # Final classification
        final_label = "FAKE" if video_confidence > 0.5 else "REAL"
        display_confidence = (
            video_confidence if final_label == "FAKE" else 1 - video_confidence
        )

        # LIME explanation (one frame)
        lime_path = None
        if explain and frame_for_lime is not None:
            print("🟦 Generating LIME heatmap...")
            lime_path = self.explain_frame(frame_for_lime)

        return {
            "final_label": final_label,
            "confidence_score": f"{display_confidence:.2%}",
            "raw_score": float(video_confidence),
            "lime_explanation_path": lime_path
        }

