# built-in
import requests
import os

from multiprocessing import Pool
from time import sleep
# user-installed
import pandas as pd

from tqdm import tqdm
from numpy.random import uniform
from dotenv import load_dotenv

load_dotenv()

# constants
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
NAME_DEMO = __name__

search_terms = ['Bad Bunny', 
                     '6LACK ', 
                     'Thee Sacred Soul', 
                     'Fantastic Negrito', 
                     'Tony Succar']

def genius(search_term, per_page=15):
    try:
        genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                            f"access_token={ACCESS_TOKEN}&per_page={per_page}"
        
        response = requests.get(genius_search_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        
        json_data = response.json()
        return json_data['response']['hits']
    except requests.exceptions.RequestException as e:
        print(f"Error in genius API request for {search_term}: {e}")
        return []

def genius_to_df(search_term, n_results_per_term=10, verbose=True, savepath=None):
    try:
        json_data = genius(search_term, per_page=n_results_per_term)
        hits = [hit['result'] for hit in json_data]
        df = pd.DataFrame(hits)

        # ... (rest of your code)

        return df
    except Exception as e:
        print(f"Error processing data for {search_term}: {e}")
        return pd.DataFrame()

def genius_to_dfs(search_terms, **kwargs):
    dfs = []

    for search_term in tqdm(search_terms):
        df = genius_to_df(search_term, **kwargs)
        if not df.empty:
            dfs.append(df)

    return pd.concat(dfs)

if __name__ == "__main__":
    with Pool(8) as p:
        results = p.map(genius_to_df, search_terms)
        print("\nTotal number of results: ", len(results))

    df_genius = pd.concat(results)

    df_genius.to_csv('./data/best_music_mp.csv', index=False)