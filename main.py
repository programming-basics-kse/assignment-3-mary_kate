import argparse

# -medals, -output, -total, -overall, -interactive
parser = argparse.ArgumentParser()

parser.add_argument("medals", help="top-10 athlete in ____ year")
args = parser.parse_args()
print(args.medals)

