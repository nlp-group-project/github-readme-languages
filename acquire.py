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
import time
import re

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token: https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

#------------------------------------------------------------------------------------------------------------

#REPOS = ['justinmk/vim-sneak', 'google-research-datasets/Objectron', 'shoes/shoes4', 'shoes/shoes-deprecated', 'filamentgroup/shoestring', 'devefy/Flutter-Adidas-Shoes-Ecommerce-App-UI', 'druv5319/Sneaks-API', 'tylerburleigh/nike-buy-bot', 'afgprogrammer/Flutter-Shoes-Shop-App', 'matadon/mizuno', 'ashbb/green_shoes', 'hua1995116/react-shopping', 'shoes/shoes3', 'Joxroxagain/adidas-bot', 'Julian/vim-textobj-variable-segment', 'mustfaibra/RoFFu', 'nelsonsilva/yUMLmeRails', 'kevin-powell/shoes', 'BenjaminMahmic/shoes_shop', 'georgewalton/Sandals', 'bdkay/nike-bot', 'dzt/supreme-api', 'micah5/sneaker-generator', 'alastairparagas/nikeshoes-bot', 'thunt01/SneakerBot-App', 'petejkim/socks', 'WebAR-rocks/WebAR.rocks.hand', 'kriziu/shoes-ecommerce', 'rashidwassan/flutter-ecommerce-app-ui', 'rprokap/pset-9', 'seuliufeng/DeepSBIR', 'cmer/shoestrap', 'reverentgeek/public-speaking', 'yuqian1023/Deep_SBIR_tf', 'sopheamen007/app.mobile.shoes-online-app-ui', 'yousefissa/Shoe-Raffle-Scripts', 'iw-an/shoepalace', 'chang-chih-yao/Shoes-Try-On-in-AR', 'brandontruggles/Selenium-Shoe-Bot-NakedCPH', 'trananhtuat/nike-shoes-landing-page', 'sloria/ped', 'shoes/shoesrb.com', 'rileyjshaw/tappy', 'finallyfunctional/vr-shoes-3d-models', 'onyxblade/ShenmeGUI', 'aslansky/react-stack-playground', '/ashbb/shoes_tutorial_html', 'iamyuu/shoes-commerce', 'chriseidhof/shoes-swift', 'luizbatanero/gostack-rocketshoes-react', 'mohamedebrahim96/Quiz-App', 'MarkipTheMudkip/in-class-project-2', 'rwema3/ShoesShop-Flutter', 'Kazuhito00/Unity-Barracuda-Objectron-WebGL', 'cfal/shoes', 'ashbb/shoes_tutorial_walkthrough', 'ankitkanojia/eCommerce_Shop', 'atapas/shoes', 'GNico/spring-eshop', 'toothrot/gutter', 'bonamoogy/Flutter-Shoes-Store', 'mkarasoff/shoe', 'ioofy/fashionsweb', 'CShorten/NIKE_vs_ADIDAS', 'mrthinger/Shubi', 'dilip-dawadi/shoeStore', 'WANNABY/WannaSDK-iOS', 'ashbb/purple_shoes', 'cloudwalking/Hermes', 'akavalar/SSAS-on-a-shoestring', '/nmewada01/e-commerce', '/aadilkhalifa/virtual-try-on', '/jrzaurin/Shoe-Shape-Classifier', '/DVS2000/UI-SHOES-STORE', '/Raynos/boot', '/fariasmateuss/shoes-out', '/swerner/brown_shoes', '/mcantelon/fashion-quest', '/jballanc/shoes-tmbundle', '/noopkat/meowshoes', '/hacketyhack/blue_shoes', '/sebastianmusial/jest-module-name-mapper', '/llSourcell/Bitcoin_Mining_Shoes', '/RamsesRomeroJr/HypeGeek', '/skrimxyz/skm-stealshoes', '/RenatoLucasMota/ShoeStore', '/Axiologue/ShoeScraper', '/adamclerk/deck', '/wasnotrice/shoes-atom', '/developer-junaid/Nike-Shoe-Store', '/emersonbroga/super-shoes', '/evuraan/yellowShoes', '/alisonmonteiro/shoe-size-converter', '/valeriofarias/learn-bdd-playing-dice-book', '/kreem007/-kreem07', '/ipenywis/react-3d-card', '/ashbb/shoes_hack_note', '/nomo-w/nike-monitor', '/shoes/brown_shoes', '/Klerith/shoesapp', '/luizbatanero/gostack-rocketshoes-react-native', '/finallyfunctional/vr-shoes-software', '/nicferrier/shoes-off', '/PoHsin-Lin/gait-parameters-analysis-LSTM', '/Dev-Adnani/Scarvs-Flutter', '/LucaArgentieri/Shoe-Discord-Bot', '/machumzd/MZEE-Shoes', '/wilkerlucio/bow_and_arrow', '/bixbydevelopers/capsule-sample-shoe', '/ZoranPandovski/ProdirectScraper', '/PragTob/pomodoro_tracker', '/pedromg/twittershoes', '/PragTob/wingtips', '/paceaux/McSandy--the-HTML5-offline-Sandbox', '/karmi/sheep_in_your_shoes', '/Johnnyhoboy-zz/MARK', '/yusufisbilir/Shoes-Website', '/haya14busa/vim-signjk-motion', '/AbolfaZlRezaEe/NikY', '/rprokap/entremanure', '/tejastn10/ShoeShoppee', '/soleHats/SNKRS-Moniter', '/Andrew-Tsegaye/Advanced-shoe-store-web-app', '/adminmyserver/ruby_pong', '/eddieferrer/sizesquirrel-open', '/SarangKumar/Footgear-corner', '/antonjlin/adidas-account-generator', '/AnmolArya1/Object_Detection_Project_using_openCv', '/OmarJ9/shoes_app', '/lljk/shoes-stuff', '/iQua/CVPR2020-Shoestring', '/mresan/ShoesE-CommerceApp', '/byprogrammers/LCRN05-nike-shoes-ecommerce-app-expo', '/NasirKhalid24/2Dto3D-Shoes', '/RedStewart/StockX-Low-Price-Monitor', '/JenkinsRobotics/JenkinsCNC', '/Hina-softwareEngineer/shoe-store', '/sausheong/auth', '/sloria/vim-ped', '/Yarnamite/2b2t-shoeSizeAndHeightList', '/barackm/Niky', '/danderfer/Comp_Sci_Sem_2', '/zzak/shoes-contrib', '/Maaarcocr/scarpe', '/qrush/snake', '/ashbb/sudoku_on_shoes', '/wildoctopus/FeetAndShoeMeasurement', '/ashbb/shoes_tutorial', '/ashbb/orange_shoes', '/joseeestrada/jimmyjazzbot', '/byprogrammers/LCRN05-nike-shoes-ecommerce-app', '/wessyy/shoebot', '/ibaiGorordo/shoeDetection', '/scoobytux/reactjs-shoes', '/Raynos/mux-demux-shoe', '/DanieleEwick/Challenge-Jordan-Shoes', '/tiegz/shoes-textmate-bundle', '/h-lame/talon', '/NodeTogether/emergency-compliment', '/wasnotrice/shoes-qt', '/saces/Shoeshop', '/steveklabnik/frp_shoes', '/cesaroviedo1234/nike-bot', '/codlizzy/shose_projects', '/skade/talaria', '/e-dant/shoestring', '/Sebu/Appetizr', '/cawel/ric-rac-roe', '/HarsimranBarki/rapid-store', '/eugeneware/angularjs-shoe', '/muhammadumair12345/shoe-store-app', '/mathieugagne/shoe-store', '/slackvishal/flutter_ecommerce_nikeshoe_app', '/MERN-Folk/Full-SorceCode-ShoeShop-Ecommerce-Web', '/iuri-pdista/nike-bot', '/yenchiah/SENSEable-Shoes', '/sugi-chan/shoes_siamese', '/JavascriptDeNoobAPro/2021-online-shoestore', '/ashbb/code_wrapper_on_shoes', '/osgcc/osgcc4-feuq', '/markryall/business_socks', '/napcs/shoes_demo_apps', '/dscape/rudolph', '/wasnotrice/shoes-black', '/JNicolao/Tom-ARP', '/DavutUdemy/SHOESTORELOGICCODE', '/karmi/shoes_demonstration_apps', '/iuri-pdista/snkrs-bot-extension', '/TheMoonMoth/SixWordStories', '/stayrealddc/BuyShoes', '/Leandro-Goncalves/react-shoe', '/fnichol/nameit', '/ferhatkatar/Customer_Segmentation_w_Unsupervised_Learning', '/flutter-devs/flutter_ecommerce_shoes', '/adarsh-technocrat/ShoesShop-Flutter-App-UI', '/alexyoung/snake-shoes', '/kaushiksheel/ShoesStore-Frontend-Typescript', '/devyn/shoes-web', '/mjokic/adidas_carter', '/dissyulina/shoesandmore']

