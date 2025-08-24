import unittest
from datetime import date

# Função utilitária para cálculo do valor total da reserva
def calcular_total(preco_noite, data_inicio, data_fim):
    noites = (data_fim - data_inicio).days
    return preco_noite * noites

# Função utilitária para validação de datas
def datas_validas(data_inicio, data_fim):
    return data_fim > data_inicio

class TestReservaUtils(unittest.TestCase):
    def test_calculo_total(self):
        preco = 100.0
        inicio = date(2024, 12, 1)
        fim = date(2024, 12, 4)
        total = calcular_total(preco, inicio, fim)
        self.assertEqual(total, 300.0)

    def test_datas_validas(self):
        inicio = date(2024, 12, 1)
        fim = date(2024, 12, 4)
        self.assertTrue(datas_validas(inicio, fim))
        self.assertFalse(datas_validas(fim, inicio))
        self.assertFalse(datas_validas(inicio, inicio))

    def test_capacidade_maxima(self):
        capacidade = 4
        convidados = [2, 4, 5]
        self.assertTrue(convidados[0] <= capacidade)
        self.assertTrue(convidados[1] <= capacidade)
        self.assertFalse(convidados[2] <= capacidade)

if __name__ == "__main__":
    unittest.main()
