from ast import Add
from datetime import datetime, timezone
from typing import Optional
import json

from pystac import (Asset, CatalogType, Collection, Extent, Item, MediaType,
                    Provider, ProviderRole, SpatialExtent, TemporalExtent)
from pystac.extensions.projection import ProjectionExtension
from stactools.core.io import ReadHrefModifier

from stactools.cclc.fragments import StacFragments
from stactools.cclc.metadata import Metadata
from stactools.cclc import constants


def create_item(collection: str, href: str, read_href_modifier: Optional[ReadHrefModifier] = None) -> Item:
    """
    """
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

    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.apply(**metadata.proj_properties)

    asset = StacFragments(collection).get_asset(href)
    item.add_asset("data", asset)

    item.stac_extensions.append(constants.CLASSIFICATION_SCHEMA)

    print(json.dumps(item.to_dict(), indent=2))
    return item
