#majd anas 0234815
from storage import toCSV


class Paper:

    def __init__(
        self,
        title="",
        result_id="",
        link="",
        snippet="",
        totalCitations="",
        citation="",
        authors=None,
    ):
        self.title = title
        self.result_id = result_id
        self.link = link
        self.snippet = snippet
        self.totalCitations = totalCitations
        self.citation = citation
        self.authors = authors if authors is not None else []

    def showPaperInfoMore(self):
        print(
            f"title: {self.title}\nlink: {self.link}\nsnippet:{self.snippet}\ntotla number of citations: {self.totalCitations}\nCitation: {self.citation}"
        )
        print(f"authors:")
        print("[")
        for author in self.authors:
            print(
                f"name: {author.name} id:{author.authorId} profile:{author.profileLink}"
            )
        print("]")
        print(f"result_id: {self.result_id}")

    def showPaperInfoLess(self):
        print(
            f"title: {self.title}\ntotla number of citations: {self.totalCitations}\nCitation: {self.citation}"
        )
        print(f"authors:")
        print("[")
        for author in self.authors:
            print(
                f"name: {author.name} id:{author.authorId} profile:{author.profileLink}"
            )
        print("]")
        print(f"result_id: {self.result_id}")

    def __gt__(self, other):
        if not isinstance(other, Paper):
            return NotImplemented
        return self.citation > other.citation

    def authorsAsString(self):
        str = ""
        for author in self.authors:
            str += author.toString() + " "
        return str


class Author:
    def __init__(self, name="", authorId="", profileLink=""):
        self.name = name
        self.authorId = authorId
        self.profileLink = profileLink

    def toString(self):
        return f"Name:{self.name} Id:{self.authorId} Link:{self.profileLink}\t"


class Folder:
    def __init__(self, title="", papers=None):
        self.title = title
        self.papers = papers if papers is not None else []

    def sortPapersByCitation(self):
        self.papers.sort()

    def showPapers(self):
        for i, paper in enumerate(self.papers):
            print(
                f"==================================\n{i+1}=================================="
            )
            paper.showPaperInfoLess()

    def showPapersTitles(self):
        for paper in self.papers:
            print(paper.title)
            print(f"===============================================")

    def getPaper(self, title):
        found = False
        for paper in self.papers:
            if paper.title == title:
                found = True
                paper.showPaperInfoMore()

        if not found:
            print("paper not found")
            return False

    def paperInFolder(self, title):
        for paper in self.papers:
            if paper.title == title:
                return True
        return False

    def deletePaper(self, title):
        index = -1
        for i, paper in enumerate(self.papers):
            if paper.title == title:
                index = i
        if index != -1:
            self.papers.pop(index)
            return True
        else:
            return False

    def addPaper(self, paper):
        self.papers.append(paper)

    def storeFolderItemsToCSV(self):
        #  def __init__(self,title="",result_id="",typeOFfile="",link="",snippet="",totalCitations="",citation="",authors=[]):
        data = [["title", "total citations", "link", "snippet", "authors"]]
        for paper in self.papers:
            a = [
                paper.title,
                paper.totalCitations,
                paper.link,
                paper.snippet,
                paper.authorsAsString(),
            ]

            data.append(a)

        toCSV(data, self.title)

    def renameFolder(self, newTitle):
        self.title = newTitle


class Library:

    def __init__(self, title, folders=None):
        self.title = title
        self.folders = folders if folders is not None else {}

    def showFolders(self):
        if len(self.folders) == 0:
            print("No folders")
            return
        for key, value in self.folders.items():
            print(f"title: {key}")

    def deleteFolder(self, title):
        if title in self.folders:
            del self.folders[title]
            print("folder deleted")
        else:
            print("no folder with this name")

    def addFolder(self, folder):
        self.folders.update({folder.title: folder})
        return folder

    def getFolder(self, title):
        return self.folders[title]

    def folderInLibrary(self, title):
        if title in self.folders:
            return True
        return False

    def renameFolder(self, title, newTitle):
        folder = self.getFolder(title)
        folder.renameFolder(newTitle)
        del self.folders[title]
        self.addFolder(folder)
