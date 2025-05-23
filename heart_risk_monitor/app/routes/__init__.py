from flask import redirect, url_for

def init_routes(app):
    # Import blueprint modules
    from app.routes.analytical import analytical_bp
    from app.routes.managerial import managerial_bp
    from app.routes.api import api_bp
    from app.routes.patient import patient_bp
    
    # Register blueprints
    app.register_blueprint(analytical_bp)
    app.register_blueprint(managerial_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(patient_bp)
    
    # Define root route
    @app.route('/')
    def index():
        # Redirect to analytical dashboard as the main page
        return redirect(url_for('analytical.dashboard'))
