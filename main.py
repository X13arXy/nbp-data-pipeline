import requests
import sqlite3  # <--- Nowa biblioteka (wbudowana w Pythona, nic nie instaluj)

# --- KLASA 1: Łącznik z Internetem (To już znasz) ---
class NBPConnector:
    def __init__(self):
        self.base_url = "http://api.nbp.pl/api/exchangerates/tables/A?format=json"

    def get_rates(self):
        try:
            response = requests.get(self.base_url)
            if response.status_code == 200:
                return response.json()[0]['rates']
            return None
        except Exception as e:
            print(f"Błąd połączenia: {e}")
            return None

# --- KLASA 2: Magazynier Bazy Danych (NOWOŚĆ) ---
class CurrencyDB:
    def __init__(self, db_name="kursy_walut.db"):
        # 1. Nawiązanie połączenia z plikiem bazy
        # Jeśli plik nie istnieje, Python sam go stworzy.
        self.conn = sqlite3.connect(db_name)
        
        # 2. Stworzenie "Cursora"
        # Cursor to taki "robotnik z długopisem", który wykonuje polecenia w bazie.
        self.cursor = self.conn.cursor()
        
        # 3. Automatyczne tworzenie tabeli przy starcie
        self.create_table()

    def create_table(self):
        # SQL: CREATE TABLE - tworzy tabelę (jak arkusz w Excelu)
        # IF NOT EXISTS - robi to tylko, jeśli tabeli jeszcze nie ma
        query = """
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_code TEXT,
            rate REAL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(query) # Robotnik wykonuje polecenie
        self.conn.commit()         # Zapisz zmiany na trwałe (Ctrl+S)

    def insert_rate(self, code, rate):
        # SQL: INSERT INTO - wstaw nowy wiersz
        # Używamy znaków zapytania (?), żeby bezpiecznie wstawić zmienne
        query = "INSERT INTO rates (currency_code, rate) VALUES (?, ?)"
        
        try:
            self.cursor.execute(query, (code, rate))
            self.conn.commit() # Ważne! Bez commit dane nie zostaną zapisane.
            print(f"--> Zapisano w bazie: {code} po kursie {rate}")
        except Exception as e:
            print(f"Błąd zapisu SQL: {e}")

    def close(self):
        # Zamykamy połączenie, żeby nie blokować pliku
        self.conn.close()

# --- GŁÓWNY PROGRAM ---
if __name__ == "__main__":
    # 1. Tworzymy obiekty (zatrudniamy pracowników)
    nbp = NBPConnector()    # Pracownik od Internetu
    db = CurrencyDB()       # Pracownik od Magazynu

    print("Pobieram dane z NBP...")
    data = nbp.get_rates()

    if data:
        print(f"Pobrano {len(data)} walut. Wrzucam do bazy...")
        
        # Pętla po wszystkich walutach
        for currency in data:
            # currency to słownik np. {'currency': 'dolar amerykański', 'code': 'USD', 'mid': 3.98}
            kod = currency['code']
            kurs = currency['mid']
            
            # Zlecenie zapisu do bazy
            db.insert_rate(kod, kurs)
            
        print("Gotowe! Dane są w pliku kursy_walut.db")
    
    # Sprzątanie po pracy
    db.close()