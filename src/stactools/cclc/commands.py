import logging
from typing import Optional

import click

from stactools.cclc.constants import DEFAULT_LEFT_BOTTOM, DEFAULT_TILE_SIZE
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
                  "--left-bottom",
                  default=DEFAULT_LEFT_BOTTOM,
                  type=(int, int),
                  help="left, bottom coordinate origin of tiles")
    @click.option("-n", "--nodata", type=int, help="nodata value")
    def tile_command(infile: str,
                     outdir: str,
                     size: int,
                     left_bottom: tuple((int, int)),
                     nodata: Optional[int] = None) -> None:
        """Tiles the input file to a grid.

        The source CCLC data are large GeoTIFFS, so we tile them to COGs.

        \b
        Args:
            infile (str): HREF to source GeoTIFF to be tiled
            outdir (str): Directory that will contain the tiles
            size (int): Tile size in meters
            left_bottom (tuple(int, int)): X, Y coordinates of tile grid origin.
                Defined as the lower left corner of the area to be tiled.
            nodata (int): nodata value to use for tiled COGs

        """
        tile(infile, outdir, size, left_bottom, nodata)

    return cclc
