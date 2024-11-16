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
                if output_file and counter < 10:
                    output(name, event, medal,None, output_file)
                if counter < 10:
                    counter += 1
                    print(f"{name}; {event}; {medal}")

            next_line = file.readline()
            next_line = next_line.rstrip('\n')
            next_line = next_line.split('\t')

        print(f"Gold: {medals_list['Gold']}\nSilver: {medals_list['Silver']}\nBronze: {medals_list['Bronze']}")
        output(name, event, medal,medals_list, output_file)


def output(name, event, medal,medals_list, output_file):
    with open(output_file, "a") as file:
        if name and event and medal:
            file.write(f"{name}; {event}; {medal}\n")
        if medals_list:
            file.write(f"Gold: {medals_list['Gold']}\n")
            file.write(f"Silver: {medals_list['Silver']}\n")
            file.write(f"Bronze: {medals_list['Bronze']}\n")


# def total():
#     pass
#
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

# def interactive():
#     pass

# -medals, -output, -total, -overall, -interactive
parser = argparse.ArgumentParser()

parser.add_argument("-medals", nargs=2, help="input Team name and year of olympiad")
parser.add_argument("-output", help="Name of the file were output will be saved")
parser.add_argument("-overall", nargs="+",help="List of countries")
args = parser.parse_args()

if args.medals:
    team, year = map(str, args.medals)
    output_file = args.output
    medals(team, year)
if args.overall:
    overall(args.overall)

