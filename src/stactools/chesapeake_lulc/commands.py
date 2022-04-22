import os
from typing import Optional

import click
from click import Choice
from pystac import CatalogType

from stactools.chesapeake_lulc import stac
from stactools.chesapeake_lulc.constants import (DEFAULT_LEFT_BOTTOM,
                                                 DEFAULT_TILE_SIZE,
                                                 CollectionId)
from stactools.chesapeake_lulc.utils import remove_nodata, tile


def create_chesapeake_lulc_command(cli):
    """Creates the stactools-chesapeake-lulc command line utility."""

    @cli.group(
        "chesapeake-lulc",
        short_help=("Commands for working with stactools-chesapeake-lulc"),
    )
    def chesapeake_lulc():
        pass

    @chesapeake_lulc.command("tile", help="Tiles the input file to a grid")
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

        The source chesapeake-lulc data are large GeoTIFFS, so we tile them to COGs.

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

    @chesapeake_lulc.command(
        "remove-nodata-tifs",
        help="Removes TIF files that contain only nodata values")
    @click.argument("INDIR")
    @click.option("-n",
                  "--nodata_dir",
                  help="directory to place nodata TIF files")
    def remove_nodata_tifs_command(indir: str,
                                   nodata_dir: Optional[str] = None) -> None:
        """Moves TIF files that contain only nodata values to a new directory.

        Useful after tiling a large area where many tiles do not intersect valid
        data. The default location for the new directory is a subdirectory
        named "nodata_tifs". Use the --nodata_dir option to override this
        default location and name.

        Args:
            indir (str): Directory of TIF files to be examined.
            nodata_dir (Optional[str]): Optional directory for the nodata TIF
                files.
        """
        if nodata_dir is None:
            nodata_dir = os.path.join(indir, "nodata_tifs")
        remove_nodata(indir, nodata_dir)

    @chesapeake_lulc.command(
        "create-item",
        short_help=("Create a STAC Item from a Chesapeake Land Use or Land "
                    "Cover COG file"))
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    def create_item_command(infile: str, outdir: str) -> None:
        """Creates a STAC Item for a tile of Chesapeake Conservancey land cover
        or land use classification data.

        \b
        Args:
            infile (str): HREF of the classification map COG.
            outdir (str): Directory that will contain the STAC Item.
        """
        item = stac.create_item(infile)
        item_path = os.path.join(outdir, f"{item.id}.json")
        item.set_self_href(item_path)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object()

    @chesapeake_lulc.command(
        "create-collection",
        short_help=("Creates a STAC collection of Chesapeake Conservancy land "
                    "cover or land use classification tiles"),
    )
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    @click.argument("COLLECTION_ID",
                    type=Choice([id.value for id in CollectionId]))
    def create_collection_command(infile: str, outdir: str,
                                  collection_id: str) -> None:
        """Creates a STAC Collection for Items defined by the hrefs in INFILE."

        \b
        Args:
            infile (str): Text file containing one href per line. The hrefs
                should point to Chesapeake Conservancy land cover or land use
                COG files.
            outdir (str): Directory that will contain the collection.
            collection_id (str): Collection ID. Must be one of
                "chesapeake-lc-7", "chesapeake-lc-13", or "chesapeake-lu".
        """
        with open(infile) as file:
            hrefs = [line.strip() for line in file.readlines()]

        collection = stac.create_collection(collection_id)
        collection.set_self_href(os.path.join(outdir, "collection.json"))
        collection.catalog_type = CatalogType.SELF_CONTAINED
        for href in hrefs:
            item = stac.create_item(href)
            collection.add_item(item)
        collection.make_all_asset_hrefs_relative()
        collection.validate_all()
        collection.save()

    return chesapeake_lulc
