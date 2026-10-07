import base64
import requests
import json

# --- 1. JOUW INSTELLINGEN ---
GEMINI_API_KEY = "AQ.Ab8RN6KmtluRoXeUFpm4i3ew-CP5k3uHPCBgmrT7KGrWKahipw"  # Je API key
GITHUB_TOKEN = "VUL_HIER_JE_GITHUB_TOKEN_IN"                               # Zorg dat je PAT (token) hier is ingevuld
GITHUB_USERNAME = "NeilB1977"
GITHUB_REPO = "Jobhunt-Dashboard"
FILE_PATH = "index.html"
# ----------------------------

def get_latest_dashboard_code():
    print("🤖 Gemini AI wordt aangeroepen om de code op te halen (via gemini-3.5-flash)...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    prompt = """
    Genereer de VOLLEDIGE, geüpdatete HTML code voor het Jobhunt Dashboard van Neil Broes.
    Gebruik Tailwind CSS via CDN.
    Begin met <!DOCTYPE html> en eindig met </html>.
    Belangrijk: Geef ENKEL de ruwe code terug, GEEN markdown opmaak zoals ```html en GEEN extra tekst. Zorg ervoor dat de Elevator Pitch met de microfoon emoji correct in de code staat.
    """

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        html_code = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        if html_code.startswith("```html"):
            html_code = html_code[7:]
        if html_code.startswith("```"):
            html_code = html_code[3:]
        if html_code.endswith("```"):
            html_code = html_code[:-3]

        return html_code.strip()
    except Exception as e:
        print(f"❌ Fout bij ophalen van code via Gemini API: {e}")
        return None

def update_github_file(content):
    if not content:
        print("❌ Geen inhoud ontvangen om te uploaden.")
        return

    print("🚀 Bezig met uploaden naar GitHub...")
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            sha = res.json()["sha"]
        else:
            print(f"❌ Fout bij ophalen bestand van GitHub: {res.status_code} - {res.text}")
            return

        # Let op: De .encode("utf-8") is cruciaal voor het verwerken van emoji's zoals de microfoon.
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        payload = {
            "message": "Automatische dashboard update via GitHub Actions & Gemini API",
            "content": encoded_content,
            "sha": sha,
            "branch": "main"
        }

        put_res = requests.put(url, headers=headers, json=payload, timeout=20)
        if put_res.status_code in (200, 201):
            print("✅ Succes! Je dashboard is geüpdatet en live op GitHub Pages.")
        else:
            print(f"❌ Fout bij updaten op GitHub: {put_res.status_code} - {put_res.text}")
    except Exception as e:
        print(f"❌ Fout bij communicatie met GitHub: {e}")

if __name__ == "__main__":
    code = get_latest_dashboard_code()
    if code:
        update_github_file(code)
