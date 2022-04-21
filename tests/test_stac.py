import unittest

from stactools.chesapeake import stac
from tests import test_data


class StacTest(unittest.TestCase):

    def test_create_item_7class_landcover(self) -> None:
        href = test_data.get_path(
            "data-files/Baywide_7class_20132014_E1300000_N1770000.tif")
        item = stac.create_item(href, "chesapeake-lc-7")
        self.assertEqual(item.id, "Baywide_7class_20132014_E1300000_N1770000")
        self.assertEqual(len(item.assets), 1)
        item.validate()

    def test_create_item_13class_landcover(self) -> None:
        href = test_data.get_path(
            "data-files/Baywide_13class_20132014_E1300000_N1770000.tif")
        item = stac.create_item(href, "chesapeake-lc-13")
        self.assertEqual(item.id, "Baywide_13class_20132014_E1300000_N1770000")
        self.assertEqual(len(item.assets), 1)
        item.validate()

    def test_create_item_landuse(self) -> None:
        href = test_data.get_path(
            "data-files/BayWide_1m_LU_E1300000_N1770000.tif")
        item = stac.create_item(href, "chesapeake-lu")
        self.assertEqual(item.id, "BayWide_1m_LU_E1300000_N1770000")
        self.assertEqual(len(item.assets), 1)
        item.validate()

    def test_read_href_modifier(self) -> None:
        href = test_data.get_path(
            "data-files/BayWide_1m_LU_E1300000_N1770000.tif")
        did_it = False

        def read_href_modifier(href: str) -> str:
            nonlocal did_it
            did_it = True
            return href

        _ = stac.create_item(href,
                             "chesapeake-lu",
                             read_href_modifier=read_href_modifier)
        assert did_it

    def test_create_collection_7class_landcover(self) -> None:
        collection = stac.create_collection("chesapeake-lc-7")
        collection.set_self_href("")
        self.assertEqual(collection.id, "chesapeake-lc-7")
        collection.validate()

    def test_create_collection_13class_landcover(self) -> None:
        collection = stac.create_collection("chesapeake-lc-13")
        collection.set_self_href("")
        self.assertEqual(collection.id, "chesapeake-lc-13")
        collection.validate()

    def test_create_collection_landuse(self) -> None:
        collection = stac.create_collection("chesapeake-lu")
        collection.set_self_href("")
        self.assertEqual(collection.id, "chesapeake-lu")
        collection.validate()
