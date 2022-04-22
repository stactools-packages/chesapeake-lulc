from enum import Enum


class CollectionId(Enum):
    LC7 = "chesapeake-lc-7"
    LC13 = "chesapeake-lc-13"
    LU = "chesapeake-lu"


DEFAULT_TILE_SIZE = 10000  # meters
DEFAULT_LEFT_BOTTOM = (1300000.0, 1650000.0)  # (x, y); meters; ESRI:102039

START_TIME = "2013-01-01T00:00:00Z"
END_TIME = "2014-12-31T23:59:59Z"

CLASSIFICATION_SCHEMA = "https://stac-extensions.github.io/classification/v1.0.0/schema.json"
