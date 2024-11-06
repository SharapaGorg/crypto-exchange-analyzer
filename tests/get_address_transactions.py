import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Консоль для вывода
console = Console()

# Получение курса биткоина к доллару через CoinGecko API
def get_btc_to_usd_rate():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    data = response.json()
    return data['bitcoin']['usd']

# Получаем актуальный курс
btc_to_usd_rate = get_btc_to_usd_rate()

# Информационная таблица
info_table = Table.grid(expand=True)
info_table.add_column(justify="left", style="cyan", no_wrap=True)
info_table.add_row(f"[bold]BTC to USD Rate:[/] {btc_to_usd_rate} USD")
info_table.add_row("[bold]Satoshi:[/] The smallest unit of Bitcoin. 1 BTC = 100,000,000 Satoshi")

# Вывод информационной таблицы
console.print(Panel(info_table, title="Exchange Rate Information", subtitle="Bitcoin Exchange Rate and Units"))

# Адрес для получения транзакций
address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# URL API BlockCypher для отображения информации по адресу
url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}"

# Выполнение запроса к API
response = requests.get(url)
data = response.json()

# Получаем транзакции адреса
transactions = data.get('txrefs', [])

# Создание основной таблицы
transaction_table = Table(title="Transactions for Address")

# Добавляем колонки к таблице
transaction_table.add_column("Transaction Hash", justify="center", style="cyan", no_wrap=True)
transaction_table.add_column("Value (Satoshi)", justify="right", style="green")
transaction_table.add_column("Value (BTC)", justify="right", style="yellow")
transaction_table.add_column("Value (USD)", justify="right", style="magenta")

# Обработка каждой транзакции
for tx in transactions:
    tx_hash = tx['tx_hash']
    value_satoshi = tx['value']
    value_btc = value_satoshi / 100_000_000
    value_usd = value_btc * btc_to_usd_rate

    transaction_table.add_row(tx_hash, str(value_satoshi), f"{value_btc:.8f}", f"${value_usd:.2f}")

# Вывод основной таблицы
console.print(transaction_table)
