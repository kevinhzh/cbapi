# -*- encoding: utf-8 -*-
"""
@File    :   test.py
@Time    :   2020/08/26
@Author  :   Kevin Huang
@Version :   1.0
"""

import cbapi
import pandas as pd
import unittest
RAPIDAPI_KEY = "INPUT YOUR RAPIDAPI_KEY HERE"


class TestCrunchbase(unittest.TestCase):

    def test_organization_single_thread(self):
        """
        Test that it can get organization data using a single thread.
        """
        session = cbapi.Crunchbase(rapidapi_key=RAPIDAPI_KEY)
        organization_data = session.get_organization(locations="California,San Francisco", organization_types="investor", page=2)
        self.assertIsInstance(organization_data, pd.DataFrame)
    
    def test_organization_multithreading(self):
        """
        Test that it can get organization data using multithreading thread.
        """
        session = cbapi.Crunchbase(rapidapi_key=RAPIDAPI_KEY)
        organization_data = session.get_organization(locations="California,San Francisco", organization_types="investor", max_thread_num=5)
        self.assertIsInstance(organization_data, pd.DataFrame)

    def test_people_single_thread(self):
        """
        Test that it can get people data using a single thread.
        """
        session = cbapi.Crunchbase(rapidapi_key=RAPIDAPI_KEY)
        people_data = session.get_people(name="Kevin", types="investor", page=2)
        self.assertIsInstance(people_data, pd.DataFrame)

    def test_people_multithreading(self):
        """
        Test that it can get people data using multithreading.
        """
        session = cbapi.Crunchbase(rapidapi_key=RAPIDAPI_KEY)
        people_data = session.get_people(name="Kevin", types="investor", max_thread_num=5)
        self.assertIsInstance(people_data, pd.DataFrame)
    
    def test_invalid_key(self):
        """
        Test that it will raise Exception while using an invalid key.
        """
        session = cbapi.Crunchbase(rapidapi_key="INVALID_KEY")
        with self.assertRaises(Exception):
            people_data = session.get_people(name="Kevin", types="investor", max_thread_num=5)


if __name__ == "__main__":
    unittest.main()
