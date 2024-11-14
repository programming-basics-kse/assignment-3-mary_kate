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
                    #output(name, event, medal)
                if counter < 10:
                    counter += 1
                    print(f"{name}; {event}; {medal}")

            next_line = file.readline()
            next_line = next_line.rstrip('\n')
            next_line = next_line.split('\t')

        print(f"Gold: {medals_list['Gold']}\nSilver: {medals_list['Silver']}\nBronze: {medals_list['Bronze']}")

# def output():
#     pass
#
# def total():
#     pass
#
# def overall():
#     pass
#
# def interactive():
#     pass

# -medals, -output, -total, -overall, -interactive
parser = argparse.ArgumentParser()

parser.add_argument("-medals", nargs=2, help="input Team name and year of olympiad")
parser.add_argument("-output", help="Name of the file were output will be saved")
args = parser.parse_args()

if args.medals:
    team, year = map(str, args.medals)
    output_file = args.output
    medals(team, year)

