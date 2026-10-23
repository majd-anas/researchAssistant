#majd anas 0234815
import csv
import os

#sotres the data into csv file
def toCSV(data, title):

    os.makedirs("csv", exist_ok=True)

    path = os.path.join("csv", f"{title}.csv")

    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

#increases the number of searches in numberOfSearchs file
def increaseNumberOfSearches():
    with open("data/numberOfSearchs.txt", "r") as file:
        n = int(file.read())

    n = n + 1
    with open("data/numberOfSearchs.txt", "w") as file:
        file.write(str(n))

#add a search to the top of the file
def addMostRecentSearch(search):
    path = "data/recentSearches.txt"
    try:
        with open(path, "r") as file:
            old_searches = file.readlines()
    except FileNotFoundError:
        old_searches = []
    with open(path, "w") as file:
        file.write(search + "\n")
        file.writelines(old_searches)

#gets total number of searches user had done
def getNumberOfSearches():
    path = "data/numberOfSearchs.txt"

    try:
        with open(path, "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

#gets the most recent search 
def getMostRecentSearch():
    path = "data/recentSearches.txt"

    try:
        with open(path, "r") as file:
            first_line = file.readline().strip()

            if first_line == "":
                return None

            return first_line

    except FileNotFoundError:
        return None