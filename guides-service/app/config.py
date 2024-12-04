import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SESSION_TYPE = 'redis'
    SESSION_REDIS = os.getenv('REDIS_URI', 'redis://localhost:6379/0')
