#majd anas 0234815
from datetime import date
import os
import models
import serpapi
import pickle
import storage

#creates new folder if it doesn't exist or retrieves existing folder
def getFolder(lib):
    print("name of the folder you want to store your paper at?")
    title = input()
    if lib.folderInLibrary(title):
        print("here")
        return lib.getFolder(title)
    else:
        return lib.addFolder(models.Folder(title))

#my serpapi api key to access google scholar
def apikey():
    return "1a7548d4644e90465207acbf3eb5acfb7f10b16604d3c966e122596d6517cc3d"

#extracts the organic result section from result and checks if result returned an error 
def processResults(result):
    if "error" in result:
        print(f"error: {result["error"]}")
        return False
    else:
        print("query was successful")
        organic_result = result["organic_results"]
        return organic_result

#returns result from user search
def search():

    query=getUserQuery()
    storage.addMostRecentSearch(query["q"])
    storage.increaseNumberOfSearches()
    client = serpapi.Client(api_key=apikey())
    results = client.search(query)
    # results = data.results  # mock data
    return results

#stores the information in organic_results into a folder
def processRequest(result, folder):
    organicResult = processResults(result)
    for i in range(0, len(organicResult)):
        authors = getAuthors(organicResult[i])
        paper = models.Paper(
            organicResult[i]["title"] + " " + organicResult[i]["result_id"],
            organicResult[i]["result_id"] if "result_id" in organicResult[i] else"",
            organicResult[i]["link"] if "link" in organicResult[i] else "",
            organicResult[i]["snippet"] if "snippet" in organicResult[i] else "",
            organicResult[i]["inline_links"]["cited_by"]["total"] if "total" in organicResult[i]["inline_links"]["cited_by"] else "",
            " ",
            authors,
        )
        folder.addPaper(paper)

#gets the paper authors and checks if they exist 
def getAuthors(paper):
    if "authors" in paper["publication_info"]:
        authors = paper["publication_info"]["authors"]
    else:
        return []
    authorArray = []
    for i in range(0, len(authors)):
        authorId = ""
        authorName = ""
        link = ""
        if "author_id" in authors[i]:
            authorId = authors[i]["author_id"]
        if "name" in authors[i]:
            authorName = authors[i]["name"]
        if "link" in authors[i]:
            link = authors[i]["link"]
        authorArray.append(models.Author(authorName, authorId, link))

    return authorArray

# creates a library with a predefined title
def createLibrary():
    library = models.Library("myLibrary")
    return library

#packages and filters the search parameters in a query variable
def getUserQuery():
    parameters = getUserInput()
    query = {"engine": "google_scholar"}
    for key, value in parameters.items():
        if value is None:
            continue
        query.update({key: value})
    return query

#gets the search parameter from the user
def getUserInput():
    as_ylo = as_yhi = None
    q = input("what topic are you researching?\n")
    hl = input("what language are you searching in?(en/es/ar..)\n")
    num = int(input("how many results are you looking for?(1-20)\n"))
    while 20 < num or num < 1:
        num = int(input("input a valid number of searches!(1-20)\n"))
    yr = input("are there specific years you want to be included?(y/n)\n")
    if yr == "y":

        as_ylo = int(input("set the start year\n"))
        while as_ylo > date.today().year:
            as_ylo = int(input("choose a valid start year!\n"))

        ey = input("is there an end year?(y/n)\n")

        if ey == "y":
            as_yhi = int(input("set the end year\n"))
            while as_yhi < as_ylo:
                as_yhi = int(input("choose valide end year (higher than start year)\n"))

    return {"q": q, "hl": hl, "as_ylo": as_ylo, "as_yhi": as_yhi, "num": num}

#searches for papers on google scholar
def lookUpPapers(lib):
    result = search()
    folder = getFolder(lib)
    if result == False:
        return False
    try:
        processRequest(result, folder)
    except KeyError as e:
        print("error key was not found")
    finally:
        saveLib(lib)


#prints the folders in library
def showFolders(lib):
    print("Your Folders:")
    lib.showFolders()

#prints papers in a folder
def seeFolderContent(lib, title):

    if title in lib.folderInLibrary(title):
        folder = lib.getFolder(title)
        folder.showPapers()
    else:
        print("no folder with such name")

#prints paper info
def seePaperDetails(folder, title):
    paper = folder.getPaper(title)
    paper.showPaperInfoMore()

#gets the library or creates one if it doesn't exist
def getStoredLib():
    lib = None
    if os.path.exists("lib.pkl"):
        with open("lib.pkl", "rb") as file:
            lib = pickle.load(file)
    else:
        lib = createLibrary()

    return lib

#saves library to pickle file
def saveLib(lib):
    with open("lib.pkl", "wb") as file:
        pickle.dump(lib, file)

