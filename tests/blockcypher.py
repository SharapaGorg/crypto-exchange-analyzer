import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import time

console = Console()

def get_btc_to_usd_rate():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    data = response.json()
    return data["bitcoin"]["usd"]

btc_to_usd_rate = get_btc_to_usd_rate()

info_table = Table.grid(expand=True)
info_table.add_column(justify="left", style="cyan", no_wrap=True)
info_table.add_row(f"[bold]BTC to USD Rate:[/] {btc_to_usd_rate} USD")
info_table.add_row(
    "[bold]Satoshi:[/] The smallest unit of Bitcoin. 1 BTC = 100,000,000 Satoshi"
)

console.print(
    Panel(
        info_table,
        title="Exchange Rate Information",
        subtitle="Bitcoin Exchange Rate and Units",
    )
)

api_base_url = "https://api.blockcypher.com/v1/btc/main"

def get_block_data():
    while True:
        try:
            response = requests.get(api_base_url)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                console.print(f"Too many requests: {response.status_code}. Waiting for 30 seconds...")
                with Progress(
                    SpinnerColumn(),
                    BarColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    transient=True,
                ) as progress:
                    task = progress.add_task("[yellow]Waiting...", total=30)
                    for _ in range(30):
                        time.sleep(1)
                        progress.advance(task)
            else:
                console.print(f"Failed to retrieve data: {response.status_code}")
                exit(1)
        except KeyboardInterrupt:
            console.print("\\n[bold green]Program terminated. All processes have been interrupted.[/bold green]")
            exit(0)

data = get_block_data()
latest_block_hash = data.get("hash")
if not latest_block_hash:
    console.print("Failed to retrieve the latest block hash.")
    exit(1)

def get_block_response():
    while True:
        try:
            block_url = f"{api_base_url}/blocks/{latest_block_hash}"
            block_response = requests.get(block_url)
            if block_response.status_code == 200:
                return block_response.json()
            elif block_response.status_code == 429:
                console.print(f"Too many requests: {block_response.status_code}. Waiting for 30 seconds...")
                with Progress(
                    SpinnerColumn(),
                    BarColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    transient=True,
                ) as progress:
                    task = progress.add_task("[yellow]Waiting...", total=30)
                    for _ in range(30):
                        time.sleep(1)
                        progress.advance(task)
            else:
                console.print(f"Failed to retrieve block data: {block_response.status_code}")
                exit(1)
        except KeyboardInterrupt:
            console.print("\\n[bold green]Program terminated. All processes have been interrupted.[/bold green]")
            exit(0)

block_data = get_block_response()
transactions = block_data.get("txids", [])

if not transactions:
    console.print("No transactions found in the latest block.")
    exit(1)

transaction_table = Table(
    title=f"Bitcoin Transactions Above $10,000", show_lines=True
)

cols = [
    ("Transaction Hash", "cyan"),
    ("Date & Time", "white"),
    ("Input Addresses", "green"),
    ("Output Addresses", "yellow"),
    ("Value (BTC)", "cyan"),
    ("Value (USD)", "magenta"),
    ("Balance (BTC)", "red")
]

for col_name, col_style in cols:
    transaction_table.add_column(col_name, justify="center", style=col_style)

addresses_added = 0
processed_hashes = set()

try:
    while addresses_added < 10:
        for tx_hash in transactions:
            if addresses_added >= 10:
                break

            if tx_hash in processed_hashes:
                continue

            tx_url = f"{api_base_url}/txs/{tx_hash}"
            tx_response = requests.get(tx_url)

            if tx_response.status_code != 200:
                if tx_response.status_code == 429:
                    console.print(f"Too many requests: {tx_response.status_code}. Waiting for 30 seconds...")
                    with Progress(
                            SpinnerColumn(),
                            BarColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            transient=True,
                    ) as delay_progress:
                        delay_task = delay_progress.add_task("[yellow]Waiting...", total=30)
                        for _ in range(30):
                            time.sleep(1)
                            delay_progress.advance(delay_task)
                    continue
                else:
                    console.print(
                        f"Failed to retrieve transaction data for {tx_hash}: {tx_response.status_code}"
                    )
                    continue

            tx_data = tx_response.json()
            tx_time_str = tx_data.get("confirmed", None)
            if tx_time_str:
                try:
                    tx_time = datetime.fromisoformat(tx_time_str.replace("Z", "+00:00"))
                except ValueError:
                    tx_time = "Unknown Format"
            else:
                tx_time = "Unconfirmed"

            is_coinbase = tx_data.get("inputs", [{}])[0].get("coinbase", False)

            input_addresses = []
            if is_coinbase:
                input_addresses_str = "Coinbase Transaction"
                balance_btc = 0
            else:
                for input in tx_data.get("inputs", []):
                    addresses = input.get("addresses", [])
                    if addresses:
                        for addr in addresses:
                            input_addresses.append(addr)
                input_addresses_str = "\\n".join(input_addresses) if input_addresses else "N/A"

                balance_btc = sum(input.get("output_value", 0) for input in tx_data.get("inputs", [])) / 100_000_000

            output_addresses = []
            total_value_satoshi = 0
            for output in tx_data.get("outputs", []):
                addresses = output.get("addresses", [])
                if addresses:
                    for addr in addresses:
                        output_addresses.append(addr)
                total_value_satoshi += output.get("value", 0)
            output_addresses_str = "\\n".join(output_addresses) if output_addresses else "N/A"
            value_btc = total_value_satoshi / 100_000_000
            value_usd = value_btc * btc_to_usd_rate

            if value_usd > 10_000:
                transaction_table.add_row(
                    tx_hash,
                    (
                        tx_time.strftime("%Y-%m-%d %H:%M:%S")
                        if isinstance(tx_time, datetime)
                        else tx_time
                    ),
                    input_addresses_str,
                    output_addresses_str,
                    f"{value_btc:.8f}",
                    f"${value_usd:.2f}",
                    f"{balance_btc:.8f}"
                )
                console.clear()
                console.print(transaction_table)
                addresses_added += 1
                processed_hashes.add(tx_hash)
                time.sleep(1)

except KeyboardInterrupt:
    console.print("\\n[bold green]Program terminated. All processes have been interrupted.[/bold green]")
