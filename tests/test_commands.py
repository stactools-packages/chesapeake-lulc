import os.path
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from stactools.testing import CliTestCase

from stactools.chesapeake_lulc.commands import create_chesapeake_lulc_command
from tests import test_data


class ItemCommandTest(CliTestCase):

    def create_subcommand_functions(self) -> List[Callable[[Group], Command]]:
        return [create_chesapeake_lulc_command]

    def test_create_item_7class_landcover(self) -> None:
        infile = test_data.get_path(
            "data-files/Baywide_7class_20132014_E1300000_N1770000.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"chesapeake-lulc create-item {infile} {tmp_dir}"
            self.run_command(cmd)
            item_path = os.path.join(
                tmp_dir, "Baywide_7class_20132014_E1300000_N1770000.json")
            item = pystac.read_file(item_path)
        item.validate()

    def test_create_item_13class_landcover(self) -> None:
        infile = test_data.get_path(
            "data-files/Baywide_13Class_20132014_E1300000_N1770000.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"chesapeake-lulc create-item {infile} {tmp_dir}"
            self.run_command(cmd)
            item_path = os.path.join(
                tmp_dir, "Baywide_13Class_20132014_E1300000_N1770000.json")
            item = pystac.read_file(item_path)
        item.validate()

    def test_create_item_landuse(self) -> None:
        infile = test_data.get_path(
            "data-files/BayWide_1m_LU_E1300000_N1770000.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"chesapeake-lulc create-item {infile} {tmp_dir}"
            self.run_command(cmd)
            item_path = os.path.join(tmp_dir,
                                     "BayWide_1m_LU_E1300000_N1770000.json")
            item = pystac.read_file(item_path)
        item.validate()
