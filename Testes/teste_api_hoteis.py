import unittest
import requests


class TesteAPIHoteis(unittest.TestCase):
    URL = 'http://127.0.0.1:5000/hoteis'

    hotel = {
        'nome': 'Teste test',
        'estrela': '4',
        'cidade': 'Teste teste'
    }

    retorno_esperado = {
        'id': 4,
        'nome': 'Nomaa Hotel',
        'estrela': '4.2',
        'cidade': 'Curitiba'
    }

    update_hotel = {
        'id': 4,
        'nome': 'Nomaa Hotel',
        'estrela': '4.2',
        'cidade': 'Curitiba'
    }

    def teste_1_get_todos_hoteis(self):
        retorno = requests.get(self.URL)
        self.assertEqual(retorno.status_code, 200)
        self.assertEqual(len(retorno.json()), 1)
        print('Teste 1 completo!')

    def teste_2_post_hotel(self):
        retorno = requests.post(self.URL, json=self.hotel)
        self.assertEqual(retorno.status_code, 200)
        print('Teste 2 completo!')

    def teste_3_get_id_hotel(self):
        retorno = requests.get(self.URL + '/4')
        self.assertEqual(retorno.status_code, 200)
        self.assertEqual(retorno.json(), self.retorno_esperado)
        print('Teste 3 completo!')

    def teste_4_delete_id_hotel(self):
        retorno = requests.delete(self.URL + '/3')
        self.assertEqual(retorno.status_code, 200)
        print('Teste 4 completo!')

    def teste_5_update_hotel(self):
        retorno = requests.put(self.URL + '/4', json=self.update_hotel)
        self.assertEqual(retorno.json()["estrela"], self.update_hotel["estrela"])


if __name__ == "__main__":
    teste = TesteAPIHoteis()

    teste.teste_1_get_todos_hoteis()
    teste.teste_2_post_hotel()
    teste.teste_3_get_id_hotel()
    teste.teste_4_delete_id_hotel()
    teste.teste_5_update_hotel()
