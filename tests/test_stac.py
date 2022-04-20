import unittest

from stactools.cclc import stac
from tests import test_data


class StacTest(unittest.TestCase):

    def test_create_item_7class_landcover(self) -> None:
        href = test_data.get_path(
            "data-files/Baywide_7class_20132014_E1300000_N1770000.tif")
        item = stac.create_item(href, "cc-lc-7-class")
        self.assertEqual(item.id, "Baywide_7class_20132014_E1300000_N1770000")
        self.assertEqual(len(item.assets), 1)
        item.validate()

    def test_create_item_13class_landcover(self) -> None:
        href = test_data.get_path(
            "data-files/Baywide_13class_20132014_E1300000_N1770000.tif")
        item = stac.create_item(href, "cc-lc-13-class")
        self.assertEqual(item.id, "Baywide_13class_20132014_E1300000_N1770000")
        self.assertEqual(len(item.assets), 1)
        item.validate()

    def test_create_item_landuse(self) -> None:
        href = test_data.get_path(
            "data-files/BayWide_1m_LU_E1300000_N1770000.tif")
        item = stac.create_item(href, "cc-lu")
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
                             "cc-lu",
                             read_href_modifier=read_href_modifier)
        assert did_it

    def test_create_collection_7class_landcover(self) -> None:
        collection = stac.create_collection("cc-lc-7-class")
        collection.set_self_href("")
        self.assertEqual(collection.id, "cc-lc-7-class")
        collection.validate()

    def test_create_collection_13class_landcover(self) -> None:
        collection = stac.create_collection("cc-lc-13-class")
        collection.set_self_href("")
        self.assertEqual(collection.id, "cc-lc-13-class")
        collection.validate()

    def test_create_collection_landuse(self) -> None:
        collection = stac.create_collection("cc-lu")
        collection.set_self_href("")
        self.assertEqual(collection.id, "cc-lu")
        collection.validate()
