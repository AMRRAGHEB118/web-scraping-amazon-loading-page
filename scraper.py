import datetime
from requests import get
from bs4 import BeautifulSoup
import csv


def getSoupInstance(date):
    response = get(f'https://www.yallakora.com/match-center/مركز-المباريات?date={date}#')
    src = response.content
    soup = BeautifulSoup(src, 'lxml')

    return soup

def getChampionshipNames(championships):
    championshipNames = []
    for championship in championships:
            championshipName = championship.find('div', {'class': 'title'}).find('h2').text.strip()
            championshipNames.append(championshipName)

    return championshipNames

def getMatchesDetails(championships, championshipNames):
    matchesDetails = []
    matchDetails = {}
    for championship, championshipName in zip(championships, championshipNames):
        matches = championship.find_all('div', {'class': 'item'})

        for match in matches:
            matchDetails = getMatchDetails(match, championshipName)
            matchesDetails.append(matchDetails)

    return matchesDetails


def getMatchDetails(match, championshipName):
    matchDetails = {}
    matchDetails['championshipName'] = championshipName
    matchAllDataContainer = match.find('div', {'class': 'allData'})
    matchDetails['channel'] = matchAllDataContainer.find('div', {'class': 'channel icon-channel'})
    if matchDetails['channel'] is not None:
        matchDetails['channel'] = matchDetails['channel'].text.strip()
    topData = matchAllDataContainer.find('div', {'class': 'topData'})


    matchDetails['round'] = topData.find('div', {'class': 'date'}).text.strip()
    matchDetails['status'] = topData.find('div', {'class': 'matchStatus'}).text.strip()
    teamsData = matchAllDataContainer.find('div', {'class': 'teamCntnr'}).find('div', {'class': 'teamsData'})
    matchDetails['homeTeam'] = teamsData.find('div', {'class': 'teams teamA'}).find('p').text.strip()
    matchDetails['awayTeam'] = teamsData.find('div', {'class': 'teams teamB'}).find('p').text.strip()
    scores = teamsData.find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
    matchDetails['homeTeamScore'] = scores[0].text.strip()
    matchDetails['awayTeamScore'] = scores[1].text.strip()
    matchDetails['time'] = teamsData.find('span', {'class': 'time'}).text.strip()

    return matchDetails


def createCsvFile(date, matchesDetails, headers):
    filename = f'matches-{date.replace("/", "-")}.csv'
    try:
        with open(filename, 'w', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(matchesDetails)
            print(f'File {filename} created successfully!')
    except FileNotFoundError:
        print(f"Error: Directory containing the file doesn't exist. Please create it manually.")


def main():
    matchesDetails = []
    championshipNames = []
    headers = ['championshipName', 'channel', 'round', 'status', 'homeTeam', 'awayTeam', 'homeTeamScore', 'awayTeamScore', 'time']
    try:
        date = input('Enter date in YYYY/MM/DD format: ')
        soup = getSoupInstance(date)

        matchesCenter = soup.find('section', {'class': 'matchesCenter'})
        championships = matchesCenter.find_all('div', {'class': 'matchesList'})

        championshipNames = getChampionshipNames(championships)

        matchesDetails = getMatchesDetails(championships, championshipNames)

        createCsvFile(date, matchesDetails, headers)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

