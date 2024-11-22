class Config:
    SECRET_KEY = "your-secret-key"
    DEBUG = True


class DevelopmentConfig(Config):
    ENV = "development"


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
