from PullWebpageData import get_toread_titles
from QueryWebpage import query_southbury_library

USER_ID = '3696598'

titles_considered = 0
for t in get_toread_titles(USER_ID):
    print("Searching for {}...".format(t))
    for r in query_southbury_library(t):
        if len(t):
            print("|".join(r))
    titles_considered += 1
print("titles searched: "+str(titles_considered))