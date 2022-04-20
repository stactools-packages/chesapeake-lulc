import os.path
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from stactools.testing import CliTestCase

from stactools.cclc.commands import create_cclc_command
from tests import test_data


class ItemCommandTest(CliTestCase):

    def create_subcommand_functions(self) -> List[Callable[[Group], Command]]:
        return [create_cclc_command]

    def test_create_item_7class_landcover(self) -> None:
        infile = test_data.get_path(
            "data-files/Baywide_7class_20132014_E1300000_N1770000.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"cclc create-item {infile} {tmp_dir} -c cc-lc-7-class"
            self.run_command(cmd)
            item_path = os.path.join(
                tmp_dir, "Baywide_7Class_20132014_E1300000_N1770000.json")
            item = pystac.read_file(item_path)
        item.validate()

    def test_create_item_13class_landcover(self) -> None:
        infile = test_data.get_path(
            "data-files/Baywide_13class_20132014_E1300000_N1770000.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"cclc create-item {infile} {tmp_dir} -c cc-lc-13-class"
            self.run_command(cmd)
            item_path = os.path.join(
                tmp_dir, "Baywide_13Class_20132014_E1300000_N1770000.json")
            item = pystac.read_file(item_path)
        item.validate()

    def test_create_item_landuse(self) -> None:
        infile = test_data.get_path(
            "data-files/Baywide_1m_LU_E1300000_N1770000.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"cclc create-item {infile} {tmp_dir} -c cc-lu"
            self.run_command(cmd)
            item_path = os.path.join(tmp_dir,
                                     "Baywide_1m_LU_E1300000_N1770000.json")
            item = pystac.read_file(item_path)
        item.validate()
