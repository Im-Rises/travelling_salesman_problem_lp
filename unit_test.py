import unittest

import numpy as np
import pandas as pd

import linear_prog_res as lpr
import routings_res as rs


class MyTestCase(unittest.TestCase):
    def test_result(self):
        filename = "data.xlsx"
        sheet = "sheet1"
        cities = pd.read_excel(filename, sheet).columns.values
        cities = np.array(cities)
        cities = np.delete(cities, 0, axis=0)
        for city in cities:
            if city not in ["Perth Stadium", "Marrara Oval"]:  # To many calculations so not testing those two
                self.assertEqual(int(lpr.main(city, filename, sheet)), int(rs.main(city, filename, sheet)))
                # The two models normally returns floats, the precision can sometimes vary a little. To be
                # sure the output is the same they are casted into int


if __name__ == '__main__':
    unittest.main()
