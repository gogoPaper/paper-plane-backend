#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

class PaperTestBase(unittest.TestCase):

    def setUp(self):
        print "test1 setup"

    def tearDown(self):
        print "test1 tearDown"



if __name__ == '__main__':
    unittest.main()