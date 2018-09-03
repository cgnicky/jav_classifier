import cfscrape
import bs4
import os
import shutil

# curPath = os.getcwd()
curPath = "/DATA/Downloads/Media/"
source = os.listdir(curPath)


# for tag in soup.find_all(True):
#    print(tag.name)

def getActorName(titleName):
    scraper = cfscrape.create_scraper()

    response = scraper.get("http://www.javlibrary.com/en/vl_searchbyid.php?keyword={}".format(titleName))
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    if validateSearchResult(soup) is True:
        if not soup.find("div", class_="videos"):
            if soup.find("span", class_="star"):
                actorName = soup.find("span", class_="star").text
                return actorName
            else:
                print("Empty actor name! Move to others...")
                return "Others"
        else:
            link = soup.find("div", class_="video").find("a", {"title": lambda x: x and x.startswith(titleName)}).attrs[
                'href']
            nextPage = scraper.get("http://www.javlibrary.com/en/{}".format(link[2:len(link)]))
            soup2 = bs4.BeautifulSoup(nextPage.content, "html.parser")
            actorName = soup2.find("span", class_="star").text
            return actorName
    else:
        print("Failed to identify! Move to others...")
        return "Others"


def checkAndCreateDirectory(filePath):
    print("Checking Directory exists or not...")
    if os.path.exists(filePath) is True:
        print("Directory existed !")
    else:
        print("Create a new directory...")
        try:
            os.mkdir(filePath)
        except OSError:
            print("Creation of the directory %s failed" % filePath)
        else:
            print("Successfully created the directory %s " % filePath)


def moveFile(file, dest):
    print("Moving {} to {}...".format(file, dest))
    shutil.move(file, dest)


def validateSearchResult(content):
    if content.find("div", id="badalert"):
        print("Invalid format of search keyword!")
        return False
    elif content.find("em"):
        print("No result found!")
        return False
    else:
        return True


def filenameFix(filename):
    if filename.endswith("C"):
        return filename[:len(filename)-2]
    else:
        return filename


for file in source:
    print(file)
    if len(file.split(".")) <= 2:
        try:
            title, ext = file.split(".")
            title = filenameFix(title)
            if file.endswith(".mp4"):
                print("Moving MP4 files...")
                dest = curPath + getActorName(title)
                src = curPath + file
                checkAndCreateDirectory(dest)
                moveFile(src, dest)
            elif file.endswith(".avi"):
                print("Moving AVI files...")
                dest = curPath + getActorName(title)
                src = curPath + file
                checkAndCreateDirectory(dest)
                moveFile(src, dest)
            else:
                print("Extension not supported!")
        except ValueError:
            print("Not a media file, skipped...")
    else:
        print("Invalid extension format!")
print("Process Successfully !!")
