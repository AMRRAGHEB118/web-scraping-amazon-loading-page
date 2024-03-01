from requests import get
from bs4 import BeautifulSoup
import csv


def get_soup_instance(date):
    response = get(f'https://www.yallakora.com/match-center/مركز-المباريات?date={date}#')
    src = response.content
    soup = BeautifulSoup(src, 'lxml')

    return soup

def get_championship_names(championships):
    championshipNames = []
    for championship in championships:
            championshipName = championship.find('div', {'class': 'title'}).find('h2').text.strip()
            championshipNames.append(championshipName)

    return championshipNames


def main():
    matchesDetails = []
    championshipNames = []
    try:
        date = input('Enter date in YYYY/MM/DD format: ')
        soup = get_soup_instance(date)

        matchesCenter = soup.find('section', {'class': 'matchesCenter'})
        championships = matchesCenter.find_all('div', {'class': 'matchesList'})

        championshipNames = get_championship_names(championships)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

