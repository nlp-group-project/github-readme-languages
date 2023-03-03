"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests
from bs4 import BeautifulSoup
import re

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token: https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = ['shoes/shoes4', 'druv5319/Sneaks-API', 'shoes/shoes3', 'WebAR-rocks/WebAR.rocks.hand', 'brandontruggles/Selenium-Shoe-Bot-NakedCPH', 'dilip-dawadi/shoeStore', 'developer-junaid/Nike-Shoe-Store', 'alisonmonteiro/shoe-size-converter', 'LucaArgentieri/Shoe-Discord-Bot', 'antonjlin/adidas-account-generator', 'Fyko/stockx-gif', 'iissh/TrendStop', 'Hetessy/Shoes-Store-App-UI-Flutter', 'Rhelli/Shoes-Github-API', 'kenmoini/multiverse-of-multicluster-madness', 'aravind2060/Capstone0', 'daxidngyn/stockx-data', 'adityar224/sneakerx', 'fumixia/supreme-api-ts', 'JDsnyke/UP-Flow', 'JordanAssayah/shoe-order', 'amouliom/sneakers', 'harryleevn93/shoes-shop', 'mprabs/Shoe-UI-mockUp', 'MaximKuklin/3D_CenterNet', 'Ohohko/shoes', 'tyrue/3th_Engineering-design2', 'udl/shoesql', 'Nickwang3/GearGuide', 'DanielMafra/desafio-1-papodedev', 'Jolonte/challenge-codelandia-jordan-shoes', 'Spitfire5720/is-the-shoe-for-you-.github.io', 'lucianojunnior17/nike-site', 'KeyulJain/RishitBlogs', 'guilhermepaitax/myboot', 'RobsonVinicius/product-card-hover-animation', 'ZuckyNeeraj/powergeneratingshoes', 'allenlogan/HypeDCWebScraper', 'JulienMousset/Animated-3D-Card', 'SilasRodrigues19/iShoes', 'JohnPetros/rocketshoes', 'trevorblades/ssx', 'Hassanalk12/csa-web-project', 'wekt0r/Calendar', 'JDsnyke/GuptaK', 'monicatvera/e-commerce', 'bisofts/hey-look', 'douglasscaini/rocketshoes', 'dudunog/eshoes-website', 'iMuhammadessa/triplemshoes', 'joshuaanaya/AnayaKicks', 'webmural/moshpit', 'StarAmbients/my-shoes-lifetime-app', 'cgr2134/nikefy', 'AnaisGueyte/JS-ShouldIBuyTheBag', 'febritecno/kalkulator-ruby-desktop', 'WBPBP/preshoes-shoes', 't8rn8r/shoe-hanger', 'BusinessBoomingKickz/Kickz4Dayz', 'jiarongj/Python', 'Selfxplanatoryy/Nike-ca-Unidays-Script', 'bhumill/Shoppy', '716r15/shopoes', 'nardonykolyszyn/simple-editor', 'bhandeystruck/NikeShoesFrontEnd', 'kristiyann/af1-spider', 'asalinasf/nike-card', 'TasnimJahan/assignment2-responsive', 'DxxxxY/eros', 'ecomteck/productdesignapp', 'vsoch/shoes', 'RobsonVinicius/product-card-shoe', 'chrisalxlng/sneakr.', 'JueK3y/Project-TypeError', 'aaronago/kinderfoos', 'millennialdev/Nike-Shoes-eCommerce', 'eLopez6/Semblance', 'rsfrankl/shoe_census_2020', 'asalinasf/nike-page', 'seawolf/rails_cookie_decryptor', 'shoestagram/front-end', 'Equilapi/MEVN---Dashboard-Shoes-Inventary', 'yagoag/shoe-shop', 'UmairShah90/Nike-Shoes', '2002Bishwajeet/shop_app', 'Aaroncye/TEAM-EVO-SPORTS-EMPORIUM', 'robcapell/maxnixon-practice-shoe_mockup', 'AnthonyMichaelc/python-genders', 'Perke1/DumplingKicks', 'sebastianalamina/MyP_2020-1_Proyecto3', 'tcdat96/ShoeFinder', 'thiccsupreme/Shoe-Size-Converter', 'jaydeep-shelake/CardAnimation', 'Kvas1407/ecomm-store-project', 'bisofts/kingshoes', 'yug20/react-gltf-models-shoes', 'Kenzothd/Shoedog_Client', 'baby-boomer/CFC-Sports']

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )

    
def get_repo_links(github_token=github_token, github_username=github_username,
                                         topic='covid-19', number_of_pages=10):
    '''
    Takes in a topic, your unique github API token, and your github username as
    strings and an integer for the number of pages to query
    Returns: list of repositories from GitHub in the form of
    '<username>/<repo_name>'
    '''
    # set URL without page number
    url = f'https://github.com/topics/{topic}?&s=stars&page='
    # set header for github auth
    headers = {"Authorization": f"token {github_token}",
               "User-Agent": github_username}
    # set empty list for total repos scraped
    list_of_repos = []
    # for each page in range of provided number
    for i in range(1, number_of_pages + 1):
        # obtain page data
        response = requests.get(url + str(i), headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find_all('h3')
        # set empty list to agg for each page
        page_list = []
        for repo in content:
            # confirms that h3 tag contains repo information
            if [re.search(r'(\S+)', x.text).group(1) for x in repo.find_all('a')] != []:
                # returns owner username and repo name
                user_name, repo_name = [re.search(r'(\S+)', x.text)\
                                         .group(1) for x in repo.find_all('a')]
                # add to page list for each repo on page
                page_list.extend([f'{user_name}/{repo_name}'])
        # add new page list into existing list for total repos
        list_of_repos.extend(page_list)
        print(f'Page {i} Completed')
    # saves returned list into .py file for calling in later functions
    with open("repos.py", "w") as repos:
        repos.write(f'REPOS = {list_of_repos}')
    return list_of_repos
    
    
def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)