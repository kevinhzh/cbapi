# -*- encoding: utf-8 -*-
"""
@File    :   cbapi.py
@Time    :   2020/08/24
@Author  :   Kevin Huang
@Version :   0.1.0
"""

import datetime
import json
import pandas as pd
import requests
import threading

class Crunchbase():
    """
    An API to get organization and people data from Crunchbase.
    """

    def __init__(self, rapidapi_key):
        self.rapidapi_key = rapidapi_key
        self.headers = {"x-rapidapi-host": "crunchbase-crunchbase-v1.p.rapidapi.com", "x-rapidapi-key": rapidapi_key}

    def _get_page_data(self, data_list, page_list, url, headers, query_string):
        """
        Get page data and add it to the data_list.
        Parameters:
            data_list: list[pd.DataFrame]
                A list to store the requested page data.
            page_list: list[int]
                A list to store the requested page number.
            url: str
                Requested url.
            headers: dict
                Requested headers, including the host name and the key.
            query_string: str
                Requested query string, including the specified parameters.
        """

        temp_query_string = query_string.copy()
        for page in page_list:
            temp_query_string["page"] = page
            response = requests.request("GET", url, headers=headers, params=temp_query_string)
            if (200 == response.status_code):
                api_response = json.loads(response.text)
            else:
                raise Exception(f"Failed to request data using {temp_query_string}, Status_code: {response.status_code}")
            page_data = pd.concat([pd.DataFrame([item["properties"]]) for item in api_response["data"]["items"]])
            current_page = api_response["data"]["paging"]["current_page"]
            total_page = api_response["data"]["paging"]["number_of_pages"]
            print(f"Retrieve page {current_page}/{total_page}")
            data_list[page - 1] = page_data
            
    def get_organization(self, updated_since=None, query=None, name=None, domain_name=None, locations=None, organization_types=None, sort_order=None, page=None, max_thread_num=1):
        """
        API to get orgnization data from Crunchbase.
        Parameters:
            updated_since: int
                Optional. Filter by updated_at >= the passed value (timestamp).
            query: str
                Optional. Full text search of an organization's name, aliases and short description.
            name: str
                Optional. Full text search limited to name and aliases.
            domain_name: str
                Optional. Text search of an organization's domain_name.
            locations: str
                Optional. Filter by location names (comma separated, AND'd together).
            organization_types: str
                Available types: company, investor, school, group
                Optional. Filter by one or more types. Multiple types are separated by commas and logically AND'd.
            sort_order: str
                Available sort orders: createdat ASC, createdat DESC, updatedat ASC, updatedat DESC
                Optional. The sort order of the collection.
            page: int
                Optional. Filter by page number of the results to retrieve.
            max_thread_num: int
                Max number of working threads while using multithreading.
                Default: 1
        """

        # generate url and query string
        url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"
        query_string = {}
        if updated_since is not None:
            query_string["updated_since"] = str(updated_since)
        if query is not None:
            query_string["query"] = query
        if name is not None:
            query_string["name"] = name
        if domain_name is not None:
            query_string["domain_name"] = domain_name
        if locations is not None:
            query_string["locations"] = locations
        if organization_types is not None:
            query_string["organization_types"] = organization_types
        if sort_order is not None:
            query_string["sort_order"] = sort_order
        if page is not None:
            query_string["page"] = str(page)

        # request data
        response = requests.request("GET", url, headers=self.headers, params=query_string)
        if (200 == response.status_code):
            api_response = json.loads(response.text)
        else:
            raise Exception(f"Failed to request data using {query_string}, Status_code: {response.status_code}")
        
        # use multithrading to retrieve date from all pages if page is not specified
        if page is None:
            # get page_list for each thread
            num_of_pages = api_response["data"]["paging"]["number_of_pages"]
            l = list(range(1, num_of_pages + 1))
            if num_of_pages <= max_thread_num:
                page_lists = [[page] for page in l]
            else:
                p = num_of_pages // max_thread_num + 1
                page_lists = [l[i:i + p] if (i + p <= num_of_pages) else l[i:] for i in range(0, num_of_pages, p)]
            # use multithrading to iterate pages
            data_list = [None] * num_of_pages
            threads = [None] * len(page_lists)
            for i in range(len(page_lists)):
                threads[i] = threading.Thread(target=Crunchbase._get_page_data, args=(self, data_list, page_lists[i], url, self.headers, query_string))
                threads[i].start()
            for t in threads:
                t.join()
            data = pd.concat(data_list).reset_index(drop=True)
        # use the requested data if page is specified
        else:
            data = pd.concat([pd.DataFrame([item["properties"]]) for item in api_response["data"]["items"]]).reset_index(drop=True)

        # return data
        return data

    def get_people(self, name=None, query=None, updated_since=None, sort_order=None, page=None, locations=None, socials=None, types=None, max_thread_num=1):
        """
        API to get people data from Crunchbase.
        Parameters:
            name: str
                Optional. Full text search of name only.
            query: str
                Optional. Full text search of name, title, and company.
            updated_since: int
                Optional. Filter by updated_at >= the passed value (timestamp).
            sort_order: str
                Available sort orders: createdat ASC, createdat DESC, updatedat ASC, updatedat DESC
                Optional. The sort order of the collection.
            page: int
                Optional. Filter by page number of the results to retrieve.
            locations: str
                Optional. Filter by location names (comma separated, AND'd together).
            socials: str
                Optional. Filter by social media identity (comma separated, AND'd together)
            types: str
                Optional. Filter by type (currently, either this is empty, or is simply "investor")
            max_thread_num: int
                Max number of working threads while using multithreading.
                Default: 1
        """

        # generate url and query string
        url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-people"
        query_string = {}
        if name is not None:
            query_string["name"] = name
        if query is not None:
            query_string["query"] = query
        if updated_since is not None:
            query_string["updated_since"] = str(updated_since)
        if sort_order is not None:
            query_string["sort_order"] = sort_order
        if page is not None:
            query_string["page"] = str(page)
        if locations is not None:
            query_string["locations"] = locations
        if socials is not None:
            query_string["socials"] = socials        
        if types is not None:
            query_string["types"] = types
        
        # request data
        response = requests.request("GET", url, headers=self.headers, params=query_string)
        if (200 == response.status_code):
            api_response = json.loads(response.text)
        else:
            raise Exception(f"Failed to request data using {query_string}, Status_code: {response.status_code}")
        
        # use multithrading to retrieve date from all pages if page is not specified
        if page is None:
            # get page_list for each thread
            num_of_pages = api_response["data"]["paging"]["number_of_pages"]
            l = list(range(1, num_of_pages + 1))
            if num_of_pages <= max_thread_num:
                page_lists = [[page] for page in l]
            else:
                p = num_of_pages // max_thread_num + 1
                page_lists = [l[i:i + p] if (i + p <= num_of_pages) else l[i:] for i in range(0, num_of_pages, p)]
            # use multithrading to iterate pages
            data_list = [None] * num_of_pages
            threads = [None] * len(page_lists)
            for i in range(len(page_lists)):
                threads[i] = threading.Thread(target=Crunchbase._get_page_data, args=(self, data_list, page_lists[i], url, self.headers, query_string))
                threads[i].start()
            for t in threads:
                t.join()
            data = pd.concat(data_list).reset_index(drop=True)
        # use the requested data if page is specified
        else:
            data = pd.concat([pd.DataFrame([item["properties"]]) for item in api_response["data"]["items"]]).reset_index(drop=True)

        # return data
        return data