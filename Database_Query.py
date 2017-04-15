import pypyodbc
import re
from math import radians, cos, sin, asin, sqrt


# query to interact with database and search for matches for a particular category
def getlabelled_entries(category, k):
    global cnx
    category = category.lower()
    cursor = cnx.cursor()
    query = "SELECT * FROM YELPFEED where category_labels like \'%" + category + "%\' order by Rating desc"
    cursor.execute(query)
    gps = getCustomerGPSCoordinates()
    l = []
    for item in cursor:
        l.append(
            '\t'.join([str(item[0]), str(item[1]), str(haversine(gps[1], gps[0], float(item[6]), float(item[5])))]))
    i = 0
    if len(l) == 0:
        return "No matches returned"
    if len(l) <= k:
        for i in l:
            print
            i
    else:
        for i in range(0, k):
            print
            l[i]
    cursor.close()
    return "Records returned successfully"


# query to interact with database and search for matches
def getsearchtag_entries(searchtag, k):
    global cnx
    # Using the like operator
    searchtag = searchtag.lower()
    cursor = cnx.cursor()
    query = "SELECT * FROM YELPFEED where searchtag like \'%" + searchtag + "%\' order by Rating desc"
    # print query
    cursor.execute(query)
    # print type(cursor)
    gps = getCustomerGPSCoordinates()
    l = []
    for item in cursor:
        l.append(
            '\t'.join([str(item[0]), str(item[1]), str(haversine(gps[1], gps[0], float(item[6]), float(item[5])))]))
    i = 0
    if len(l) == 0:
        return "No matches returned"
    if len(l) <= k:
        for i in l:
            print
            i
    else:
        for i in range(0, k):
            print
            l[i]

    cursor.close()
    return "Records returned successfully"


def getCustomerGPSCoordinates():
    # function to return the GPS coordinates
    gps = [37.789, -122.409]
    return gps


# distance calculation function
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


# Adding distance based measure,map with pandas

if __name__ == "__main__":
    cnx = pypyodbc.connect(r'Driver={SQL Server};Server=YASH\SQLEXPRESS;Database=YELPETL;Trusted_Connection=yes;')
    process = 'Y'
    while process != 'N':
        print("Enter the search criteria: ")
        print ("Ex: searchtag restaurants 10 \n label comedy 10")
        print("Output : NAME, RATING ,DISTANCE FROM CUSTOMER separated by tabs")

        input = input().split(' ')
        if input[0] == 'searchtag':
            print
            getsearchtag_entries(input[1], int(input[2]))
        if input[0] == 'label':
            print
            getlabelled_entries(input[1], int(input[2]))
        print
        "Do you want to continue : Y or N"
        process = input()
    cnx.close()