from sql_alchemy import banco


class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    nome = banco.Column(banco.String(80))
    estrela = banco.Column(banco.String(80))
    cidade = banco.Column(banco.String(80))

    def __init__(self, nome, estrela, cidade):
        self.nome = nome
        self.estrela = estrela
        self.cidade = cidade

    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'estrela': self.estrela,
            'cidade': self.cidade
        }

    @classmethod
    def find_hotel(cls, id):
        hotel = cls.query.filter_by(id=id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrela, cidade):
        self.nome = nome
        self.estrela = estrela
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
