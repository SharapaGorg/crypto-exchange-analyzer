import requests
from rich.table import Table
from rich.console import Console

# API URL to get information about the latest transactions
API_URL = "https://api.blockcypher.com/v1/btc/main/txs"

# Request to get the latest transactions
response = requests.get(API_URL)
transactions = response.json()

# Create a console object for rich output
console = Console()

# Create a table object
table = Table(title="Bitcoin Transactions", show_lines=True)

# Add columns to the table
table.add_column("Transaction Hash", style="cyan", no_wrap=True)
table.add_column("Input Addresses", style="magenta")
table.add_column("Input Count", style="magenta")
table.add_column("Output Addresses", style="green")
table.add_column("Output Count", style="green")

# Parse and output wallet addresses of transaction participants
for tx in transactions:
    inputs = tx.get('inputs', [])
    outputs = tx.get('outputs', [])

    input_addresses = [", ".join(inp.get('addresses', [])) for inp in inputs] if inputs else ["N/A"]
    output_addresses = [", ".join(out.get('addresses', [])) for out in outputs] if outputs else ["N/A"]

    input_count = sum(len(inp.get('addresses', [])) for inp in inputs)
    output_count = sum(len(out.get('addresses', [])) for out in outputs)

    table.add_row(
        tx['hash'], 
        "\n".join(input_addresses),
        str(input_count),
        "\n".join(output_addresses), 
        str(output_count)
    )

# Display the table
console.print(table)
