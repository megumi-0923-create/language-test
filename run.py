import unittest
import th
import csv

suite = unittest.TestSuite()
loader = unittest.TestLoader()

#清空测试结果.csv内容
test_case_list=[th.surface_lang_detect]
with open('测试结果_th.csv', 'w') as f:
    pass

for i in test_case_list:
    suite.addTest(loader.loadTestsFromTestCase(i))
runner = unittest.TextTestRunner()
runner.run(suite)



