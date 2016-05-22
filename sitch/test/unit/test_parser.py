import imp
import os
modulename = 'sitchutils'
modulepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
file, pathname, description = imp.find_module(modulename, [modulepath])
fixturepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "../fixture/cell_towers.csv.gz")
sitchutils = imp.load_module(modulename, file, pathname, description)


class TestOpenCellIdDataset:
    def test_list_mcc(self):
        parser = sitchutils.OpenCellIdDataset(fixturepath)
        mcc_list = parser.get_mcc_list()
        assert len(mcc_list) > 100

    def test_get_all_for_mcc(self):
        band = 'GSM'
        mcc = '310'
        parser = sitchutils.OpenCellIdDataset(fixturepath)
        all_for_mcc = parser.get_all_for_mcc(band, mcc)
        assert len(all_for_mcc) > 100
