import argparse
import csv

# def medals():
#     pass
#
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

medals = args.medals
output_file = args.output
print(args)
print(medals, output_file)

