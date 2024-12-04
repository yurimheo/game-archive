import jwt as pyjwt
from flask import request, jsonify
from functools import wraps

SECRET_KEY = "supersecretkey"

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Decoded token:", g.user)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization token required"}), 401

        token = auth_header.split(" ")[1]
        try:
            decoded_token = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded_token  
        except pyjwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except pyjwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function
