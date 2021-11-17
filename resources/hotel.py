from flask_restful import Resource, reqparse
from Models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

hoteis = [
    {

    }
]


def parametros_path(cidade=None,
                    estrela_minimo=0,
                    estrela_maximo=5,
                    limit=5,
                    offset=0, **dados):
    if cidade:
        return {
            'estrela_minimo': estrela_minimo,
            'estrela_maximo': estrela_maximo,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
    return {
        'estrela_minimo': estrela_minimo,
        'estrela_maximo': estrela_maximo,
        'limit': limit,
        'offset': offset
    }


path_parametros = reqparse.RequestParser()
path_parametros.add_argument('cidade', type=str)
path_parametros.add_argument('estrela_minimo', type=float)
path_parametros.add_argument('estrela_maximo', type=float)
path_parametros.add_argument('limit', type=float)
path_parametros.add_argument('offset', type=float)


class Hoteis(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ser nulo")
    argumentos.add_argument('estrela', type=float, required=True, help="O campo 'estrela' não pode ser nulo")
    argumentos.add_argument('cidade', type=str, required=True, help="O campo 'cidade' não pode ser nulo")

    def get(self):

        conexao = sqlite3.connect('banco.db')
        cursor = conexao.cursor()

        dados = path_parametros.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = parametros_path(**dados_validos)

        if not parametros.get('cidade'):
            consulta = "SELECT * FROM hoteis WHERE (estrela >= ? and estrela <= ?) \
                       LIMIT ? OFFSET ?"
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM hoteis WHERE (estrela >= ? and estrela <= ?) \
                        and cidade = ? LIMIT ? OFFSET ?"
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
            
        hoteis = []
        for linha in resultado:
            hoteis.append({
                'id': linha[0],
                'nome': linha[1],
                'estrela': linha[2],
                'cidade': linha[3]
            })
        
        return {'hoteis': hoteis}

    @jwt_required()
    def post(self):

        dados = Hoteis.argumentos.parse_args()
        hotel = HotelModel(**dados)
        try:
            hotel.save_hotel()
        except:
            return {"messagem": "Houve erro ao criar novo Hotel."}, 500
        return {"message": "Hotel criado com sucesso"}, 200


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ser nulo")
    argumentos.add_argument('estrela', type=float, required=True, help="O campo 'estrela' não pode ser nulo")
    argumentos.add_argument('cidade', type=str, required=True, help="O campo 'cidade' não pode ser nulo")

    def get(self, id):

        hotel = HotelModel.find_hotel(id)
        if hotel:
            return hotel.json()
        return {"message": f"Id '{id}' não encontrado"}, 404


    def put(self, id):

        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {"messagem": f"Houve erro ao atualizar Hotel com Id: '{id}'."}, 500
            return hotel_encontrado.json(), 200
        return {"message": f"id '{id}' não encontrado"}, 404


    def delete(self, id):

        hotel = HotelModel.find_hotel(id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {"messagem": f"Houve erro ao deletar Hotel com Id: '{id}'."}, 500
            return {"message": f"Hotel Id '{id}' deletado"}, 200
        return {"message": f"Id '{id}' não encontrado"}, 404
