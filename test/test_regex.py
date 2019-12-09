import sys
import unittest
from bs4 import BeautifulSoup

from src import lambda_aws


class TestRegexProcess1(unittest.TestCase):
    PATH_HTML = "../data/processo1.html"

    @classmethod
    def setUpClass(cls):
        with open(cls.PATH_HTML, "rb") as html_file:
            b_html = html_file.read()

        cls.json_process_data = lambda_aws.get_process_data(BeautifulSoup(b_html, features="html.parser"))
        cls.json_process_parts = lambda_aws.get_process_parts(BeautifulSoup(b_html, features="html.parser"))
        cls.json_last_movement = lambda_aws.get_last_move(BeautifulSoup(b_html, features="html.parser"))

    def test_process_data(self):
        self.assertEqual(type({}), type(self.json_process_data))
        self.assertEqual('1048561-15.2019.8.26.0053', self.json_process_data['process_number'])
        self.assertEqual('Procedimento do Juizado Especial', self.json_process_data['class']['type'])
        self.assertEqual('Cível', self.json_process_data['class']['area'])
        self.assertNotEqual('MARIA ISABEL ROMERO RODRIGUES HENRIQUES', self.json_process_data['judge'])
        self.assertEqual('Maria Isabel Romero Rodrigues Henriques', self.json_process_data['judge'])
        self.assertEqual('R$ 1.000,00', self.json_process_data['value'])

    def test_process_parts(self):
        self.assertEqual(type({}), type(self.json_process_parts))
        self.assertEqual('Reqte', list(self.json_process_parts.keys())[0])
        self.assertEqual('Reqdo', list(self.json_process_parts.keys())[1])
        self.assertEqual('Adolpho Onofre Galliano', self.json_process_parts['Reqte']['name'])
        self.assertEqual(1, len(self.json_process_parts['Reqte']['Advogad(a/o)']))
        self.assertNotEqual('Tiago Henrique dos Santos Gois', self.json_process_parts['Reqte']['Advogad(a/o)'][0])
        self.assertEqual('Tiago Henrique Dos Santos Gois', self.json_process_parts['Reqte']['Advogad(a/o)'][0])
        self.assertEqual('Prefeitura de São Paulo', self.json_process_parts['Reqdo']['name'])

    def test_last_movement(self):
        self.assertEqual('18/09/2019', self.json_last_movement['date'])
        self.assertEqual('Certidão de Publicação Expedida', self.json_last_movement['movement'])
        self.assertEqual('Relação :0172/2019 Data da Disponibilização: 18/09/2019 Data da Publicação: 19/09/2019 Número do Diário: 2894 Página: 1336/1348',
                         self.json_last_movement['info'])


class TestRegexProcess2(unittest.TestCase):
    PATH_HTML = "../data/processo2.html"

    @classmethod
    def setUpClass(cls):
        with open(cls.PATH_HTML, "rb") as html_file:
            b_html = html_file.read()

        cls.json_process_data = lambda_aws.get_process_data(BeautifulSoup(b_html, features="html.parser"))
        cls.json_process_parts = lambda_aws.get_process_parts(BeautifulSoup(b_html, features="html.parser"))
        cls.json_last_movement = lambda_aws.get_last_move(BeautifulSoup(b_html, features="html.parser"))

    def test_process_data(self):
        self.assertEqual(type({}), type(self.json_process_data))
        self.assertEqual('1047868-31.2019.8.26.0053', self.json_process_data['process_number'])
        self.assertEqual('Mandado de Segurança Cível', self.json_process_data['class']['type'])
        self.assertEqual('Cível', self.json_process_data['class']['area'])
        self.assertNotEqual('Marcos de Lima Porta', self.json_process_data['judge'])
        self.assertEqual('Marcos De Lima Porta', self.json_process_data['judge'])
        self.assertEqual('R$ 50.000,00', self.json_process_data['value'])

    def test_process_parts(self):
        self.assertEqual(type({}), type(self.json_process_parts))
        self.assertEqual('Imptte', list(self.json_process_parts.keys())[0])
        self.assertEqual('Imptdo', list(self.json_process_parts.keys())[1])
        self.assertEqual('Serviço Social do Comércio - Sesc', self.json_process_parts['Imptte']['name'])
        self.assertEqual(1, len(self.json_process_parts['Imptte']['Advogad(a/o)']))
        self.assertEqual('Alessandra Passos Gotti', self.json_process_parts['Imptte']['Advogad(a/o)'][0])
        self.assertEqual('Diretor do Departamento de Tributação e Julgamento - Dejug', self.json_process_parts['Imptdo']['name'])

    def test_last_movement(self):
        self.assertEqual('19/09/2019', self.json_last_movement['date'])
        self.assertEqual('Mandado Devolvido Cumprido Positivo', self.json_last_movement['movement'])
        self.assertEqual('Certidão - Oficial de Justiça - Mandado Cumprido Positivo',
                         self.json_last_movement['info'])