REPOS = ['justinmk/vim-sneak',
 'google-research-datasets/Objectron',
 'shoes/shoes4',
 'shoes/shoes-deprecated',
 'filamentgroup/shoestring',
 'devefy/Flutter-Adidas-Shoes-Ecommerce-App-UI',
 'druv5319/Sneaks-API',
 'tylerburleigh/nike-buy-bot',
 'afgprogrammer/Flutter-Shoes-Shop-App',
 'matadon/mizuno',
 'ashbb/green_shoes',
 'hua1995116/react-shopping',
 'shoes/shoes3',
 'Joxroxagain/adidas-bot',
 'Julian/vim-textobj-variable-segment',
 'mustfaibra/RoFFu',
 'nelsonsilva/yUMLmeRails',
 'kevin-powell/shoes',
 'BenjaminMahmic/shoes_shop',
 'georgewalton/Sandals',
 'bdkay/nike-bot',
 'dzt/supreme-api',
 'micah5/sneaker-generator',
 'alastairparagas/nikeshoes-bot',
 'thunt01/SneakerBot-App',
 'petejkim/socks',
 'WebAR-rocks/WebAR.rocks.hand',
 'kriziu/shoes-ecommerce',
 'rashidwassan/flutter-ecommerce-app-ui',
 'rprokap/pset-9',
 'seuliufeng/DeepSBIR',
 'cmer/shoestrap',
 'reverentgeek/public-speaking',
 'yuqian1023/Deep_SBIR_tf',
 'sopheamen007/app.mobile.shoes-online-app-ui',
 'yousefissa/Shoe-Raffle-Scripts',
 'iw-an/shoepalace',
 'chang-chih-yao/Shoes-Try-On-in-AR',
 'brandontruggles/Selenium-Shoe-Bot-NakedCPH',
 'trananhtuat/nike-shoes-landing-page',
 'sloria/ped',
 'shoes/shoesrb.com',
 'rileyjshaw/tappy',
 'finallyfunctional/vr-shoes-3d-models',
 'onyxblade/ShenmeGUI',
 'aslansky/react-stack-playground',
 'ashbb/shoes_tutorial_html',
 'iamyuu/shoes-commerce',
 'chriseidhof/shoes-swift',
 'luizbatanero/gostack-rocketshoes-react',
 'mohamedebrahim96/Quiz-App',
 'MarkipTheMudkip/in-class-project-2',
 'rwema3/ShoesShop-Flutter',
 'Kazuhito00/Unity-Barracuda-Objectron-WebGL',
 'cfal/shoes',
 'ashbb/shoes_tutorial_walkthrough',
 'ankitkanojia/eCommerce_Shop',
 'atapas/shoes',
 'GNico/spring-eshop',
 'toothrot/gutter',
 'bonamoogy/Flutter-Shoes-Store',
 'mkarasoff/shoe',
 'ioofy/fashionsweb',
 'CShorten/NIKE_vs_ADIDAS',
 'mrthinger/Shubi',
 'dilip-dawadi/shoeStore',
 'WANNABY/WannaSDK-iOS',
 'ashbb/purple_shoes',
 'cloudwalking/Hermes',
 'akavalar/SSAS-on-a-shoestring',
 'nmewada01/e-commerce',
 'aadilkhalifa/virtual-try-on',
 'jrzaurin/Shoe-Shape-Classifier',
 'DVS2000/UI-SHOES-STORE',
 'Raynos/boot',
 'fariasmateuss/shoes-out',
 'swerner/brown_shoes',
 'mcantelon/fashion-quest',
 'jballanc/shoes-tmbundle',
 'noopkat/meowshoes',
 'hacketyhack/blue_shoes',
 'sebastianmusial/jest-module-name-mapper',
 'llSourcell/Bitcoin_Mining_Shoes',
 'RamsesRomeroJr/HypeGeek',
 'skrimxyz/skm-stealshoes',
 'RenatoLucasMota/ShoeStore',
 'Axiologue/ShoeScraper',
 'adamclerk/deck',
 'wasnotrice/shoes-atom',
 'developer-junaid/Nike-Shoe-Store',
 'emersonbroga/super-shoes',
 'evuraan/yellowShoes',
 'alisonmonteiro/shoe-size-converter',
 'valeriofarias/learn-bdd-playing-dice-book',
 'ashbb/shoes_hack_note',
 'nomo-w/nike-monitor',
 'shoes/brown_shoes',
 'Klerith/shoesapp',
 'luizbatanero/gostack-rocketshoes-react-native',
 'finallyfunctional/vr-shoes-software',
 'nicferrier/shoes-off',
 'PoHsin-Lin/gait-parameters-analysis-LSTM',
 'Dev-Adnani/Scarvs-Flutter',
 'LucaArgentieri/Shoe-Discord-Bot',
 'machumzd/MZEE-Shoes',
 'wilkerlucio/bow_and_arrow',
 'bixbydevelopers/capsule-sample-shoe',
 'ZoranPandovski/ProdirectScraper',
 'PragTob/pomodoro_tracker',
 'pedromg/twittershoes',
 'PragTob/wingtips',
 'paceaux/McSandy--the-HTML5-offline-Sandbox',
 'karmi/sheep_in_your_shoes',
 'Johnnyhoboy-zz/MARK',
 'yusufisbilir/Shoes-Website',
 'haya14busa/vim-signjk-motion',
 'AbolfaZlRezaEe/NikY',
 'rprokap/entremanure',
 'tejastn10/ShoeShoppee',
 'soleHats/SNKRS-Moniter',
 'Andrew-Tsegaye/Advanced-shoe-store-web-app',
 'adminmyserver/ruby_pong',
 'eddieferrer/sizesquirrel-open',
 'SarangKumar/Footgear-corner',
 'antonjlin/adidas-account-generator',
 'AnmolArya1/Object_Detection_Project_using_openCv',
 'OmarJ9/shoes_app',
 'lljk/shoes-stuff',
 'iQua/CVPR2020-Shoestring',
 'mresan/ShoesE-CommerceApp',
 'byprogrammers/LCRN05-nike-shoes-ecommerce-app-expo',
 'NasirKhalid24/2Dto3D-Shoes',
 'RedStewart/StockX-Low-Price-Monitor',
 'JenkinsRobotics/JenkinsCNC',
 'Hina-softwareEngineer/shoe-store',
 'sausheong/auth',
 'sloria/vim-ped',
 'Yarnamite/2b2t-shoeSizeAndHeightList',
 'barackm/Niky',
 'danderfer/Comp_Sci_Sem_2',
 'zzak/shoes-contrib',
 'Maaarcocr/scarpe',
 'qrush/snake',
 'ashbb/sudoku_on_shoes',
 'wildoctopus/FeetAndShoeMeasurement',
 'ashbb/shoes_tutorial',
 'ashbb/orange_shoes',
 'joseeestrada/jimmyjazzbot',
 'byprogrammers/LCRN05-nike-shoes-ecommerce-app',
 'wessyy/shoebot',
 'ibaiGorordo/shoeDetection',
 'scoobytux/reactjs-shoes',
 'Raynos/mux-demux-shoe',
 'DanieleEwick/Challenge-Jordan-Shoes',
 'tiegz/shoes-textmate-bundle',
 'h-lame/talon',
 'NodeTogether/emergency-compliment',
 'wasnotrice/shoes-qt',
 'saces/Shoeshop',
 'steveklabnik/frp_shoes',
 'cesaroviedo1234/nike-bot',
 'codlizzy/shose_projects',
 'skade/talaria',
 'e-dant/shoestring',
 'Sebu/Appetizr',
 'cawel/ric-rac-roe',
 'HarsimranBarki/rapid-store',
 'eugeneware/angularjs-shoe',
 'muhammadumair12345/shoe-store-app',
 'mathieugagne/shoe-store',
 'slackvishal/flutter_ecommerce_nikeshoe_app',
 'MERN-Folk/Full-SorceCode-ShoeShop-Ecommerce-Web',
 'iuri-pdista/nike-bot',
 'yenchiah/SENSEable-Shoes',
 'sugi-chan/shoes_siamese',
 'JavascriptDeNoobAPro/2021-online-shoestore',
 'ashbb/code_wrapper_on_shoes',
 'osgcc/osgcc4-feuq',
 'markryall/business_socks',
 'napcs/shoes_demo_apps',
 'dscape/rudolph',
 'wasnotrice/shoes-black',
 'JNicolao/Tom-ARP',
 'DavutUdemy/SHOESTORELOGICCODE',
 'karmi/shoes_demonstration_apps',
 'iuri-pdista/snkrs-bot-extension',
 'TheMoonMoth/SixWordStories',
 'stayrealddc/BuyShoes',
 'Leandro-Goncalves/react-shoe',
 'fnichol/nameit',
 'ferhatkatar/Customer_Segmentation_w_Unsupervised_Learning',
 'flutter-devs/flutter_ecommerce_shoes',
 'adarsh-technocrat/ShoesShop-Flutter-App-UI',
 'alexyoung/snake-shoes',
 'kaushiksheel/ShoesStore-Frontend-Typescript',
 'devyn/shoes-web',
 'mjokic/adidas_carter',
 'dissyulina/shoesandmore']

