import os
import time
import requests
import base64
from datetime import datetime

# Nastavení cesty k hlavnímu adresáři
hlavni_adresar = r"C:\Users\Matyáš\AppData\Roaming\Chatterino2\Logs\Twitch\Channels"

# Nastavení cesty k repozitáři na GitHubu
url_repozitar = "https://api.github.com/repos/metjum/twitchlog/contents/"

# Nastavení hlavičky pro autentizaci s GitHub API
headers = {
    "Authorization": "token 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",
}

def create_or_update_file(file_path, repo_url, headers):
    # Načtení obsahu souboru a kódování do Base64
    with open(file_path, "rb") as f:
        obsah_souboru = base64.b64encode(f.read()).decode("utf-8")

    # Vytvoření nebo aktualizace souboru na GitHubu
    nazev_souboru = os.path.relpath(file_path, hlavni_adresar).replace("\\", "/")
    url_souboru = repo_url + nazev_souboru

    # Získání aktuálního obsahu souboru z GitHubu
    existing_file_response = requests.get(url_souboru, headers=headers)

    # Příprava dat pro aktualizaci souboru na GitHubu s uvedením SHA
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "message": f"{timestamp}",
        "content": obsah_souboru,
    }

    # Pokud soubor již existuje, přidej SHA do dat pro aktualizaci
    if existing_file_response.status_code == 200:
        data["sha"] = existing_file_response.json()["sha"]

    # Odeslání požadavku na vytvoření nebo aktualizaci souboru na GitHubu
    odpoved = requests.put(url_souboru, headers=headers, json=data)

    # Zkontrolování odpovědi (nahrání souboru bylo úspěšné)
    if odpoved.status_code == 201 or odpoved.status_code == 200:
        print(f"Soubor {nazev_souboru} byl úspěšně nahrán na GitHub.")
    else:
        print(f"Chyba při nahrávání souboru {nazev_souboru}.")
        print(f"Response content: {odpoved.content}")

def process_directory(directory_path, repo_url, headers):
    for kořen, složky, soubory in os.walk(directory_path):
        for soubor in soubory:
            file_path = os.path.join(kořen, soubor)
            create_or_update_file(file_path, repo_url, headers)

# Hlavní smyčka
while True:
    try:
        process_directory(hlavni_adresar, url_repozitar, headers)
        time.sleep(360)
    except Exception as e:
        print(f"Chyba: {e}")
        time.sleep(360)
