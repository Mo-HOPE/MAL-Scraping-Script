import requests
import csv
from bs4 import BeautifulSoup
from googlesearch import search
from os import path, path, mkdir


''' 
Created by: HØPE
Github user: Mo-HOPE

'''


def main():

    user_input()

    # Get Anime Main Name
    Anime_Name = soup.find("h1",{"class": "title-name"}).find("strong").text.strip()

    # Check For Alternative Name And Get It IF It Exist (print empty string if not)
    if (soup.find("p",{"class": "title-english"}) == None):
        Other_Name = ""
    else:
        Other_Name = soup.find("p",{"class": "title-english"}).text.strip()
    

    Anime_Information = soup.find_all("div",{"class": "spaceit_pad"}) # A list with all divs that contain anime informaion
    start_point = 0 
    
    # Determine the div we start from
    for i in range(len(Anime_Information)):
        if (Anime_Information[i].find("span").text.strip() == "Type:"):
            start_point = i
            break


    # divs with constant order in every anime type
    Anime_Type = Anime_Information[start_point].find("a").text.strip()
    Anime_Episodes = Anime_Information[start_point+1].contents[2].strip()
    Anime_Status = Anime_Information[start_point+2].contents[2].strip()
    Anime_Aired = Anime_Information[start_point+3].contents[2].strip()
    Anime_Premiered = Anime_Information[start_point+4].find("a").text.strip()


    # Determine a new start point for other divs depends on the anime type (order of divs change only in cases inside if condition)
    if ((Anime_Type == "OVA") or (Anime_Type == "ONA") or (Anime_Type == "Special") or (Anime_Type == "Movie")):
        new_start_point = start_point+6
        Anime_Premiered = Anime_Aired
    else:
        Anime_Premiered = Anime_Information[start_point+4].find("a").text.strip()
        new_start_point = start_point+8 
    

    # Determine anime studio with new start point
    Anime_Studio = "" 
    studios_list =  Anime_Information[new_start_point].find_all("a")
    for i in range(len(studios_list)):
        Anime_Studio = f"{Anime_Studio}, {studios_list[i].text.strip()}" 

    Anime_Studio = Anime_Studio[2:]

    # Determine anime source
    Anime_Source = Anime_Information[new_start_point+1].contents[2].strip()

    # Determine anime genres
    genre_list = Anime_Information[new_start_point+2].find_all("span",{"itemprop": "genre"})
    Anime_Genre = ""
    for i in range(len(genre_list)):
        Anime_Genre = f"{Anime_Genre}, {genre_list[i].text.strip()}"
    Anime_Genre = Anime_Genre[2:]


    # Determine anime rate
    Anime_Rate = ""
    for i in range(len(Anime_Information)):
        if (Anime_Information[i].find("span").text.strip() == "Rating:"):
              Anime_Rate = Anime_Information[i].contents[2].strip()
              break

    
    # List of one dictionary that contain the informations of the anime as values 
    Full_Info = [{"Name": Anime_Name, "Another Name": Other_Name,"Type": Anime_Type, 
                 "Episodes": Anime_Episodes, "Status": Anime_Status, "Aired": Anime_Aired,
                 "Premiered": Anime_Premiered, "Studio": Anime_Studio,"Source": Anime_Source, 
                 "Genres": Anime_Genre,"Rating": Anime_Rate},]

    
    # Determine file name with the same name of anime and remove invalid characters
    file_name = Anime_Name
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for i in invalid_chars:
        for j in file_name:
            if (j == i):
                file_name = file_name.replace(i,"")
    file_path = "D:/Work/Learn/Python/MAL Script/Results/"+file_name+".csv"

    # Create Results folder if not exist in the same script folder to store csv files
    code_file_directory = path.dirname(path.abspath(__file__))
    folder_path = path.join(code_file_directory, "Results")

    if not path.exists(folder_path):
        mkdir(folder_path)
    
    # create the csv file and but the keys and values of dic in it
    with open(file_path,'w', encoding="utf-8-sig") as final_file:
        keys = Full_Info[0].keys()
        dict_writer = csv.DictWriter(final_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(Full_Info)
        
        
        print("File Created Successfully") #end of the program


def user_input():

    while True:
        anime_checker = "https://myanimelist.net/anime/"
        user_choise =input("Press 1 if you want to write anime name and press 2 if you want to write url diractly: ")
        
        if (user_choise == "1"):
            print("Write anime name (prefer the main name) and the number of seasons if exist ..\n for example: boku no hero academia season 6")
            query = input("Enter the name: ")
            query = query+" mal"
            print(f"Searching for '{query}' on Google ...")
            url = ""
            for index, url in enumerate(search(query, num_results=1)):
                    if index == 0:
                        break
            if (url[0:30] == anime_checker):
                break
        
            else:
                print("The name you enter is not an anime on mal please check the anime name or enter the url directly ...")   
        
        
        elif(user_choise == "2"):
            url = input("enter the url please: ")
            if (url[0:30] == anime_checker):
                break
        
            else:
                print("The URL you enter is not a URL of anime page on mal please check the url and write it again ...")   
        
        
        else:
            print("please press only 1 or 2")
            continue
    url_checker(url)


def url_checker(url):
    valid = 0
    try:    
        response = requests.get(url)
        if (response.status_code == 200):
            print(f"Request successful: {response.status_code}")
            valid = 1
            set_page(valid,url)
        elif (response.staus_code == 400):
            print(f"Bad request: {response.status_code}")
        elif (response.status_code == 401):
            print(f"Unauthorized: {response.status_code}")
        elif (response.status_code == 403):
            print(f"Forbidden: {response.status_code}")
        elif (response.status_code == 404):
            print(f"Not found: {response.status_code}")
        elif (response.status_code == 429):
            print(f"Too many requests: {response.status_code}")
        else:
            print(f"An error occurred: {response.status_code}")    
    except: 
        set_page(valid,url)


def set_page(valid,url):
    global soup
    if (valid):
        page = requests.get(url)
        src = page.content
        soup = BeautifulSoup(src, "lxml")
        return soup

    else:
        print("there is a problem with the site server, please try again and check the website ")    
        user_input()


if __name__ == "__main__":
    main()


''' 
Created by: HØPE
Github user: Mo-HOPE

'''    