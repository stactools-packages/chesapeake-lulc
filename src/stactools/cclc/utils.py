import os.path
from typing import List, Optional

import rasterio
from stactools.core.utils.subprocess import call


class Tile:

    def __init__(self,
                 left: float,
                 bottom: float,
                 right: float,
                 top: float,
                 nodata: Optional[int] = None):
        self._left = left
        self._bottom = bottom
        self._right = right
        self._top = top
        self._nodata = nodata

    def subset(self, infile, outdir) -> None:
        base = os.path.splitext(os.path.basename(infile))[0]
        outfile = os.path.join(
            outdir,
            (f"{base}_E{str(int(self._left))}_N{str(int(self._bottom))}.tif"))
        args = [
            "gdal_translate", "-of", "COG", "-a_nodata", "0", "-co",
            "compress=deflate", "-co", "blocksize=512", "-projwin",
            str(self._left),
            str(self._top),
            str(self._right),
            str(self._bottom)
        ]
        if self._nodata is not None:
            args.extend(["-a_nodata", str(self._nodata)])
        args.append(infile)
        args.append(outfile)
        call(args)


def tile(infile: str,
         outdir: str,
         size: int,
         left_bottom: tuple[(int, int)],
         nodata: Optional[int] = None) -> None:
    """Tiles the given input to a grid."""
    with rasterio.open(infile) as dataset:
        _, _, right, top = dataset.bounds
        left, bottom = left_bottom
        tiles = create_tiles(left, bottom, right, top, size, nodata)
    for tile in tiles:
        tile.subset(infile, outdir)


def create_tiles(left: float,
                 bottom: float,
                 right: float,
                 top: float,
                 size: int,
                 nodata: Optional[int] = None) -> List[Tile]:
    x = left
    y = bottom
    tiles = []
    while x < right:
        while y < top:
            tile = Tile(x, y, min(x + size, right), min(y + size, top), nodata)
            tiles.append(tile)
            y += size
        x += size
        y = bottom
    return tiles
