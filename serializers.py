from flask_restplus import Namespace

api = Namespace('Guia de recolhimento.', description='Gera e recalcula guias de recolhimento.')

guia_parser = api.parser()
guia_parser.add_argument('nome', required=True, type=str, help='Razão social da empresa', location='form')
guia_parser.add_argument('num_doc', required=True, type=str, help='Número do CNPJ da empresa', location='form')
guia_parser.add_argument('insc_estadual', required=True, type=str, help='Inscrição estadual da empresa', location='form')
guia_parser.add_argument('cep', required=True, type=str, help='CEP da empresa', location='form')
guia_parser.add_argument('endereco', required=True, type=str, help='Endereço da empresa', location='form')
guia_parser.add_argument('bairro', required=True, type=str, help='Bairro da empresa', location='form')
guia_parser.add_argument('cidade', required=True, type=str, help='Cidade da empresa', location='form')
guia_parser.add_argument('uf', required=True, type=str, help='UF da empresa', location='form')
guia_parser.add_argument('cod_receita', required=True, type=str, help='Código da receita do imposto', location='form')
guia_parser.add_argument('data_vencimento', required=True, type=str, help='Data de vencimento da guia', location='form')
guia_parser.add_argument('num_nota', required=True, type=str, help='Número da nota à qual a guia é referente', location='form')
guia_parser.add_argument('valor', required=True, type=str, help='Valor da nota', location='form')
guia_parser.add_argument('obs', required=True, type=str, help='Observação à ser inserida na nota', location='form')
guia_parser.add_argument('exercicio', required=True, type=str, help='Ano de emissão da guia', location='form')
guia_parser.add_argument('referencia', required=True, type=str, help='Mês de emissão da nota', location='form')