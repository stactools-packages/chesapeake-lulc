from enum import Enum

DEFAULT_TILE_SIZE = 10000  # meters
DEFAULT_LEFT_BOTTOM = (1300000.0, 1650000.0)  # (x, y); meters; ESRI:102039

START_TIME = "2013-01-01T00:00:00Z"
END_TIME = "2014-12-31T23:59:59Z"

CLASSIFICATION_SCHEMA = "https://stac-extensions.github.io/classification/v1.0.0/schema.json"

class Collections(Enum):
    LC_13 = "cc-lc-13-class"
    LC_7 = "cc-lc-7-class"
    LU = "cc-lu"
