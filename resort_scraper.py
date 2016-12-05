import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import pandas as pd

def get_all_ratings(state_list):
    '''Gets all of the ratings for all of the resorts on onthesnow.com.
    Input: list of states
    Output: ratings dataframe'''

    full_ratings_df = pd.DataFrame(columns= ['overall', 'beginner', 'intermediate', 'expert', 'all_mountain', 'family', 'apres', 'terrain', 'value'])
    for state in state_list:
        print state
        resorts = get_resorts('{}'.format(state))
        ratings = get_ratings(resorts)
        full_ratings_df = pd.concat([full_ratings_df, ratings])
    return full_ratings_df

def get_resorts(state):
    '''Gets the links to all colorado resort review pages and adds them to the resorts list
    Input: State (string, lowercase)
    Output: List of Resorts
    '''
    resort_list = []
    req_home = requests.get('http://www.onthesnow.com/{}/ski-resorts.html'.format(state))
    html_home = BeautifulSoup(req_home.content, 'html.parser')
    table = html_home.find_all('div', attrs={'class': 'resScrollCol8'})[0]
    for link in table.find_all('a'):
        str_link = unidecode(link['href'])
        if 'reviews' in str_link:
            resort_list.append(str_link)
        else:
            pass
    return resort_list

def get_ratings(resort_list):
    '''Once a list of resort links has been collected, this goes to all of the review pages and scrapes the reviews themselves.
    Input: list of resorts
    Output: Dictionary of resort ratings (keys: resort name, values: dictionary of different ratings)
    '''

    rating_dict = {}
    for resort in resort_list:
        print resort
        req_resort = requests.get('http://www.onthesnow.com{}'.format(resort))
        print req_resort.status_code
        if req_resort.status_code == 200:
            html_resort = BeautifulSoup(req_resort.content, 'html.parser')

            resort_name = unidecode(html_resort.find_all('span', attrs={'class': 'resort_name'})[0].text)
            overall_rating = unidecode(html_resort.find_all('div', attrs={'class': 'rating_header'})[0].find_all('b')[0].text)
            beginner_rating = unidecode(html_resort.find_all('div', attrs={'class': 'white_inset clearfix'})[0].find_all('b')[0].text)
            intermediate_rating = unidecode(html_resort.find_all('div', attrs={'class': 'white_inset clearfix'})[0].find_all('b')[3].text)
            expert_rating = unidecode(html_resort.find_all('div', attrs={'class': 'white_inset clearfix'})[0].find_all('b')[3].text)
            all_mountain_rating = unidecode(html_resort.find_all('div', attrs={'class': 'white_inset clearfix'})[0].find_all('b')[9].text)
            family_rating = unidecode(html_resort.find_all('div', attrs={'class': 'white_inset clearfix'})[0].find_all('b')[12].text)
            apres_rating = unidecode(html_resort.find_all('div', attrs={'class': 'white_inset clearfix'})[0].find_all('b')[15].text)
            terrain_rating = unidecode(html_resort.find_all('div', attrs={'class': 'white_inset clearfix'})[0].find_all('b')[18].text)
            value_rating = unidecode(html_resort.find_all('div', attrs={'class': 'white_inset clearfix'})[0].find_all('b')[21].text)

            rating_dict['{}'.format(resort_name)] = [overall_rating, beginner_rating, intermediate_rating, expert_rating, all_mountain_rating, family_rating, apres_rating, terrain_rating, value_rating]
        else:
            pass

    ratings_df = pd.DataFrame(rating_dict)
    ratings_df = ratings_df.transpose()
    ratings_df.columns = ['overall', 'beginner', 'intermediate', 'expert', 'all_mountain', 'family', 'apres', 'terrain', 'value']
    return ratings_df


if __name__ == '__main__':
    states = ['colorado', 'utah', 'wyoming', 'montana', 'idaho', 'new-mexico', 'california', 'lake-tahoe', 'nevada', 'oregon', 'washington', 'new-york', 'pennsylvania', 'vermont', 'new-hampshire', 'maine', 'massachusetts', 'michigan', 'minnesota',\
     'wisconsin', 'alberta', 'british-columbia', 'ontario', 'quebec', 'south-america', 'australia', 'new-zealand', 'france', 'austria', 'italy', 'switzerland']
    resort_ratings_df = get_all_ratings(states)
