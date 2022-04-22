# stactools-chesapeake-lulc

[![PyPI](https://img.shields.io/pypi/v/stactools-chesapeake-lulc)](https://pypi.org/project/stactools-chesapeake-lulc/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stactools-packages/chesapeake-lulc/main?filepath=docs/installation_and_basic_usage.ipynb)

- Name: chesapeake-lulc
- Package: `stactools.chesapeake-lulc`
- PyPI: https://pypi.org/project/stactools-chesapeake-lulc/
- Owner: @pjhartzell
- Dataset homepage: https://www.chesapeakeconservancy.org/conservation-innovation-center/high-resolution-data/
- STAC extensions used:
  - [classification](https://github.com/stac-extensions/classification)
  - [item-assets](https://github.com/stac-extensions/item-assets)
  - [projection](https://github.com/stac-extensions/projection/)
  - [raster](https://github.com/stac-extensions/raster)

Generate STAC Items and Collections for high-resolution (1 meter) Land Use and Land Cover classification raster products for the Chesapeake Bay Watershed. The data are produced by the Chesapeake Conservancy [Conservation Innovation Center](https://www.chesapeakeconservancy.org/conservation-innovation-center/high-resolution-data/). Three STAC Collections are available:
- 7-class Land Cover: `chesapeake-lc-7`
- 13-class Land Cover: `chesapeake-lc-13`
- 17-class Land Use `chesapeake-lu`

## Examples

### STAC objects

- [Collection](examples/chesapeake-lc-7/collection.json)
- [Item](examples/chesapeake-lc-7/Baywide_7Class_20132014_E1300000_N1770000/Baywide_7Class_20132014_E1300000_N1770000.json)

### Command-line usage

To create a STAC Item:

```bash
$ stac chesapeake-lulc create-item <source-cog-file> <output-directory>
```

For example:

```bash
$ stac chesapeake-lulc create-item tests/data-files/Baywide_7class_20132014_E1300000_N1770000.tif examples
```

To create a STAC Collection, a text file containing hrefs to one or more COG files and the collection id is required:

```bash
$ stac chesapeake-lulc create-collection <file-of-cog-hrefs> <output-directory> <collection-id>
```

For example, the following command will create the contents of the `examples/chesapeake-lc-7` directory:

```bash
$ stac chesapeake-lulc create-collection examples/chesapeake-lc-7.txt examples/chesapeake-lc-7 chesapeake-lc-7
```

Use `stac chesapeake-lulc --help` to see all subcommands and options.
