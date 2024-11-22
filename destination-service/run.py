from app import create_app
from config import DevelopmentConfig

app = create_app()
app.config.from_object(DevelopmentConfig)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
