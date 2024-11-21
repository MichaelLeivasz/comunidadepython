#este arquivo "__init__" irá rodar sempre que a pasta "comunidadepython" for "chamada" (semelhante a uma estrutura de classes, que quando é chamada roda o init).
#aqui fica as configurações iniciais do app e do banco de dados.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm.path_registry import PropRegistry

app = Flask(__name__)

app.config['SECRET_KEY'] = 'edfbbe12c0dd87893675b3c8d0ec7eb4'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app) #segurança para senhas dos usuarios
login_manager = LoginManager(app)
login_manager.login_view = 'login' #redirecionar o usuario para página de login, se ele estiver tentando acessar uma página que só aparece para quem está logado.
login_manager.login_message_category = 'alert-info'

from comunidadepython import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Base de dados criada")
else:
    print("Base de dados já existente")


#para que as páginas/routes do site sejam rodadas, preciso importar elas neste arquivo. A importação é feita após colocarmos o app no ar, pois, os routes precisam do app para funcionar.
from comunidadepython import routes

