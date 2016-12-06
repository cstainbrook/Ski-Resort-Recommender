import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import pandas as pd
import numpy as np


def get_all_ratings(state_list):
    '''Gets all of the ratings for all of the resorts on onthesnow.com.
    Input: list of states
    Output: ratings dataframe'''

    full_ratings_df = pd.DataFrame(columns= ['user_name', 'resort_name', 'rating'])
    for state in state_list:
        print state
        resorts = get_resorts('{}'.format(state))
        ratings = get_user_ratings(resorts)
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

def get_user_ratings(resort_list):
    '''Once a list of resort links has been collected, this goes to all of the review pages and scrapes the user ratings of the resort.
    Input: list of resorts
    Output: Dictionary of resort ratings (keys: resort name, values: dictionary of different ratings)
    '''

    rating_df = pd.DataFrame(columns=['user_name', 'resort_name', 'rating'])
    for resort in resort_list:
        print resort
        req_resort = requests.get('http://www.onthesnow.com{}'.format(resort))
        print req_resort.status_code
        if req_resort.status_code == 200:
            html_resort = BeautifulSoup(req_resort.content, 'html.parser')
            resort_name = unidecode(html_resort.find_all('span', attrs={'class': 'resort_name'})[0].text)
            for user, rating in zip(html_resort.find_all('ul', attrs={'class': 'entries'})[0].find_all('h3'), html_resort.find_all('ul', attrs={'class': 'entries'})[0].find_all('b', attrs={'class': 'rating'})):
                user_str = unidecode(user.text).split(' ')[0]
                rating_int = int(rating.text)
                rating_df.append([[user_str, resort, rating_int]])
            try:
                num_reviews = int(unidecode(html_resort.find_all('p', attrs={'class': 'displaying'})[0].text).split('\t')[-1].split(' ')[0])
                num_pages = num_reviews/6.
                start_review = 6
                if num_reviews > 6:
                    for page in np.arange(num_pages):
                        req_review = requests.get('http://www.onthesnow.com{}?startRow={}&numRows=6'.format(resort, start_review))
                        print req_review.status_code
                        if req_resort.status_code == 200:
                            html_review = BeautifulSoup(req_review.content, 'html.parser')
                            for user, rating in zip(html_review.find_all('ul', attrs={'class': 'entries'})[0].find_all('h3'), html_review.find_all('ul', attrs={'class': 'entries'})[0].find_all('b', attrs={'class': 'rating'})):
                                user_str = unidecode(user.text).split(' ')[0]
                                rating_int = int(rating.text)
                                new_df = pd.DataFrame([[user_str, resort_name, rating_int]], columns=['user_name', 'resort_name', 'rating'])
                                rating_df = rating_df.append(new_df, ignore_index=True)
                                start_review += 6
                        else:
                            pass
                else:
                    pass
            except IndexError:
                pass
        else:
            pass
    return rating_df


if __name__ == '__main__':
    states = ['new-mexico', 'minnesota', 'colorado', 'utah', 'wyoming', 'montana', 'idaho', 'california', 'lake-tahoe', 'nevada', 'oregon', 'washington', 'new-york', 'pennsylvania', 'vermont', 'new-hampshire', 'maine', 'massachusetts', 'michigan',\
     'wisconsin', 'alberta', 'british-columbia', 'ontario', 'quebec', 'south-america', 'australia', 'new-zealand', 'france', 'austria', 'italy', 'switzerland']
    user_ratings_df = get_all_ratings(states)
