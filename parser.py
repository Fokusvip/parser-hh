from bs4 import BeautifulSoup
import requests
import unicodedata
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 YaBrowser/20.7.0.894 Yowser/2.5 Safari/537.36'
}

def get_page_data(html):       
    r = requests.get(html, headers = headers)
    soup = BeautifulSoup(r.text, 'lxml')
    all_vacancy = soup.find('div', {'class':'vacancy-serp'})
    vacancy = []


    for r in all_vacancy:
        v1 = vacancy_title = r.find('span', {'class': 'resume-search-item__name'})
        v2 = vacancy_salary = r.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if v1 and v2:
            vacancy.append({
                'Вакансия': v1.string,
                'Зарплата': unicodedata.normalize('NFKD', v2.string)
            })
        else:
            continue
   
    for vac in vacancy:
        print(vac)


def getLastPage(url):
    respones = requests.get(url,headers=headers)
    soup = BeautifulSoup(respones.text,'lxml')
    id = soup.find('div', {'data-qa':'pager-block'})
    pages = id.find('a', {'class': 'HH-Pager-Controls-Next'})
    last = pages.find_previous('a',{'data-qa': 'pager-page'})
    
    return int(str(last.text))

def main():
    url = 'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&fromSearch=true'
    lastPage = getLastPage(url)
    for x in range(1,lastPage + 1):
        url = f'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&fromSearch=true&page={x}'
        print(url)
        get_page_data(url)

if __name__ == '__main__':
    main()