"""
This is the entrypoint for the cli
"""

from enum import Enum
from pathlib import Path
import logging

import typer

from src.ultils import load_config, setup_logging
from src.preprocessing.main import main as preprocess_main
from src.semantic_search.search import main as search_main


class Stage(str, Enum):
    preprocess = "preprocess"
    search = "search"
    all = "all"

class Config(str, Enum):
    dev = "dev"
    prod = "prod"

app = typer.Typer()

def get_config_path(env: Config) -> Path:
    """Get config path and verify it exists"""
    logger = logging.getLogger(__name__)
    logger.debug(f"Getting config path for environment: {env.value}")
    
    config_path = Path("configs") / f"{env.value}-config.yaml"
    logger.debug(f"Checking if config path exists: {config_path}")
    
    if not config_path.exists():
        logger.error(f"Config path does not exist: {config_path}")
        
        if not Path("configs").exists():
            logger.critical("'configs' directory not found")
            raise typer.Exit(1)
            
        available_configs = list(Path("configs").glob("*.yaml"))
        if available_configs:
            logger.warning("Config not found, but other configs are available")
            for config in available_configs:
                logger.warning(f"Available config: {config.name}")
        
        logger.error(f"Config file not found: {config_path}")
        raise typer.Exit(1)
    
    logger.info(f"Using config file: {config_path}")
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
    ),
    query: str = typer.Option(
        None,
        help="Search query (required for search stage)"
    )
) -> None:
    """Run pipeline"""
    try:
        logger = logging.getLogger(__name__)
        logger.info(f"Starting pipeline with stage={stage.value}, env={env.value}")
        
        logger.debug("Getting config path")
        config_path = get_config_path(env)
        
        logger.debug("Loading configuration")
        config = load_config(config_path)
        
        logger.debug("Setting up logging configuration")
        logger = setup_logging(config)
        logger.info(f"Running in {env.value} environment")

        if stage in [Stage.preprocess, Stage.all]:
            logger.info("Starting preprocessing stage")
            preprocess_main(config)
            logger.info("Completed preprocessing stage")

        logger.info("Pipeline completed successfully")

        if stage in [Stage.search, Stage.all]:
            if query is None:
                logger.error("Search query is required for search stage")
                print("[red]Error: Search query is required for search stage[/red]")
                raise typer.Exit(1)
            logger.info("Starting search stage")
            search_main(config, query)

    except Exception as e:
        print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()