# init_db.py
import requests
import sqlite3
import os

url = "https://v6.exchangerate-api.com/v6/a6b6b66db857e66ab5dd506b/latest/USD"
DATABASE = 'database.db'

def delete_database():
    """Elimina el archivo de la base de datos si existe."""
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"La base de datos '{DATABASE}' ha sido eliminada.")
    else:
        print(f"La base de datos '{DATABASE}' no existe o ya fue eliminada.")



def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Crear la tabla para los tipos de cambio
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversion_rates (
            currency TEXT PRIMARY KEY,
            rate REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()


def fetch_conversion_rates():
    response = requests.get(url)
    data = response.json()
    return data['conversion_rates']  # Esto devuelve el diccionario de tipos de cambio

def store_conversion_rates(rates):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Inserta o reemplaza los tipos de cambio
    for currency, rate in rates.items():
        cursor.execute('''
            INSERT OR REPLACE INTO conversion_rates (currency, rate) VALUES (?, ?)
        ''', (currency, rate))
    
    conn.commit()
    conn.close()


if __name__ == '__main__':
    initialize_database()
    rates = fetch_conversion_rates()
    store_conversion_rates(rates)