import os
import sys
from google import genai

def main():
    # Controleer of de API Key aanwezig is
    if 'GEMINI_API_KEY' not in os.environ:
        print("Fout: GEMINI_API_KEY omgevingsvariabele ontbreekt!")
        sys.exit(1)

    # Initialiseer de client
    client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

    # Lees je live data in
    if not os.path.exists('data.txt'):
        print("Fout: data.txt niet gevonden in de repository!")
        sys.exit(1)

    with open('data.txt', 'r', encoding='utf-8') as f:
        live_data = f.read()

    # De instructie voor Gemini 3.8 Flash
    prompt = f"""
    Analyseer de volgende data:
    {live_data}
    
    Maak op basis hiervan een prachtig, modern en responsive HTML-dashboard (index.html).
    Eisen:
    1. Gebruik Tailwind CSS via CDN voor een strak, modern design (donkere modus stijl, mooie kaarten, duidelijke statistieken).
    2. Gebruik Chart.js via CDN om de belangrijkste datapunten visueel te maken in interactieve grafieken (bijv. een lijn- of staafdiagram).
    3. Voeg een sectie toe met 'Laatste update: ' met de huidige datum/tijd en een korte tekstuele samenvatting over de trends.
    4. Lever ALLEEN de pure HTML-code op. Begin NIET met ```html en eindig NIET met ```. Geen tekst eromheen, direct starten met <!DOCTYPE html>.
    """

    print("Dashboard aan het genereren via Gemini 3.8 Flash...")
    
    try:
        # We gebruiken de stabiele generate_content call
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
        )
        
        raw_text = response.text.strip()
        
        # Veilige opschoning van eventuele markdown code-blocks
        if raw_text.startswith("```html"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
            
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        clean_html = raw_text.strip()

        # Sla het dashboard op
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(clean_html)
        
        print("Dashboard succesvol gegenereerd en opgeslagen als index.html!")

    except Exception as e:
        print(f"Er is een fout opgetreden tijdens de API aanroep: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
