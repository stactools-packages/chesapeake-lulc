import os.path

import rasterio
from stactools.core.utils.subprocess import call


def tile(infile: str, outdir: str, size: int,
         lower_left: tuple[(int, int)]) -> None:
    """Tiles the given input to a grid."""
    with rasterio.open(infile) as dataset:
        _, _, right, top = dataset.bounds
        left, bottom = lower_left
        tiles = create_tiles(left, bottom, right, top, size)
    for tile in tiles:
        tile.subset(infile, outdir)


def create_tiles(left, bottom, right, top, size):
    x = left
    y = bottom
    tiles = []
    while x < right:
        while y < top:
            tile = Tile(x, y, min(x + size, right), min(y + size, top))
            tiles.append(tile)
            y += size
        x += size
        y = bottom
    return tiles


class Tile:

    def __init__(self, left, bottom, right, top):
        self._left = left
        self._bottom = bottom
        self._right = right
        self._top = top

    def subset(self, infile, outdir):
        base = os.path.splitext(os.path.basename(infile))[0]
        outfile = os.path.join(
            outdir,
            (f"{base}_{str(int(self._left))}_{str(int(self._bottom))}.tif"))
        args = [
            "gdal_translate", "-of", "COG", "-co", "compress=deflate", "-co",
            "blocksize=512", "-projwin",
            str(self._left),
            str(self._top),
            str(self._right),
            str(self._bottom)
        ]
        args.append(infile)
        args.append(outfile)
        return call(args)
