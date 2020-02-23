from PullWebpageData import get_toread_titles
from QueryWebpage import query_southbury_library

USER_ID = '3696598'

titles_considered = 0
titles_hit = 0
page = 0
while titles_hit < 50:
    page += 1
    for t in get_toread_titles(USER_ID, page):
#        print("Searching for {}...".format(t))
        for r in query_southbury_library(t):
            titles_hit += 1
            if len(r)>0:
                print("|".join(r))
        titles_considered += 1
print("titles searched: "+str(titles_considered))
print("results returned: "+str(titles_hit))
