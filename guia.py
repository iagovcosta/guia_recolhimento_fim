import requests
import base64
import json


class Guia:

    def __init__(self):
        self.__session = requests.session()
        self.__header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '114',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'ASP.NET_SessionId={}',
            'Host': 'www2.agencianet.fazenda.df.gov.br',
            'Origin': 'https://www2.agencianet.fazenda.df.gov.br',
            'Referer': 'https://www2.agencianet.fazenda.df.gov.br/DarAvulso/',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.__url = 'https://www2.agencianet.fazenda.df.gov.br/DarAvulso/Home/'


    def get_session_id(self):

        self.__session.get('https://www2.agencianet.fazenda.df.gov.br/DarAvulso/')
        session_id = self.__session.cookies.get_dict()
        session_id = session_id['ASP.NET_SessionId']

        return session_id

    def injeta_dados(self, data):

        payload = {
            "NumDocumento": data['num_doc'],
            "TipoDocumento": "CNPJ",
            "CodReceita": data['cod_receita'],
            "Inscricao": "",
            "CapchaResponse": ""
        }

        self.__session.post(self.__url + 'PreencherDAR',
                                headers=self.__header.update({'Cookie': 'ASP.NET_SessionId={}'.format(self.get_session_id())}),
                                data=payload)


        with open('gravar_dar_payload.json', 'r') as gravar_dar_payload:
            gravar_dar_payload = json.load(gravar_dar_payload)

        self.__header['Content-Length'] = '2445'
        self.__header['Cookie'] = 'ASP.NET_SessionId={}'.format(self.get_session_id())

        gravar_dar_payload['NumDocumento'] = str(data['num_doc'])
        gravar_dar_payload['Contribuinte']['NumDocumento'] = str(data['num_doc'])
        gravar_dar_payload['CodReceita'] = str(data['cod_receita'])
        gravar_dar_payload['Exercicio'] = str(data['exercicio'])
        gravar_dar_payload['Referencia'] = str(data['referencia'])
        gravar_dar_payload['DtaVencimento'] = str(data['data_vencimento'])
        gravar_dar_payload['ValOriginal'] = str(data['valor'])
        gravar_dar_payload['ValTotal'] = str(data['valor'])
        gravar_dar_payload['Observacao'] = str(data['obs'])
        gravar_dar_payload['NroDoc'] = str(data['num_nota'])
        gravar_dar_payload['Contribuinte']['Inscricao'] = str(data['insc_estadual'])
        gravar_dar_payload['Contribuinte']['ListaInscricao'] = str(data['insc_estadual'])
        gravar_dar_payload['Contribuinte']['NomeRazao'] = str(data['nome'])
        gravar_dar_payload['Contribuinte']['Cep'] = str(data['cep'])
        gravar_dar_payload['Contribuinte']['Logradouro'] = str(data['endereco'])
        gravar_dar_payload['Contribuinte']['Bairro'] = str(data['bairro'])
        gravar_dar_payload['Contribuinte']['Cidade'] = str(data['cidade'])
        gravar_dar_payload['Contribuinte']['UF'] = str(data['uf'])

        if data['cod_receita'] == '1568' or data['cod_receita'] == '1317' or data['cod_receita'] == '1560' or data['cod_receita'] == '1558' or data['cod_receita'] == '1563':
            gravar_dar_payload.pop('NroDoc')
            gravar_dar_payload['TipDoc'] = None

        gravarDAR = self.__session.post(url='https://www2.agencianet.fazenda.df.gov.br/DarAvulso/Home/GravarDAR',
        data=json.dumps(gravar_dar_payload),
        headers=self.__header)

        return gravarDAR.text


    def get_valores_calculados(self, data):

        valores_recalculo = json.loads(self.injeta_dados(data))

        val_multa = valores_recalculo['ValMulta']
        val_juros = valores_recalculo['ValJuros']
        exercicio = valores_recalculo['Exercicio']
        referencia = valores_recalculo['CotaOuRef']
        valor_total = valores_recalculo['ValTotal']

        dictio = {
            "val_multa": val_multa,
            "val_juros": val_juros,
            "exercicio": exercicio,
            "referencia": referencia,
            "valor_total": valor_total
        }

        return dictio

    def gera_boleto(self, data):

        with open('emitir_boleto_payload.json', 'r') as emitir_boleto_payload:
            emitir_boleto_payload = json.load(emitir_boleto_payload)

            valores_calculados = self.get_valores_calculados(data)

            self.__header['Content-Length'] = '4311'
            self.__header['Cookie'] = 'ASP.NET_SessionId={}'.format(self.get_session_id())

            emitir_boleto_payload['Boleto']['Contribuinte']['NumDocumento'] = str(data['num_doc'])
            emitir_boleto_payload['Boleto']['Contribuinte']['Inscricao'] = str(data['insc_estadual'])
            emitir_boleto_payload['Boleto']['Contribuinte']['ListaInscricao'] = [str(data['insc_estadual'])]
            emitir_boleto_payload['Boleto']['Contribuinte']['NomeRazao'] = str(data['nome'])
            emitir_boleto_payload['Boleto']['Contribuinte']['Cep'] = str(data['cep'])
            emitir_boleto_payload['Boleto']['Contribuinte']['Logradouro'] = str(data['endereco'])
            emitir_boleto_payload['Boleto']['Contribuinte']['Bairro'] = str(data['bairro'])
            emitir_boleto_payload['Boleto']['Contribuinte']['Cidade'] = str(data['cidade'])
            emitir_boleto_payload['Boleto']['Contribuinte']['UF'] = str(data['uf'])
            emitir_boleto_payload['Boleto']['NumDoc'] = str(data['num_nota'])
            emitir_boleto_payload['Boleto']['Receita']['CodReceita'] = str(data['cod_receita'])
            emitir_boleto_payload['Boleto']['Observacoes'] = str(data['obs'])
            emitir_boleto_payload['Boleto']['CotaOuRef'] = str(data['referencia'])
            emitir_boleto_payload['Boleto']['DtaVencimento'] = str(data['data_vencimento'])
            emitir_boleto_payload['Boleto']['DtaPagamento'] = str(data['data_vencimento'])
            emitir_boleto_payload['Boleto']['DtaPagamentoFormat'] = str(data['data_vencimento'])
            emitir_boleto_payload['Boleto']['ValOriginal'] = str(data['valor'])
            emitir_boleto_payload['Boleto']['ValPrincipal'] = str(data['valor'])
            emitir_boleto_payload['Boleto']['ValMulta'] = valores_calculados['val_multa']
            emitir_boleto_payload['Boleto']['ValJuros'] = valores_calculados['val_juros']
            emitir_boleto_payload['Boleto']['ValTotal'] = valores_calculados['valor_total']


            emitirBoleto = self.__session.post(self.__url + 'EmitirBoleto',
                                                headers=self.__header,
                                                data=json.dumps(emitir_boleto_payload))

            return emitirBoleto.text

    def gera_pdf(self, data):

        self.__header['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        self.__header['Content-Length'] = '1129'
        self.__header['Content-Type'] = 'application/json'
        self.__header['Cookie'] = 'ASP.NET_SessionId={}'.format(self.get_session_id())
        self.__header['X-Requested-With'] = 'XMLHttpRequest'

        emitirPDF = self.__session.post(url='https://www2.agencianet.fazenda.df.gov.br/DarAvulso/Home/EmitirBoletoPDF',
                                 headers=self.__header,
                                 data=self.gera_boleto(data))

        return emitirPDF.text

    def get_fname(self, data):
        fName = self.gera_pdf(data)
        return fName

    def download_file(self, data):

        fName = json.loads(self.get_fname(data))['fName']
        download_file = self.__session.get('https://www2.agencianet.fazenda.df.gov.br/DarAvulso/Home/DownloadFile?fName={}'.format(fName))

        return download_file.content

    def pdf_to_base64(self, data):
        pdf_base64 = base64.b64encode(self.download_file(data))
        pdf_base64 = str(pdf_base64)

        return pdf_base64

    def guia(self, data):
        return {'detalhes': json.loads(self.gera_boleto(data)),
                'documento': self.pdf_to_base64(data)}
