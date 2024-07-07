import requests
from bs4 import BeautifulSoup
import csv

date = input("please enter the date in the following format MM/DD/YY")
page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#")

def main(page):
    src = page.content
    soup = BeautifulSoup(src,"lxml")
    match_details=[]
    
    championchips = soup.find_all("div",{'class':'matchCard'})
    
    def get_match_info(championchips):
            
            # get championship title
            championchip_title = championchips.contents[1].find('h2').text.strip()
            all_matches = championchips.contents[3].find_all('div',{'class':'teamCntnr'})
            number_of_matches= len(all_matches)

            for i in range (number_of_matches):
            # get teams
                teamA = all_matches[i].find('div',{'class':'teamA'}).find('p').text.strip()
                teamB = all_matches[i].find('div',{'class':'teamB'}).find('p').text.strip()
            
            # get results    
                match_result = all_matches[i].find('div' , {'class':'MResult'}).find_all('span' , {'class':'score'}) 
                score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}" 
                print(score)

            # get time 
                match_time = all_matches[i].find('span',{'class':'time'}).text.strip()

            # put all info in match_details   
                match_details.append({"نوع البطولة":championchip_title,"الفريق الاول":teamA,"الفريق الثاني":teamB,"موعد المباراة":match_time,"النتيجة":score})

    for i in range(len(championchips)) :       
     get_match_info(championchips[i])        

    # use csv file     
    keys = match_details[0].keys()
    with open ('D:\FCDS\Data Scraping\yallakora.csv','w') as output_file:
     dict_writer = csv.DictWriter(output_file, keys)
     dict_writer.writeheader()
     dict_writer.writerows(match_details)
     print("file created")

main(page)    