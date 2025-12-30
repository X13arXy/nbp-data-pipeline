import requests
import json
import os
print(f"TUTAJ JESTEM: {os.getcwd()}")
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
        
    def save_to_json(self,data,filename): 
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

# --- CZĘŚĆ WYKONAWCZA (To co się dzieje "na hali") ---
if __name__ == "__main__":
    # 1. Tworzenie obiektu
    connector = NBPConnector()
    
    # 2. Pobieranie danych
    rates = connector.get_rates()
    
    if rates:
        print("Pobrano dane, zapisuję...")
        
        # 3. WYWOŁANIE TWOJEJ NOWEJ FUNKCJI (Tego brakowało!)
        # Przekazujemy: dane (rates) i nazwę pliku ("kursy.json")
        connector.save_to_json(rates, "kursy.json")
        
    else:
        print("Błąd: Nie udało się pobrać danych")