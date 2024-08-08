import logging
import json
import requests
import azure.functions as func
from azure.identity import DefaultAzureCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Obter token de acesso usando DefaultAzureCredential
        credential = DefaultAzureCredential()
        token = credential.get_token("https://graph.microsoft.com/.default")
        
        # Verificar se o token foi recebido com sucesso
        if not token.token:
            raise Exception("Token não foi obtido com sucesso.")

        # Obter o CEP da solicitação
        cep = req.params.get('cep')
        if not cep:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                cep = req_body.get('cep')

        if not cep:
            return func.HttpResponse(
                "CEP não fornecido.",
                status_code=400
            )

        # Consultar o CEP usando uma API pública (por exemplo, ViaCEP)
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        
        if response.status_code != 200:
            return func.HttpResponse(
                f"Erro ao consultar o CEP: {response.text}",
                status_code=response.status_code
            )

        cep_info = response.json()

        return func.HttpResponse(
            json.dumps(cep_info),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Erro: {str(e)}")
        return func.HttpResponse(
            str(e),
            status_code=500
        )