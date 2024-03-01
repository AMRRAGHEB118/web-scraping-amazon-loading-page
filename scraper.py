import requests
from bs4 import BeautifulSoup
import csv


def getSoupInstance(date):
    response = requests.get(f'https://www.yallakora.com/match-center/مركز-المباريات?date={date}#')
    response.raise_for_status()
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
    filename = f'csv/matches-{date.replace("/", "-")}.csv'
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=headers)
            writer.writeheader()

            if len(matchesDetails) == 0:
                print('No matches found for the selected date.')
                writer.writerow({'championshipName': 'No matches', 'channel': 'No matches', 'round': 'No matches', 'status': 'No matches', 'homeTeam': 'No matches', 'awayTeam': 'No matches', 'homeTeamScore': 'No matches', 'awayTeamScore': 'No matches', 'time': 'No matches', })
            else:
                writer.writerows(matchesDetails)

            csvFile.close()
            print(f'File {filename} created successfully!')
    except FileNotFoundError:
        print(f"Error: Directory containing the file doesn't exist. Please create it manually.")


def main():
    matchesDetails = []
    championshipNames = []
    resDate = ''
    headers = ['championshipName', 'channel', 'round', 'status', 'homeTeam', 'awayTeam', 'homeTeamScore', 'awayTeamScore', 'time']
    try:
        date = input('Enter date in MM/DD/YYYY format: ')

        if not date:
            raise ValueError('Date cannot be empty')
        if len(date.split('/')) != 3:
            raise ValueError('Date must be in MM/DD/YYYY format')

        soup = getSoupInstance(date)

        matchesCenter = soup.find('section', {'class': 'matchesCenter'})

        matchCenterDays = matchesCenter.find('div', {'class': 'matchCenterDays'})

        resDate = matchCenterDays.find('button', {'class': 'active'})['date']

        championships = matchesCenter.find_all('div', {'class': 'matchesList'})

        championshipNames = getChampionshipNames(championships)

        matchesDetails = getMatchesDetails(championships, championshipNames)

        createCsvFile(resDate, matchesDetails, headers)
    except ValueError as e:
        print(e)
    except requests.exceptions.RequestException as e: 
        print(e)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

