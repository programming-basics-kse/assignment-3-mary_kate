import argparse

def medals(team, year):

    medals_list = {'Gold': 0, 'Silver': 0, 'Bronze': 0}

    with open("Olympic Athletes - athlete_events.tsv", "r") as file:
        header = file.readline().rstrip('\n').split('\t')

        YEAR = header.index("Year")
        TEAM = header.index("Team")
        NOC = header.index("NOC")
        NAME = header.index("Name")
        EVENT = header.index("Event")
        MEDAL = header.index("Medal")

        next_line = file.readline()
        next_line = next_line.rstrip('\n')
        next_line = next_line.split('\t')

        counter = 0
        while next_line != ['']:
            if (next_line[TEAM] == team or next_line[NOC] == team) and next_line[YEAR] == year and next_line[MEDAL] != "NA":
                name = next_line[NAME]
                event = next_line[EVENT]
                medal = next_line[MEDAL]

                medals_list[medal] += 1
                if counter < 10:
                    counter += 1
                    print(f"{name}; {event}; {medal}")
                    if args.output:
                        output(name, event, medal, None, output_file)

            next_line = file.readline()
            next_line = next_line.rstrip('\n')
            next_line = next_line.split('\t')

        print(f"Gold: {medals_list['Gold']}\nSilver: {medals_list['Silver']}\nBronze: {medals_list['Bronze']}")
        if args.output:
            output(name, event, medal,medals_list, output_file)

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

    with open("Olympic Athletes - athlete_events.tsv", "r") as file:
        header = file.readline().rstrip('\n').split('\t')

        YEAR = header.index("Year")
        NOC = header.index("NOC")
        MEDAL = header.index("Medal")

        next_line = file.readline()

        while next_line:
            next_line = next_line.rstrip('\n')
            next_line = next_line.split('\t')

            if next_line[YEAR] == year and next_line[MEDAL] != "NA":
                if next_line[NOC] not in countries:
                    countries[next_line[NOC]] = {"Gold": 0, "Silver": 0, "Bronze": 0}
                countries[next_line[NOC]][next_line[MEDAL]] += 1
            next_line = file.readline()

    for country, medal in countries.items():
        print(f"{country}, Gold: {medal["Gold"]}, Silver: {medal["Silver"]}, Bronze: {medal["Bronze"]}")

def overall(countries):
    country_medals = {}
    for country in countries:
        country_medals[country] = {}
    with open("Olympic Athletes - athlete_events.tsv", "r") as file:
        header = file.readline().rstrip('\n').split('\t')

        YEAR = header.index("Year")
        TEAM = header.index("Team")
        NOC = header.index("NOC")
        MEDAL = header.index("Medal")

        next_line = file.readline().rstrip('\n').split('\t')

        while next_line != ['']:
            year = next_line[YEAR]
            team = next_line[TEAM]
            noc = next_line[NOC]
            medal = next_line[MEDAL]

            for country in countries:
                if(team == country or noc == country) and medal !="NA":
                    country_medals[country][year] = country_medals[country].get(year,0)+1

            next_line = file.readline().rstrip('\n').split('\t')

        for country in countries:
            if country_medals[country]:
                max_year = max(country_medals[country], key=country_medals[country].get)
                max_medals = country_medals[country][max_year]
                print(f"{country}. Year with most medals - {max_year}, total - {max_medals}")
            else: print("No medals data")

def interactive():
    with open("Olympic Athletes - athlete_events.tsv", "r") as file:
        header = file.readline().rstrip('\n').split('\t')
        YEAR = header.index("Year")
        TEAM = header.index("Team")
        NOC = header.index("NOC")
        MEDAL = header.index("Medal")
        CITY = header.index("City")

        data = []
        for line in file:
            data.append(line.rstrip('\n').split('\t'))

    while True:
        country = input("Enter a name or code of country: ")

        if country == 'exit':
            return None

        country_data = []
        for row in data:
            if row[TEAM] == country or row[NOC] == country:
                country_data.append(row)

        if not country_data:
            print(f"No data found for country: {country}")
            continue

        first_year, first_city = None, None
        for row in country_data:
            if first_year is None or int(row[YEAR]) < int(first_year):
                first_year, first_city = row[YEAR], row[CITY]

        medals_by_year = {}
        for row in country_data:
            year, medal = row[YEAR], row[MEDAL]
            if medal != "NA":
                if year not in medals_by_year:
                    medals_by_year[year] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
                medals_by_year[year][medal] += 1

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


# -medals, -output, -total, -overall, -interactive
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-medals", nargs=2, help="input Team name and year of olympiad")
parser.add_argument("-output", help="Name of the file were output will be saved")
group.add_argument("-total", help="Year of olympiad, will give you countries with medals")
group.add_argument("-overall", nargs="+",help="List of countries")
group.add_argument("-interactive", action="store_true", help="Запустити інтерактивний режим")
args = parser.parse_args()

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
