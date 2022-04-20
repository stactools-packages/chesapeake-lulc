import json
from typing import Any, Dict

import pkg_resources
from pystac import Asset, Extent, Link, MediaType, Provider
from pystac.utils import make_absolute_href


class StacFragments:
    """Class for accessing asset data."""

    def __init__(self, collection_id: str) -> None:
        self.collection_id = collection_id

    def get_asset(self, href: str) -> Asset:
        asset = self._load("asset.json")
        asset["type"] = MediaType.COG
        asset["href"] = make_absolute_href(href)
        return Asset.from_dict(asset)

    def get_collection(self) -> Dict[str, Any]:
        data = self._load("collection.json")
        data["extent"] = Extent.from_dict(data["extent"])
        data["providers"] = [
            Provider.from_dict(provider) for provider in data["providers"]
        ]
        data["links"] = [Link.from_dict(link) for link in data["links"]]
        return data

    def _load(self, file_name: str) -> Any:
        try:
            with pkg_resources.resource_stream(
                    "stactools.cclc.fragments",
                    f"fragments/{self.collection_id}/{file_name}") as stream:
                return json.load(stream)
        except FileNotFoundError as e:
            raise e
