import os
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main():
    try:
        # Certifique-se de configurar as variáveis de ambiente COUCH_USERNAME e IAM_API_KEY
        client = Cloudant.iam(
            account_name=os.environ["COUCH_USERNAME"],
            api_key=os.environ["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("Erro ao conectar ao Cloudant")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("Erro de conexão")
        return {"error": err}

    return {"dbs": client.all_dbs()}

if __name__ == "__main__":
    result = main()
    print(result)
