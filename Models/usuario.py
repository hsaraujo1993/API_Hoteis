from sql_alchemy import banco


class UsuarioModel(banco.Model):
    __tablename__ = 'users'

    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    user = banco.Column(banco.String(15))
    senha = banco.Column(banco.String(16))

    def __init__(self, nome, user, senha):
        self.nome = nome
        self.user = user
        self.senha = senha

    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'user': self.user,
        }

    def json_cadastro(self):
        return {
            'user': self.user,
            'senha': self.senha
        }

    @classmethod
    def find_id(cls, id):
        usuario = cls.query.filter_by(id=id).first()
        if usuario:
            return usuario
        return None

    @classmethod
    def find_user(cls, user):
        usuario = cls.query.filter_by(user=user).first()
        if usuario:
            return usuario
        return None

    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    def update_usuario(self, nome, user, senha):
        self.nome = nome
        self.user = user
        self.senha = senha

    def delete_usuario(self):
        banco.session.delete(self)
        banco.session.commit()

