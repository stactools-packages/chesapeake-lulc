import json
from typing import Any, Collection

import pkg_resources
from pystac import Asset, MediaType
from pystac.utils import make_absolute_href


class StacFragments:
    """Class for accessing asset data."""

    def __init__(self, collection: str) -> None:
        self.collection = collection

    def get_asset(self, href: str) -> Asset:
        asset = self._load("asset.json")
        asset["type"] = MediaType.COG
        asset["href"] = make_absolute_href(href)
        return Asset.from_dict(asset)

    def get_collection(self) -> Collection:
        collection = self._load("collection.json")

    def _load(self, file_name: str) -> Any:
        try:
            with pkg_resources.resource_stream(
                    "stactools.cclc.fragments",
                    f"fragments/{self.collection}/{file_name}") as stream:
                return json.load(stream)
        except FileNotFoundError as e:
            raise e
