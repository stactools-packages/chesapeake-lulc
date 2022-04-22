from datetime import datetime, timezone
from typing import Optional

from pystac import Collection, Item
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterExtension
from stactools.core.io import ReadHrefModifier

from stactools.chesapeake_lulc import constants
from stactools.chesapeake_lulc.fragments import StacFragments
from stactools.chesapeake_lulc.metadata import Metadata


def create_item(href: str,
                read_href_modifier: Optional[ReadHrefModifier] = None) -> Item:
    """Create a collection-specific STAC Item for a COG tile of the Chesapeake
    Conservancy land cover or land use data.

    Args:
        href (str): HREF to a COG containing classification data.
        read_href_modifier (Callable[[str], str]): An optional function to
            modify the href (e.g. to add a token to a url).
    Returns:
        Item: STAC Item object representing the tile of classification data.
    """
    metadata = Metadata(href, read_href_modifier)

    item = Item(id=metadata.item_id,
                geometry=metadata.geometry,
                bbox=metadata.bbox,
                datetime=None,
                properties={
                    "start_datetime": constants.START_TIME,
                    "end_datetime": constants.END_TIME
                })
    item.common_metadata.created = datetime.now(tz=timezone.utc)

    asset = StacFragments(metadata.collection_id).get_asset(href)
    item.add_asset("data", asset)

    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.apply(**metadata.proj_properties)

    RasterExtension.add_to(item)

    item.stac_extensions.append(constants.CLASSIFICATION_SCHEMA)

    return item


def create_collection(collection_id: str) -> Collection:
    """Creates a STAC Collection for Chesapeake Conservancy land cover or land
    use data.

    Args:
        collection_id (str): ID of the STAC Collection. Must be one of
        "chesapeake-lc-13", "chesapeake-lc-7", or "chesapeake-lu"
    Returns:
        Collection: The created STAC Collection.
    """
    fragment = StacFragments(collection_id).get_collection()

    collection = Collection(id=collection_id,
                            title=fragment["title"],
                            description=fragment["description"],
                            license=fragment["license"],
                            keywords=fragment["keywords"],
                            providers=fragment["providers"],
                            extent=fragment["extent"])
    collection.add_links(fragment["links"])

    item_assets = {}
    asset_dict = StacFragments(collection_id).get_asset("").to_dict()
    asset_dict.pop("href")
    item_assets["data"] = AssetDefinition(asset_dict)

    item_assets_ext = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets_ext.item_assets = item_assets

    ItemAssetsExtension.add_to(collection)
    RasterExtension.add_to(collection)
    collection.stac_extensions.append(constants.CLASSIFICATION_SCHEMA)

    return collection
