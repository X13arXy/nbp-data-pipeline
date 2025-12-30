import requests
import json

# Definicja KLASY (Schemat urządzenia)
class NBPConnector:
    
    # 1. Konstruktor (__init__): Tu ustawiamy "parametry startowe"
    def __init__(self):
        # To jest zmienna, którą widzi cała klasa (self.url)
        self.base_url = "http://api.nbp.pl/api/exchangerates/tables/A?format=json"

    # 2. Metoda (Funkcja wewnątrz klasy): To jest "przycisk", który wykonuje akcję
    def get_rates(self):
        try:
            response = requests.get(self.base_url)
            
            if response.status_code == 200:
                data = response.json()
                return data[0]['rates'] # Zwracamy tylko listę walut
            else:
                print(f"Błąd API: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Błąd połączenia: {e}")
            return None

# --- CZĘŚĆ WYKONAWCZA (To co się dzieje "na hali") ---

if __name__ == "__main__":
    # 1. Tworzymy obiekt (Instancję). Wyjmujemy urządzenie z pudełka.
    connector = NBPConnector()
    
    # 2. Używamy metody tego obiektu.
    print("Łączenie z NBP...")
    data = connector.get_rates()
    
    # 3. Przetwarzamy wynik (jeśli coś przyszło)
    if data:
        print("Pobrano kursy walut:")
        # Wyświetlamy np. USD (zazwyczaj jest pierwszy lub drugi, szukamy pętlą dla pewności)
        for currency in data:
            if currency['code'] in ['USD', 'EUR']:
                print(f"{currency['code']}: {currency['mid']} PLN")
    else:
        print("Nie udało się pobrać danych.")
        