# pylint: disable=cyclic-import
"""
Copyright (c) 2024 Anchita Ramani, Meet Patel, Abhinav Jami
This code is licensed under MIT license (see LICENSE for details)

@author: FilmFolio
"""
<<<<<<< HEAD
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy #used for integrating SQLite
from flask_bcrypt import Bcrypt #used for hashing passwords
from flask_cors import CORS #allows the server to handle requests from different origins
from flask_login import LoginManager  #manages user sessions in Flask
from flask_socketio import SocketIO #for real time communication

app = Flask(__name__) #creates an instance
=======
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO


app = Flask(__name__)
>>>>>>> 38ee9baa60d52f7efac66fc7cb68fa0dfe43c6c2
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
socket = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
cors = CORS(app, resources={
    r"/*": {
        "origins": "*" # * allows for all origins
    }
})

#pylint: disable=wrong-import-position
from src import routes
