from flask import Flask, jsonify, request, render_template, url_for, redirect
from sqlalchemy.exc import SQLAlchemyError
import models

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/flask_db'
    
    models.db.init_app(app)
    
    User = models.User
      
    @app.route('/')
    def index():
        users = User.query.all()
        return render_template('index.html', users=users)

    @app.route('/add_user', methods=['POST'])
    def add_user():
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            new_user = User(username=username, email=email, password=password)
            models.db.session.add(new_user)
            models.db.session.commit()

            return redirect(url_for('index'))

        except SQLAlchemyError as e:
            models.db.session.rollback()
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/delete_user/<int:user_id>', methods=['POST'])
    def delete_user(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "User not found"}), 404

            models.db.session.delete(user)
            models.db.session.commit()

            return redirect(url_for('index'))

        except SQLAlchemyError as e:
            models.db.session.rollback()
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app

if __name__ == '__main__':
     app = create_app()
     app.run(host='0.0.0.0', port=5001)