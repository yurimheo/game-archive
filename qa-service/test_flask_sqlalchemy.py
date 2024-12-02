try:
    from flask_sqlalchemy import SQLAlchemy
    print("Flask-SQLAlchemy imported successfully.")
except ImportError as e:
    print(f"Error: {e}")
