# cbapi
A full-featured API library to allow downloading and presenting organization and people data from Crunchbase using [Rapidapi](https://rapidapi.com).

## Quick Start
### Create the session
The ```Crunchbase``` class allows you to create a session with your own Rapidapi key to access data from Crunchbase.
```python
import cbapi
session = cbapi.Crunchbase(rapidapi_key="INPUT YOUR RAPIDAPI_KEY HERE")
```
### Fetch organization data
The ```get_organization``` member function allows you to get organization data with multithreading. The parameters you can use to filter the data include update_since, query, name, domain_name, locations, organization_types, sort_order and page.  
Example:
```python
organization_data = session.get_organization(locations="California,San Francisco", organization_types="investor", max_thread_num=5)
```
### Fetch people data
The ```get_people``` member function allows you to get people data with multithreading. The parameters you can use to filter the data include name, query, update_since, sort_order, page, locations, socials and types.  
Example:
```python
people_data = session.get_people(name="Kevin", types="investor", max_thread_num=5)
```
### Test
The ```RAPIDAPI_KEY``` should be changed to your own Rapidapi key at the top of the codes before you run the test.py.

## Installation
Install cbapi using pip:
```python
pip install git+https://github.com/kevinhzh/cbapi.git
```

## Requirements
* pandas>=0.25.0
* requests>=2.22.0
