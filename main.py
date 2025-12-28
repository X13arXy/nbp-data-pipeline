import requests
import json

def fetch_data():
    url = "http://api.nbp.pl/api/exchangerates/tables/A?format=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("Pobrano dane z NBP:")
        print(f"Data tabeli: {data[0]['effectiveDate']}")
        rates = data[0]['rates']
        for rate in rates[:3]:
            print(f"{rate['code']}: {rate['mid']}")
    else:
        print("Błąd pobierania danych")

if __name__ == "__main__":
    fetch_data()