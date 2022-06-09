import io
import sys
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
            if city != "Perth Stadium" and city != "Marrara Oval":
                self.assertEqual(lpr.main(city, filename, sheet), rs.main(city, filename, sheet))
                print("Monscript fait")


if __name__ == '__main__':
    unittest.main()
