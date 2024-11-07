import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Консоль для вывода
console = Console()

address = "bc1qz2r83ac3gy8x6ls7jtkdnv0qdnjkwa4ux4p5f4"

def get_btc_to_usd_rate():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    data = response.json()
    return data['bitcoin']['usd']

btc_to_usd_rate = get_btc_to_usd_rate()

info_table = Table.grid(expand=True)
info_table.add_column(justify="left", style="cyan", no_wrap=True)
info_table.add_row(f"[bold]BTC to USD Rate:[/] {btc_to_usd_rate} USD")
info_table.add_row("[bold]Satoshi:[/] The smallest unit of Bitcoin. 1 BTC = 100,000,000 Satoshi")

console.print(Panel(info_table, title="Exchange Rate Information", subtitle="Bitcoin Exchange Rate and Units"))

# API URL
url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}"
response = requests.get(url)
data = response.json()
transactions = data.get('txrefs', [])

# Создание объединенной таблицы для отображения всех транзакций
transaction_table = Table(title="Transactions for Address", show_lines=True)

cols = [
    ("Type", "bold magenta"),
    ("Transaction Hash", "cyan"),
    ("Date & Time", "white"),
    ("Value (Satoshi)", "green"),
    ("Value (BTC)", "yellow"),
    ("Value (USD)", "magenta")
]

for col_name, col_style in cols:
    transaction_table.add_column(col_name, justify="center", style=col_style)

# Обработка транзакций
for tx in transactions:
    tx_hash = tx.get('tx_hash', 'Unknown')
    tx_time_str = tx.get('confirmed', None)
    if tx_time_str:
        try:
            tx_time = datetime.fromisoformat(tx_time_str.replace('Z', '+00:00'))
        except ValueError:
            tx_time = "Unknown Format"
    else:
        tx_time = "Unconfirmed"

    value_satoshi = tx['value']
    value_btc = value_satoshi / 100_000_000
    value_usd = value_btc * btc_to_usd_rate

    if tx['tx_output_n'] >= 0:
        # Входящая транзакция
        transaction_type = "[green bold]Incoming[/green bold]"
    else:
        # Исходящая транзакция
        transaction_type = "[red bold]Outgoing[/red bold]"

    transaction_table.add_row(
        transaction_type,
        tx_hash, 
        tx_time.strftime("%Y-%m-%d %H:%M:%S") if isinstance(tx_time, datetime) else tx_time, 
        str(value_satoshi), 
        f"{value_btc:.8f}", 
        f"${value_usd:.2f}"
    )

console.print(transaction_table)
