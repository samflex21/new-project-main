from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Import routes at the end to avoid circular imports
from app.routes import init_routes

# Initialize routes
init_routes(app)
