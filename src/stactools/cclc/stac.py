from datetime import datetime, timezone
from typing import Optional

from pystac import Item
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterExtension
from stactools.core.io import ReadHrefModifier

from stactools.cclc import constants
from stactools.cclc.fragments import StacFragments
from stactools.cclc.metadata import Metadata


def create_item(href: str,
                collection: str,
                read_href_modifier: Optional[ReadHrefModifier] = None) -> Item:
    """Create a collection-specific STAC Item for a COG tile of the Chesapeake
    Conservancy land cover or land use data.

    Args:
        href (str): HREF to a COG containing classification data.
        collection (str): The id of the collection to which the Item belongs.
        read_href_modifier (Callable[[str], str]): An optional function to
            modify the href (e.g. to add a token to a url).
    Returns:
        Item: STAC Item object representing the tile of classification data.
    """
    if collection not in constants.COLLECTIONS:
        raise ValueError(
            f"The collection must be one of: {', '.join(constants.COLLECTIONS)}."
        )

    metadata = Metadata(href, read_href_modifier)

    item = Item(id=metadata.id,
                geometry=metadata.geometry,
                bbox=metadata.bbox,
                datetime=None,
                properties={
                    "start_datetime": constants.START_TIME,
                    "end_datetime": constants.END_TIME
                })
    item.common_metadata.created = datetime.now(tz=timezone.utc)

    asset = StacFragments(collection).get_asset(href)
    item.add_asset("data", asset)

    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.apply(**metadata.proj_properties)

    RasterExtension.add_to(item)

    item.stac_extensions.append(constants.CLASSIFICATION_SCHEMA)

    return item
