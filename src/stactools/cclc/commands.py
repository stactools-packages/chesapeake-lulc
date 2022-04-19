import logging

import click

from stactools.cclc.constants import DEFAULT_LOWER_LEFT, DEFAULT_TILE_SIZE
from stactools.cclc.utils import tile

logger = logging.getLogger(__name__)


def create_cclc_command(cli):
    """Creates the stactools-cclc command line utility."""

    @cli.group(
        "cclc",
        short_help=("Commands for working with stactools-cclc"),
    )
    def cclc():
        pass

    @cclc.command("tile", help="Tiles the input COG to a grid")
    @click.argument("infile")
    @click.argument("outdir")
    @click.option("-s",
                  "--size",
                  default=DEFAULT_TILE_SIZE,
                  help="Tile size in meters")
    @click.option("-l",
                  "--lower-left",
                  default=DEFAULT_LOWER_LEFT,
                  type=(int, int),
                  help="Lower left origin of tiles")
    def tile_command(infile: str, outdir: str, size: int,
                     lower_left: tuple((int, int))):
        """Tiles the input file to a grid.
        The source CCLC data are huge GeoTIFFS, so we tile the geotiffs.
        """
        tile(infile, outdir, size, lower_left)

    return cclc
