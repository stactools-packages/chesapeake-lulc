import os
from typing import Optional

import click
from click import Choice
from pystac import CatalogType

from stactools.cclc import stac
from stactools.cclc.constants import (COLLECTION_IDS, DEFAULT_LEFT_BOTTOM,
                                      DEFAULT_TILE_SIZE)
from stactools.cclc.utils import tile


def create_cclc_command(cli):
    """Creates the stactools-cclc command line utility."""

    @cli.group(
        "cclc",
        short_help=("Commands for working with stactools-cclc"),
    )
    def cclc():
        pass

    @cclc.command("tile", help="Tiles the input COG to a grid")
    @click.argument("INFILE")
    @click.argument("OUTDIR")
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

    @cclc.command(
        "create-item",
        short_help=("Create a STAC Item from CCLC Land Cover COG file."))
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    @click.option("-c",
                  "--collection-id",
                  type=Choice(COLLECTION_IDS),
                  required=True)
    def create_item_command(infile: str, outdir: str,
                            collection_id: str) -> None:
        """Creates a STAC Item for a tile of Chesapeake Conservancey land cover
        or land use classification data.

        \b
        Args:
            infile (str): HREF of the classification map COG.
            outdir (str): Directory that will contain the STAC Item.
            collection_id (str): Collection ID. Must be one of "cc-lc-13-class",
                "cc-lc-7-class", or "cc-lu"
        """
        item = stac.create_item(infile, collection_id)
        item_path = os.path.join(outdir, f"{item.id}.json")
        item.set_self_href(item_path)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object()

    @cclc.command(
        "create-collection",
        short_help=("Creates a STAC collection of Chesapeake Conservancy land "
                    "cover or land use classification tiles."),
    )
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    @click.option("-c",
                  "--collection-id",
                  type=Choice(COLLECTION_IDS),
                  required=True)
    def create_collection_command(infile: str, outdir: str,
                                  collection_id: str) -> None:
        """Creates a STAC Collection for Items defined by the hrefs in INFILE."

        \b
        Args:
            infile (str): Text file containing one href per line. The hrefs
                should point to Chesapeake Conservancy land cover or land use
                COG files.
            outdir (str): Directory that will contain the collection.
            collection (str): Collection ID. Must be one of "cc-lc-13-class",
                "cc-lc-7-class", or "cc-lu"
        """
        with open(infile) as file:
            hrefs = [line.strip() for line in file.readlines()]

        collection = stac.create_collection(collection_id)
        collection.set_self_href(os.path.join(outdir, "collection.json"))
        collection.catalog_type = CatalogType.SELF_CONTAINED
        for href in hrefs:
            item = stac.create_item(href, collection_id)
            collection.add_item(item)
        collection.make_all_asset_hrefs_relative()
        collection.validate_all()
        collection.save()

    return cclc
