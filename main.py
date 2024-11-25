import argparse
from player_class import Player

def player_list():
    players = []

    with open("Olympic Athletes - athlete_events.tsv", "r") as file:
        header = file.readline().rstrip('\n').split('\t')

        NAME = header.index("Name")
        YEAR = header.index("Year")
        TEAM = header.index("Team")
        NOC = header.index("NOC")
        EVENT = header.index("Event")
        CITY = header.index("City")
        MEDAL = header.index("Medal")

        line = file.readline()

        while line:
            line = line.rstrip('\n')
            line = line.split('\t')
            if line[MEDAL] != 'NA':
                players.append(Player(line[NAME], line[TEAM], line[NOC], line[YEAR], line[CITY], line[EVENT], line[MEDAL]))
            line = file.readline()

    return players

def medals(team, year):

    medals_list = {'Gold': 0, 'Silver': 0, 'Bronze': 0}

    counter = 0
    for player in players:
        if (player.team == team or player.noc == team) and player.year == year:
            name = player.name
            event = player.event
            medal = player.medal

            medals_list[medal] += 1
            if counter < 10:
                counter += 1
                print(f"{name}; {event}; {medal}")
                if args.output:
                    output(name, event, medal, None, output_file)

    print(f"Gold: {medals_list['Gold']}\nSilver: {medals_list['Silver']}\nBronze: {medals_list['Bronze']}")
    if args.output:
        output(name, event, medal, medals_list, output_file)

def output(name, event, medal,medals_list, output_file):

    with open(output_file, "a") as file:
        if name and event and medal:
            file.write(f"{name}; {event}; {medal}\n")
        if medals_list:
            file.write(f"Gold: {medals_list['Gold']}\n")
            file.write(f"Silver: {medals_list['Silver']}\n")
            file.write(f"Bronze: {medals_list['Bronze']}\n")


def total(year):
    countries = {}

    for player in players:
        if player.year == year:
            if player.noc not in countries:
                countries[player.noc] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            countries[player.noc][player.medal] += 1

    for country, medal in countries.items():
        print(f"{country}, Gold: {medal["Gold"]}, Silver: {medal["Silver"]}, Bronze: {medal["Bronze"]}")


def overall(countries):
    country_medals = {}
    for country in countries:
        country_medals[country] = {}

    for player in players:
        for country in countries:
            if player.team == country or player.noc == country:
                if player.year not in country_medals[country]:
                    country_medals[country][player.year] = 0
                country_medals[country][player.year] += 1

    for country in countries:
        if country_medals[country]:
            max_year = max(country_medals[country], key=country_medals[country].get)
            max_medals = country_medals[country][max_year]
            print(f"{country}. Year with most medals - {max_year}, total - {max_medals}")
        else:
            print(f"No medals data for {country}")


def interactive():

    while True:
        country = input("Enter a name or code of country: ")

        if country == 'exit':
            return None

        country_players = []
        for player in players:
            if player.team == country or player.noc == country:
                country_players.append(player)

        if not country_players:
            print(f"No data found for country: {country}")
            continue

        first_year, first_city = None, None
        for player in country_players:
            if first_year is None or int(player.year) < int(first_year):
                first_year, first_city = player.year, player.city

        medals_by_year = {}
        for player in country_players:
            if player.year not in medals_by_year:
                medals_by_year[player.year] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
            medals_by_year[player.year][player.medal] += 1

        most_successful, least_successful = None, None
        for year, counts in medals_by_year.items():
            total = sum(counts.values())
            if most_successful is None or total > sum(most_successful[1].values()):
                most_successful = (year, counts)
            if least_successful is None or (total < sum(least_successful[1].values()) and total > 0):
                least_successful = (year, counts)

        total_years = len(medals_by_year)
        total_gold, total_silver, total_bronze = 0, 0, 0
        for counts in medals_by_year.values():
            total_gold += counts['Gold']
            total_silver += counts['Silver']
            total_bronze += counts['Bronze']

        average_gold = round(total_gold / total_years if total_years > 0 else 0)
        average_silver = round(total_silver / total_years if total_years > 0 else 0)
        average_bronze = round(total_bronze / total_years if total_years > 0 else 0)

        print(f"First participation: {first_year} у {first_city}")
        if most_successful:
            print(f"The most successful Olympiad: {most_successful[0]} ({sum(most_successful[1].values())} medals)")
        if least_successful:
            print(f"The most unsuccessful Olympics: {least_successful[0]} ({sum(least_successful[1].values())} medals)")
        else:
            print("All the Olympiads were successful for this country.")
        print(f"Average number of medals: Gold: {average_gold}, Silver: {average_silver}, Bronze: {average_bronze}")


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-medals", nargs=2, help="input Team name and year of olympiad")
parser.add_argument("-output", help="Name of the file were output will be saved")
group.add_argument("-total", help="Year of olympiad, will give you countries with medals")
group.add_argument("-overall", nargs="+",help="List of countries")
group.add_argument("-interactive", action="store_true", help="Запустити інтерактивний режим")
args = parser.parse_args()

players = player_list()

if args.medals:
    team, year = map(str, args.medals)
    output_file = args.output
    medals(team, year)

if args.overall:
    overall(args.overall)

if args.total:
    total(args.total)

if args.interactive:
    interactive()
