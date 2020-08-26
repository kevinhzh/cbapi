# -*- encoding: utf-8 -*-
"""
@File    :   runtest.py
@Time    :   2020/08/24
@Author  :   Kevin Huang
@Version :   1.0
"""

import cbapi
import datetime
import timeit
RAPIDAPI_KEY = "INPUT YOUR RAPIDAPI_KEY HERE"

def time_stuff(func):
    """
    Measure time of execution of a function
    """
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        end = timeit.default_timer()
        print(f"Running time: {end - start} seconds")
    return wrapper

@time_stuff
def test_organization_single_thread():
    print("Test get_organization using single thread")
    session = cbapi.Crunchbase(rapidapi_key=RAPIDAPI_KEY)
    organization_data = session.get_organization(locations="California,San Francisco", organization_types="investor")
    print(organization_data.shape)

@time_stuff
def test_organization_multithreading():
    print("Test get_organization using multithreading")
    session = cbapi.Crunchbase(rapidapi_key=RAPIDAPI_KEY)
    organization_data = session.get_organization(locations="California,San Francisco", organization_types="investor", max_thread_num=5)
    print(organization_data.shape)

@time_stuff
def test_people_single_thread():
    print("Test get_people using single thread")
    session = cbapi.Crunchbase(rapidapi_key=RAPIDAPI_KEY)
    people_data = session.get_people(name="Kevin", types="investor")
    print(people_data.shape)

@time_stuff
def test_people_multithreading():
    print("Test get_people using multithreading")
    session = cbapi.Crunchbase(rapidapi_key=RAPIDAPI_KEY)
    people_data = session.get_people(name="Kevin", types="investor", max_thread_num=5)
    print(people_data.shape)


if __name__ == "__main__":
    test_organization_single_thread()
    test_organization_multithreading()
    test_people_single_thread()
    test_people_multithreading()