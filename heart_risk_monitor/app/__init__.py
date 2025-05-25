from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Register custom template filters
@app.template_filter('format_number')
def format_number_filter(value):
    """Format a number with commas as thousands separators"""
    try:
        return "{:,}".format(int(value))
    except (ValueError, TypeError):
        return value

# Import routes at the end to avoid circular imports
from app.routes import init_routes

# Initialize routes
init_routes(app)
