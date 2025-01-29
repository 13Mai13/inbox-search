"""
This is the entrypoint for the cli
"""

from enum import Enum
from pathlib import Path

import typer
from rich import print

from src.ultils import load_config, setup_logging
from src.preprocessing.main import main as preprocess_main


class Stage(str, Enum):
    preprocess = "preprocess"
    all = "all"

class Config(str, Enum):
    dev = "dev"
    prod = "prod"

app = typer.Typer()

def get_config_path(env: Config) -> Path:
    """Get config path and verify it exists"""
    config_path = Path("configs") / f"{env.value}-config.yaml"
    if not config_path.exists():
        if not Path("configs").exists():
            print("[red]Error: 'configs' directory not found. Please create it with the required config files.[/red]")
            raise typer.Exit(1)
            
        available_configs = list(Path("configs").glob("*.yaml"))
        if available_configs:
            print("[yellow]Available config files:[/yellow]")
            for config in available_configs:
                print(f"  - {config.name}")
        print(f"[red]Error: Config file not found: {config_path}[/red]")
        raise typer.Exit(1)
    return config_path

@app.command()
def main(
    stage: Stage = typer.Option(
        Stage.all,
        help="Pipeline stage to run"
    ),
    env: Config = typer.Option(
        Config.dev,
        help="Environment to use (dev or prod)"
    )
) -> None:
    """Run pipeline"""
    try:
        config_path = get_config_path(env)
        config = load_config(config_path)
        logger = setup_logging(config)
        logger.info(f"Running in {env.value} environment")

        if stage in [Stage.preprocess, Stage.all]:
            logger.info("Starting preprocessing stage")
            preprocess_main(config)

    except Exception as e:
        print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()