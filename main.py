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
                    if args.output:
                        output(name, event, medal,None, output_file)

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


# def total():
#     pass
#
# def overall():
#     pass
#
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

        print(f"Перша участь: {first_year} у {first_city}")
        if most_successful:
            print(f"Найуспішніша олімпіада: {most_successful[0]} ({sum(most_successful[1].values())} медалей)")
        if least_successful:
            print(f"Найневдаліша олімпіада: {least_successful[0]} ({sum(least_successful[1].values())} медалей)")
        else:
            print("Усі олімпіади для цієї країни були успішними.")
        print(f"Середня кількість медалей: Gold: {average_gold}, Silver: {average_silver}, Bronze: {average_bronze}")


# -medals, -output, -total, -overall, -interactive
parser = argparse.ArgumentParser()

parser.add_argument("-medals", nargs=2, help="input Team name and year of olympiad")
parser.add_argument("-output", help="Name of the file were output will be saved")
parser.add_argument("-interactive", action="store_true", help="Запустити інтерактивний режим")

args = parser.parse_args()

if args.medals:
    team, year = map(str, args.medals)
    output_file = args.output
    medals(team, year)

if args.interactive:
    interactive()


