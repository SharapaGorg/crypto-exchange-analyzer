import requests
from rich.console import Console
from rich import box
from rich.panel import Panel
from rich.table import Table

# Консоль для вывода
console = Console()

# Функция для получения актуального курса биткоина
def get_btc_to_usd_rate():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    data = response.json()
    return data['bitcoin']['usd']

# Получаем актуальный курс
btc_to_usd_rate = get_btc_to_usd_rate()

# Адрес биткоин-кошелька для проверки баланса
address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# URL API BlockCypher для получения информации об адресе
url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"

# Выполнение запроса к API для получения баланса кошелька
response = requests.get(url)
data = response.json()

# Получение общего баланса и баланса непотраченных выходов
total_balance = data.get('balance', 0)  # баланс в сатоши
unspent_balance = data.get('final_balance', 0)  # непотраченный баланс тоже в сатоши

# Конвертация баланса в биткоины и доллары
total_balance_btc = total_balance / 100_000_000
unspent_balance_btc = unspent_balance / 100_000_000
total_balance_usd = total_balance_btc * btc_to_usd_rate
unspent_balance_usd = unspent_balance_btc * btc_to_usd_rate

# Отображение баланса
balance_table = Table(title="Bitcoin Wallet Balance", box=box.SIMPLE)
balance_table.add_column("Description", justify="left")
balance_table.add_column("BTC Value", justify="right")
balance_table.add_column("USD Value", justify="right")

balance_table.add_row("Total Balance", f"{total_balance_btc:.8f} BTC", f"${total_balance_usd:.2f} USD")
balance_table.add_row("Unspent Balance", f"{unspent_balance_btc:.8f} BTC", f"${unspent_balance_usd:.2f} USD")

# Вывод таблицы баланса
console.print(Panel(balance_table, title="Wallet Balance Information"))
