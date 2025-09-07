from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register routes
    from .routes import bp
    app.register_blueprint(bp)

    return app

# For simple direct execution: flask --app app run (if using factory adapt)
app = create_app()
