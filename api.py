import requests
import os
from dotenv import load_dotenv
import pprint
import argparse

os.environ.clear()

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--MLB', nargs='+', type=str, required=True, help='Lista de códigos MLB')
args = parser.parse_args()

# Lê dados do .env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CODE = os.getenv("CODE")

# Lista de MLBs
mlb_list = args.MLB # Substitua pelos seus códigos

# Atualiza .env com novo refresh_token
def update_refresh_token(new_token):
    lines = []
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("REFRESH_TOKEN="):
                lines.append(f"REFRESH_TOKEN={new_token}\n")
            else:
                lines.append(line)
    with open(".env", "w") as f:
        f.writelines(lines)

# Gera access_token usando refresh_token
def refresh_access_token(refresh_token):
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        token_info = response.json()
        update_refresh_token(token_info["refresh_token"])
        return token_info["access_token"]
    else:
        print("❌ Erro ao renovar token:", response.text)
        return None

# Gera access_token usando code (apenas na primeira vez)
def generate_access_token_from_code(code):    
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        token_info = response.json()
        update_refresh_token(token_info["refresh_token"])
        return token_info["access_token"]
    else:
        print("❌ Erro ao gerar token com code:", response.text)

        print("")
        print("Abra a URL abaixo no seu browser e copie o CODE, coloque no seu .env e apague o valor da variavel REFRESH_TOKEN")
        print(f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}")
        return None

# Consulta item
def get_item_data(access_token, mlb):
    url = f"https://api.mercadolibre.com/items/{mlb}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"\n🔍 Item {mlb}:")
        pprint.pprint(response.json(), compact=True)
        
        print("")
        print("##########################################################################")
        print("##########################################################################")
        print("##########################################################################")
        print("")
    else:
        print(f"\n❌ Erro {response.status_code} no item {mlb}")
        print(response.text)

# Execução principal
def main():
    print(REFRESH_TOKEN)
    if REFRESH_TOKEN and REFRESH_TOKEN != "":
        access_token = refresh_access_token(REFRESH_TOKEN)
    else:
        access_token = generate_access_token_from_code(CODE)

    if access_token:
        for mlb in mlb_list:
            get_item_data(access_token, mlb)

if __name__ == "__main__":
    main()

