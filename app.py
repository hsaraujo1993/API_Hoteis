from flask import Flask, jsonify
from flask_restful import Api
from resources.usuario import Usuarios, Usuario, Login, Logoff
from resources.hotel import Hoteis, Hotel
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'chave'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)


@app.before_request
def cria_banco():
    banco.create_all()


@jwt.token_in_blocklist_loader
def verificar_backlist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({"message": "Token inativado"}), 401


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<int:id>')
api.add_resource(Usuarios, '/usuarios')
api.add_resource(Usuario, '/usuarios/<int:id>')
api.add_resource(Login, '/login')
api.add_resource(Logoff, '/logoff')

if __name__ == '__main__':
    from sql_alchemy import banco

    banco.init_app(app)
    app.run(debug=True)
