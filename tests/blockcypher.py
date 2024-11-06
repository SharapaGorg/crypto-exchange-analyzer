import requests

# API URL для получения информации о последних транзакциях
API_URL = "https://api.blockcypher.com/v1/btc/main/txs"

# Запрос для получения последних транзакций
response = requests.get(API_URL)
transactions = response.json()

# Парсинг и вывод адресов кошельков участников транзакций
for tx in transactions:
    inputs = tx.get('inputs', [])
    outputs = tx.get('outputs', [])

    input_addresses = [inp.get('addresses', []) for inp in inputs]
    output_addresses = [out.get('addresses', []) for out in outputs]

    print(f"Transaction Hash: {tx['hash']}")
    print("Input Addresses:", input_addresses)
    print("Output Addresses:", output_addresses)
    print("\n")
