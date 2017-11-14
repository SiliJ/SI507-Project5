import unittest
from SI507project5_code import *


class CodeTests1(unittest.TestCase):
    def setUp(self):
         try:
             with open(CACHE_FNAME, 'r') as cache_file:
                 cache_json = cache_file.read()
                 CACHE_DICTION = json.loads(cache_json)
         except:
             CACHE_DICTION = {}
             self.CACHE_DICTION=json.loads(cache_json)
    def test_uniqueident_method(self):
        self.assertEqual(TEDx_IDENT,"https://www.eventbriteapi.com/v3/events/search/?token=<token>include_all_series_instances-True_q-TEDx")
    def test_cachetype(self):
        self.assertEqual(type(CACHE_DICTION),type({"key":"answer"}))
    def test_getfromcache_method(self):
        self.assertEqual(Check_TEDx_events,CACHE_DICTION['TEDx_IDENT'])
    def test_geteventdata_method(self):
        self.assertEqual(TEDx_events,CACHE_DICTION['TEDx_IDENT'])
    def test_cachecontent_method(self):
        self.assertEqual(len(CACHE_DICTION[TEDx_IDENT]['events']) > 30,True)
    #def tearDown(self):






if __name__ == "__main__":
    unittest.main(verbosity=2)
