import os
from google import genai

def main():
    # Initialiseer de client met de API-sleutel
    client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

    # Lees je live data in
    if not os.path.exists('data.txt'):
        print("Fout: data.txt niet gevonden in de repository!")
        return

    with open('data.txt', 'r', encoding='utf-8') as f:
        live_data = f.read()

    # De instructie voor Gemini (We gebruiken nu gemini-3.8-flash)
    prompt = f"""
    Je bent een expert in data-dashboards. Analyseer de volgende data:
    {live_data}
    
    Maak op basis hiervan een prachtig, modern en responsive HTML-dashboard (index.html).
    Eisen:
    1. Gebruik Tailwind CSS via CDN voor een strak, modern design (donkere modus stijl, mooie kaarten, duidelijke statistieken).
    2. Gebruik Chart.js via CDN om de belangrijkste datapunten visueel te maken in interactieve grafieken (bijv. een lijn- of staafdiagram).
    3. Voeg een sectie toe met 'Laatste update: ' met de huidige datum/tijd en een korte tekstuele samenvatting over de trends.
    4. Lever ALLEEN de pure HTML-code op. Begin NIET met ```html en eindig NIET met ```. Geen tekst eromheen, direct starten met <!DOCTYPE html>.
    """

    print("Dashboard aan het genereren via Gemini 3.8 Flash...")
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
    )

    # Schoon de output op (voor het geval Gemini toch markdown-tags toevoegt)
    clean_html = response.text.strip()
    if clean_html.startswith("```html"):
        clean_html = clean_html.split("```html")[1]
    if clean_html.endswith("```"):
        clean_html = clean_html.rsplit("```", 1)[0]
    clean_html = clean_html.strip()

    # Sla het dashboard op
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(clean_html)
    
    print("Dashboard succesvol gegenereerd en opgeslagen als index.html!")

if __name__ == "__main__":
    main()