#deletes folder from library
def deleteFolder(lib):
    showFolders(lib)
    folderDel = input("enter folder you want to delete[input -1 to exit]")
    while not lib.folderInLibrary(folderDel) or folderDel != "-1":
        folderDel = input("choose a folder that exists or [ -1 to exit]\n")
    if folderDel == "-1":
        return False
    else:
        lib.deleteFolder(folderDel)
        print("deleting successful")
        return True

#ui function to store folder content to csv file
def storeOp(lib, title):
    folder = lib.getFolder(title)
    try:
        print("folder items")
        folder.showPapersTitles()
        
        folder.storeFolderItemsToCSV()
    except UnicodeEncodeError as e:
        print("unicode error happened")
    finally:
        saveLib(lib)
    print("papers stored successfuly check your csv folder")

#ui function to rename a folder
def renameOp(lib, title):
    rename = input("enter new folder name\n")
    lib.renameFolder(title, rename)

#function to delete a folder from library
def deleteOp(lib, folderDel):
    lib.deleteFolder(folderDel)
    print("deleting successful")

#function to view folder content
def viewOp(lib, title):
    folder = lib.getFolder(title)
    folder.showPapers()
    print(f"these are papers in folder[{title}] ")

#performs folder operations
def folderOperation(op, lib):
    showFolders(lib)
    opName = ""
    if op == 1:
        opName = "view papers"
    elif op == 2:
        opName = "delete"
    elif op == 3:
        opName = "rename"
    else:
        opName = "save to csv"

    title = input(f"enter folder you want to {opName}[-1 to exit]\n")
    while not lib.folderInLibrary(title) and title != "-1":
        title = input("choose a folder that exists or [ -1 to exit]\n")
    if title == "-1":
        return False
    else:
        if op == 1:
            viewOp(lib, title)
        elif op == 2:
            deleteOp(lib, title)
        elif op == 3:
            renameOp(lib, title)
        else:
            storeOp(lib, title)
        return True

#ui function to provide folder operation
def manageFolders(lib):
    print(
        "1-[view papers in folder] 2-[delete a folder] 3-[rename a folder] 4-[save folder to csv file] 5-[back to main menue]"
    )
    print("choose by typing a number")
    n = int(input())
    if n == 1:
        folderOperation(1, lib)
    elif n == 2:
        folderOperation(2, lib)
    elif n == 3:
        folderOperation(3, lib)
    elif n == 4:
        folderOperation(4, lib)
    elif n == 5:
        return

#view paper details
def paperViewOp(folder, title):
    folder.getPaper(title)
    print("paper viewed")

#function to delete paper from folder
def paperDeleteOp(folder, title):
    status = folder.deletePaper(title)
    if status:
        print("deleted paper successfully")
    else:
        print("deletion failed")

#performs the paper operations
def paperOperation(op, folder):
    print(f"papers in folder[{folder.title}]")
    folder.showPapersTitles()
    opName = ""
    if op == 1:
        opName = "view info"
    elif op == 2:
        opName = "delete"

    title = input(f"enter paper you want to {opName}[-1 to exit]\n")
    while not folder.paperInFolder(title) and title != "-1":
        title = input("choose a paper that exists or [ -1 to exit]\n")
    if title == "-1":
        return False
    else:
        if op == 1:
            paperViewOp(folder, title)
        elif op == 2:
            paperDeleteOp(folder, title)
        return True

#provides operations user can do to papers
def managePapers(lib):
    showFolders(lib)
    title = input(f"enter folder you want the papers of\n")
    while not lib.folderInLibrary(title):
        title = input("choose a folder that exists\n")
    folder = lib.getFolder(title)
    print("1-[view paper info] 2-[delete paper] 3-[back to main menue]")
    print("choose by typing a number")
    n = int(input())
    if n == 1:
        paperOperation(1, folder)
    elif n == 2:
        paperOperation(2, folder)
    elif n == 3:
        return
#gets most recent search from data folder
def mostRecentSearch():
    search=storage.getMostRecentSearch()
    print(f"most recent search {search}")

#gets number of searces by user
def numberOfSearches():
        n=storage.getNumberOfSearches()
        print(f"you have done {n} searches")
    
#runs the program
def ui():

    lib = getStoredLib()

    print("welcome to your research Library!")
    n = 0
    while n != 7:
        print("what do you want to do? :)")
        print(
            "1-[search for papers] 2-[view folders] 3-[manage folders] 4-[manage papers] 5-[most recent searches] 6-[number of searches] 7-exit"
        )
        print("choose by typing a number")
        n = int(input())
        if n == 1:
            lookUpPapers(lib)
        if n == 2:
            showFolders(lib)
        if n == 3:
            manageFolders(lib)
        if n == 4:
            managePapers(lib)
        if n==5:
            mostRecentSearch()
        if n==6:
            numberOfSearches()


    saveLib(lib)

    print("BYE :O")
