import rauth
import time
import pandas as pd
import re


def main():
    criteria = ["fun things to do", "restaurants", "cafes", "businesses", "attractions"]
    api_calls = []
    fileName = 'feed.txt'
    # Pipelining the feed to the flatfile
    feedPreparation(fileName, criteria)
    print ("Yelp Search Feed Collected Sucessfully")


## function to store the feed in the pipe delimited file
def feedPreparation(fileName, criteria):
    f = open(fileName, 'wb')
    for x in criteria:
        params = get_search_parameters(x)
        d = get_results(params)
        if 'businesses' in d:
            for business in d['businesses']:
                k = '%s|%s|%s|%s|%s|%s|%s|%s\n' % (business['name'], business['rating'], business['review_count'],
                                                   getCategories(business['categories']),
                                                   ' '.join(business['location']['display_address']),
                                                   business['location']['coordinate']['latitude'],
                                                   business['location']['coordinate']['longitude'], x)
                f.write(k.encode('utf-8'))  # writing to the output file

        # Be a good internet citizen and rate-limit yourself
        time.sleep(1.0)
    f.close()


# function to interact with the YELP API
def get_results(params):
    # Obtain these from Yelp's manage access page
    consumer_key = "#########################"
    consumer_secret = "###########################"
    token = "#############################"
    token_secret = "###########################"

    session = rauth.OAuth1Session(
        consumer_key=consumer_key
        , consumer_secret=consumer_secret
        , access_token=token
        , access_token_secret=token_secret)

    request = session.get("http://api.yelp.com/v2/search", params=params)

    # Transforms the JSON API response into a Python dictionary
    data = request.json()
    session.close()

    return data


# function to define the search parameters
def get_search_parameters(criteria):
    # See the Yelp API for more details
    params = {}
    params["term"] = criteria
    params["location"] = "San Francisco"
    params["radius_filter"] = "2000"
    params["limit"] = "20"
    # params["sort"]= 2

    return params


# Preprocessing the categories to eliminate the duplicates
def getCategories(categories):
    cat = ''
    for k in categories:
        temp = list(map(getProcessedString, k))
        if temp[0] != temp[1]:
            cat = cat + ','.join(temp) + ','
        else:
            cat = cat + temp[0] + ','
    cat = cat[:-1]
    return cat


# string preprocessing to eliminate the special characters

def getProcessedString(s):
    # code to remove any special characters
    s = re.sub('[^A-Za-z0-9]+', ' ', s)
    return s.lower()


if __name__ == "__main__":
    main()


# In[ ]:
