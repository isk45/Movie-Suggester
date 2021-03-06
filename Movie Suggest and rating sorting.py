import requests
import json

def get_movies_from_tastedive(st):
    d = {'q':st ,'type':'movies','limit':11}
    m = requests.get('https://tastedive.com/api/similar' , params = d)
    return m.json()
    
def extract_movie_titles(dic):
    lis=[]
    for res in dic["Similar"]["Results"]:
        lis.append(res["Name"])
    return lis

def get_related_titles(lis):
    rel_mov = []
    for mov in lis:
        rel = extract_movie_titles(get_movies_from_tastedive(mov))
        for movie in rel:
            if movie not in rel_mov:
                rel_mov.append(movie)
    return rel_mov

def get_movie_data(title):
    d = {'t':title, 'r':'json', 'apikey':'API KEY'}
    rev = requests.get('http://www.omdbapi.com/', params = d)
    return rev.json()

def get_movie_rating(d):
    for lis in d['Ratings']:
        if lis['Source'] == 'Rotten Tomatoes':
            return int(lis['Value'][:2])
    else:
        return 0  

def get_sorted_recommendations(lis_titles):
    lis = get_related_titles(lis_titles)
    lis2 = sorted(lis , key = lambda x: (get_movie_rating(get_movie_data(x)), x[0]), reverse = True)
    return lis2

sorted_list = get_sorted_recommendations(['carry on jatta'])
for mov in sorted_list:
  print(mov)
