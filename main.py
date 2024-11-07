import os
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from time import sleep
from InquirerPy import prompt
from InquirerPy.validator import PathValidator

console = Console()

logo = """
 ⣿⣿⣷⡁⢆⠈⠕⢕⢂⢕⢂⢕⢂⢔⢂⢕⢄⠂⣂⠂⠆⢂⢕⢂⢕⢂⢕⢂⢕⢂
 ⣿⣿⣿⡷⠊⡢⡹⣦⡑⢂⢕⢂⢕⢂⢕⢂⠕⠔⠌⠝⠛⠶⠶⢶⣦⣄⢂⢕⢂⢕
 ⣿⣿⠏⣠⣾⣦⡐⢌⢿⣷⣦⣅⡑⠕⠡⠐⢿⠿⣛⠟⠛⠛⠛⠛⠡⢷⡈⢂⢕⢂
 ⠟⣡⣾⣿⣿⣿⣿⣦⣑⠝⢿⣿⣿⣿⣿⣿⡵⢁⣤⣶⣶⣿⢿⢿⢿⡟⢻⣤⢑⢂
 ⣾⣿⣿⡿⢟⣛⣻⣿⣿⣿⣦⣬⣙⣻⣿⣿⣷⣿⣿⢟⢝⢕⢕⢕⢕⢽⣿⣿⣷⣔
 ⣿⣿⠵⠚⠉⢀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⢕⢕⢕⢕⢕⢕⣽⣿⣿⣿⣿
 ⢷⣂⣠⣴⣾⡿⡿⡻⡻⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣿⣿⣿⣿⣿⡿
 ⢌⠻⣿⡿⡫⡪⡪⡪⡪⡪⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋
 ⠣⡁⠹⡪⡪⡪⡪⣮⣿⣿⣿⣿⣿⡿⠐⢉⢍⢋⢝⠻⣿⣿⣿⣿⣿⣿⣿⣿⠏⠈
 ⡣⡘⢄⠙⢾⣼⣾⣿⣿⣿⣿⣿⣿⡀⢐⢕⢕⢕⢕⢕⣘⣿⣿⣿⣿⣿⣿⡿⠚⠈
 ⠌⢊⢂⢣⠹⣿⣿⣿⣿⣿⣿⣿⣿⣧⢐⢕⢕⢕⢕⢕⢅⢁⢉⢍⢋⠁⢐⢕⢂⠈
 ⠄⠁⠕⠝⡢⠈⠻⣿⣿⣿⣿⣿⣿⣿⣇⢐⢕⢕⢕⢕⢕⢕⢕⣕⣿⣿⣿⡿⠚⠙
 ⠨⡂⢀⢑⢕⡅⠂⠄⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠂⠄⠉⠉⢕⢂⢕⠈
 ⠄⠪⣂⠁⢕⠆⠄⠂⠄⠁⠂⢂⠉⠉⠍⢛⢛⢛⢛⢛⢕⢕⢕⢕⣽⣾⣿⠈
"""

def main():
    os.system("cls" if os.name == "nt" else "clear")

    text_block = (
        f"[#ff5555]{logo}\n\n[bold #ff5555]Created by an unknown digital unit Delagorg"
    )

    panel_content = Panel(
        text_block,
        border_style="#ff5555",
        title="[bold #ff5555]Lol, Fuck you",
        title_align="center",
        padding=(1, 2),
    )

    console.print(panel_content, justify="center")

    try:
        with Progress(
            TextColumn("[bold #ff5555]{task.description}"),
            BarColumn(bar_width=console.size.width - 40),
            TimeRemainingColumn(),
            console=console,
            expand=True,
        ) as progress:
            task = progress.add_task("[bold #ff5555]Loading environment...", total=100)
            while not progress.finished:
                progress.update(task, advance=1)
                sleep(0.03)

        os.system("cls" if os.name == "nt" else "clear")

        scripts_folder = "scripts"

        scripts = [f for f in os.listdir(scripts_folder) if f.endswith(".py")]

        if not scripts:
            console.print("[bold red]No Python scripts found in 'scripts' folder.[/]")
            return

        choices = [{"name": script, "value": script} for script in scripts]
        questions = [
            {
                "type": "list",
                "name": "script",
                "message": "Select a script to run",
                "choices": choices,
            }
        ]

        answer = prompt(questions)
        script_to_run = answer.get("script")

        if script_to_run:
            script_path = os.path.join(scripts_folder, script_to_run)
            os.system(f'python "{script_path}"')
    except KeyboardInterrupt:
        console.print("\n[bold red]Process interrupted by user.[/]")

if __name__ == "__main__":
    main()