class TestRegexProcess3(unittest.TestCase):
    PATH_HTML = "../data/processo3.html"

    @classmethod
    def setUpClass(cls):
        with open(cls.PATH_HTML, "rb") as html_file:
            b_html = html_file.read()

        cls.json_process_data = lambda_aws.get_process_data(BeautifulSoup(b_html, features="html.parser"))
        cls.json_process_parts = lambda_aws.get_process_parts(BeautifulSoup(b_html, features="html.parser"))
        cls.json_last_movement = lambda_aws.get_last_move(BeautifulSoup(b_html, features="html.parser"))

    def test_process_data(self):
        self.assertEqual(type({}), type(self.json_process_data))
        self.assertEqual('0026087-34.2000.8.26.0053', self.json_process_data['process_number'])
        self.assertEqual('Procedimento Comum Cível', self.json_process_data['class']['type'])
        self.assertEqual('Cível', self.json_process_data['class']['area'])
        self.assertEqual('Wellington Urbano Marinho', self.json_process_data['judge'])
        self.assertEqual('R$ 4.886.228,30', self.json_process_data['value'])

    def test_process_parts(self):
        self.assertEqual(type({}), type(self.json_process_parts))
        self.assertEqual('Reqte', list(self.json_process_parts.keys())[0])
        self.assertEqual('Reqdo', list(self.json_process_parts.keys())[1])
        self.assertEqual('Companhia de Saneamento Básico do Estado de São Paulo- Sabesp', self.json_process_parts['Reqte']['name'])
        self.assertEqual(4, len(self.json_process_parts['Reqte']['Advogad(a/o)']))
        self.assertNotEqual('GISLAINE MARIA BERARDO', self.json_process_parts['Reqte']['Advogad(a/o)'][0])
        self.assertEqual('Gislaine Maria Berardo', self.json_process_parts['Reqte']['Advogad(a/o)'][0])
        self.assertNotEqual('MANOEL GUERRERO RAMOS', self.json_process_parts['Reqte']['Advogad(a/o)'][1])
        self.assertEqual('Manoel Guerrero Ramos', self.json_process_parts['Reqte']['Advogad(a/o)'][1])
        self.assertEqual('Maria Juliana Lopes Lenharo Botura', self.json_process_parts['Reqte']['Advogad(a/o)'][2])
        self.assertEqual('Renata Costa Bomfim', self.json_process_parts['Reqte']['Advogad(a/o)'][3])
        self.assertEqual('Prefeitura de São Paulo', self.json_process_parts['Reqdo']['name'])
        self.assertEqual('Katia Leite', self.json_process_parts['Reqdo']['Advogad(a/o)'][0])
        self.assertNotEqual('Marcos Vinicius Sales dos Santos', self.json_process_parts['Reqdo']['Advogad(a/o)'][1])
        self.assertEqual('Marcos Vinicius Sales Dos Santos', self.json_process_parts['Reqdo']['Advogad(a/o)'][1])
        self.assertEqual('Gian Paolo Gasparini', self.json_process_parts['Reqdo']['Advogad(a/o)'][2])

    def test_last_movement(self):
        self.assertEqual('03/09/2019', self.json_last_movement['date'])
        self.assertEqual('Recebidos os Autos do Distribuidor local', self.json_last_movement['movement'])
        self.assertEqual('A tramitação se dará nos incidentes digitais em andamento, onde prosseguirá com peticionamento eletrônico. Os autos ficarão à disposição em cartório para eventual consulta pelo prazo de 30 dias a contar da movimentação do recebimento nesta Unidade.',
                         self.json_last_movement['info'])


if __name__ == '__main__':
    unittest.main()