#------------------------------------------------------------------------------------------------------------

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )

#------------------------------------------------------------------------------------------------------------

def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data

#------------------------------------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------------------------------------

def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )

#------------------------------------------------------------------------------------------------------------

def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""

#------------------------------------------------------------------------------------------------------------

def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    
    print(repo)
    
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

#------------------------------------------------------------------------------------------------------------

def scrape_github_data():
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
 
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)
    
#------------------------------------------------------------------------------------------------------------
        
def get_repo_links(github_token=github_token, github_username=github_username,
                                         topic='shoes', number_of_pages=20):
    '''
    Takes in a topic, your unique github API token, and your github username as
    strings and an interger for the number of pages to query
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
        content = soup.find_all('a', class_='v-align-middle')
        print(response)
        time.sleep(2)
        
        
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
    
    print(response)
    
    return list_of_repos

#------------------------------------------------------------------------------------------------------------

def get_readme_data():
    
    '''
    Scrapes a variety of news articles. Must create a topic_list variable that contains the 
    category of the news article. Example: ['business','technology','sports']
    '''

    # Check if JSON file exists
    file = 'readme_data.json'
    
    if os.path.exists(file):
        
        with open(file) as f:
            
            return json.load(f)
    
    
    readme_data = scrape_github_data()
    
    
    # Save into JSON
    with open(file, 'w') as f:
        
        json.dump(readme_data, f)
    
    
    return readme_data

#------------------------------------------------------------------------------------------------------------

def get_repo_links_200(github_token = github_token, github_username = github_username,
                                         topic = 'shoes', number_of_pages = 20):
    '''
    Takes in a topic, your unique GitHub API token, and 
    your GitHub username as strings, along with an interger for 
    the number of pages to query.
    Returns : a list of keyworded repositories from GitHub.
    '''
    # set URL without page number
    #url = f'https://github.com/topics/{topic}?&s=stars&page='
    
    
    # set header for github authorisation
    headers = {"Authorization": f"token {github_token}",
               "User-Agent": github_username}
    
    # set empty list for total repos scraped
    list_of_repos = []
    
    # for each page in range of provided number
    for i in range(1, number_of_pages + 1):
        
        url = f'https://github.com/search?o=desc&p={i}&q={topic}&s=stars&type=Repositories'
        
        # obtain page data
        response = requests.get(url + str(i), headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find_all('a', class_='v-align-middle')
        print(response)
        
        repos_list = []
        
        for repo in content:
        
            link = repo['href']
            print(link)
            
            repos_list.append(link)
            print(repos_list)
        
        time.sleep(20)
        
        list_of_repos.extend(repos_list)
        print(list_of_repos)
        print()
    
    # saves returned list into .py file for calling in later functions
    with open("repos.py", "w") as repos:
        repos.write(f'REPOS = {list_of_repos}')
    
    print(response)
    
    return list_of_repos
