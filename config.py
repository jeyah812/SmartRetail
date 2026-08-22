import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "smartretail-capstone-secret-key-2026")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    IMAGE_FOLDER = os.path.join(BASE_DIR, "static", "images")
    MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
    ENCODER_PATH = os.path.join(BASE_DIR, "models", "encoders.pkl")
    METRICS_PATH = os.path.join(BASE_DIR, "models", "model_metrics.json")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
