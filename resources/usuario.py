from hmac import compare_digest
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask_restful import Resource, reqparse
from Models.usuario import UsuarioModel
from blacklist import BLACKLIST


usuarios = [
    {

    }
]


class Usuarios(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ser nulo")
    argumentos.add_argument('user', type=str, required=True, help="O campo 'user' não pode ser nulo")
    argumentos.add_argument('senha', type=str, required=True, help="O senha 'nome' não pode ser nulo")

    def get(self):
        return {'usuarios': [usuario.json() for usuario in UsuarioModel.query.all()]}

    @jwt_required()
    def post(self):
        dados = Usuarios.argumentos.parse_args()
        if UsuarioModel.find_user(dados['user']):
            return {"message": f"Usuario {dados['user']} já existe"}
        usuario = UsuarioModel(**dados)
        try:
            usuario.save_usuario()
        except:
            return {"messagem": "Houve erro ao criar novo Usuário."}, 500
        return {"message": "Usuario criado com sucesso"}, 201


class Usuario(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str)
    argumentos.add_argument('user', type=str, required=True, help="O campo 'user' não pode ser nulo")
    argumentos.add_argument('senha', type=str, required=True, help="O senha 'nome' não pode ser nulo")

    def get(self, id):
        usuario = UsuarioModel.find_id(id)
        if usuario:
            return usuario.json()
        return {"message": "Id não encontrado"}

    @jwt_required()
    def put(self, id):
        dados = Usuario.argumentos.parse_args()
        usuario = UsuarioModel.find_id(id)
        if usuario:
            usuario.update_usuario(**dados)
            try:
                usuario.save_usuario()
            except:
                return {"messagem": f"Houve erro ao atualizar Usuário com Id: '{id}'."}, 500
            return usuario.json()
        return {"message": "Id não encontrado"}

    @jwt_required()
    def delete(self, id):
        usuario = UsuarioModel.find_id(id)
        if usuario:
            try:
                usuario.delete_usuario()
            except:
                return {"messagem": f"Houve erro ao deletar Usuário com Id: '{id}'."}, 500
            return {"message": f"Id '{id}' deletado"}
        return {"message": "Id não encontrado"}


class Login(Resource):
    login = False
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('user')
    argumentos.add_argument('senha')

    @classmethod
    def post(cls):
        dados = Usuario.argumentos.parse_args()
        usuario = UsuarioModel.find_user(dados['user'])
        if usuario and compare_digest(usuario.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=usuario.user)
            return {"access_token": token_de_acesso}, 200
        return {"message": "Usuário ou senha incorreto"}, 401


class Logoff(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {"message": "Logoff realizado com sucesso"}

