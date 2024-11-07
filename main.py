import os
import signal
import subprocess
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from time import sleep, time
import sys
from InquirerPy import prompt

console = Console()

logo = """
 ⣿⣿⣷⡁⢆⠈⠕⢕⢂⢕⢂⢕⢂⢔⢂⢕⢄⠂⣂⠂⠆⢂⢕⢂⢕⢂⢕⢂⢕⢂
 ⣿⣿⣿⡷⠊⡢⡹⣦⡑⢂⢕⢂⢕⢂⢕⢂⠕⠔⠌⠝⠛⠶⠶⢶⣦⣄⢂⢕⢂⢕
 ⣿⣿⠏⣠⣾⣦⡐⢌⢿⣷⣦⣅⡑⠕⠡⠐⢿⠿⣛⠟⠛⠛⠛⠛⠡⢷⡈⢂⢕⢂
 ⠟⣡⣾⣿⣿⣿⣿⣦⣑⠝⢿⣿⣿⣿⣿⣿⡵⢁⣤⣶⣶⣿⢿⢿⢿⡟⢻⣤⢑⢂
 ⣾⣿⣿⡿⢟⣛⣻⣿⣿⣿⣦⣬⣙⣻⣿⣿⣷⣿⣿⢟⢝⢕⢕⢕⢕⢽⣿⣿⣷⣔
 ⣿⣿⠵⠚⠉⢀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⢕⢕⢕⢕⢕⢕⣽⣿⣿⣿⣿
 ⢷⣂⣠⣴⣾⡿⡿⡻⡻⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣿⣿⣿⣿⣿⡿
 ⢌⠻⣿⡿⡫⡪⡪⡪⡪⡪⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋
 ⠣⡁⠹⡪⡪⡪⡪⣮⣿⣿⣿⣿⣿⡿⠐⢉⢍⢋⢝⠻⣿⣿⣿⣿⣿⣿⣿⣿⠏⠈
 ⡣⡘⢄⠙⢾⣼⣾⣿⣿⣿⣿⣿⣿⡀⢐⢕⢕⢕⢕⢕⣘⣿⣿⣿⣿⣿⣿⡿⠚⠈
 ⠌⢊⢂⢣⠹⣿⣿⣿⣿⣿⣿⣿⣿⣧⢐⢕⢕⢕⢕⢕⢅⢁⢉⢍⢋⠁⢐⢕⢂⠈
 ⠄⠁⠕⠝⡢⠈⠻⣿⣿⣿⣿⣿⣿⣿⣇⢐⢕⢕⢕⢕⢕⢕⢕⣕⣿⣿⣿⡿⠚⠙
 ⠨⡂⢀⢑⢕⡅⠂⠄⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠂⠄⠉⠉⢕⢂⢕⠈
 ⠄⠪⣂⠁⢕⠆⠄⠂⠄⠁⠂⢂⠉⠉⠍⢛⢛⢛⢛⢛⢕⢕⢕⢕⣽⣾⣿⠈
"""

def signal_handler(signum, frame):
    console.print("\n[bold red]Script execution interrupted by user.[/]")
    sys.exit(0)

def run_script(script_path):
    start_time = time()
    try:
        process = subprocess.Popen([sys.executable, script_path], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        process.communicate()
    except KeyboardInterrupt:
        console.print("\n[bold red]Script execution interrupted by user.[/]")
        process.terminate()
        process.wait()

    end_time = time()
    elapsed_time = end_time - start_time
    console.print(f"\n[bold green]Script execution completed in {elapsed_time:.2f} seconds.[/]")
    process_stats(process)

def process_stats(process):
    # Здесь можно добавить больше логики для сбора и отображения статистики процесса.
    console.print(f"\n[bold blue]Process ID:[/] {process.pid}")
    console.print(f"[bold blue]Return Code:[/] {process.returncode}")
    if os.name != 'nt':
        import resource
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        console.print(f"[bold blue]User CPU time:[/] {usage.ru_utime:.2f} seconds")
        console.print(f"[bold blue]System CPU time:[/] {usage.ru_stime:.2f} seconds")

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

            # Setting up signal handler
            signal.signal(signal.SIGINT, signal_handler)

            run_script(script_path)
    except KeyboardInterrupt:
        console.print("\n[bold red]Process interrupted by user.[/]")

if __name__ == "__main__":
    main()
