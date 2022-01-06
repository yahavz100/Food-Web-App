from datetime import timedelta
from flask import Flask
from webApp.routes import main_bp

app = Flask(__name__, template_folder='templates')
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)
app.register_blueprint(main_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
