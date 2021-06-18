from typing import Any, Dict
import logging
import click
from pathlib import Path
from .model import notion

FORMAT = "%(asctime)-15s (%(module)s) [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT)

logger = logging.getLogger("N2O")


@click.group()
@click.option("-v", "--verbose", count=True, help="Set how chatty ox is.")
@click.option(
    "-L",
    "--log-level",
    type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]),
    default="WARNING",
    help="Set logging level.",
)
@click.pass_context
def knox(ctx: click.Context, verbose: int, log_level: str):
    ctx.ensure_object(dict)
    logger.setLevel(log_level)


@knox.command(name="import")
@click.argument("source", type=click.Path(exists=True))
@click.argument("target", required=False, type=click.Path())
@click.option(
    "-s",
    "--src-format",
    type=click.Choice(["NOTION"]),
    default="NOTION",
    help="Tell ox the format of the data in SOURCE.",
)
@click.pass_context
def import_cmd(ctx: click.Context, source: str, target: str, src_format: str):
    """
    Import the SOURCE into TARGET suitable for Obsidian.

    When TARGET is omitted a Zip file is created, the name will be random.
    """
    logger.info("Processing %s", source)
    datasource = notion.Notion(Path(source))
