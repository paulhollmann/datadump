from csv import writer
import requests
from bs4 import BeautifulSoup
import csv
import argparse

"""
    CSV Columns
"""
DEP=3
ARR=4
ROUTE=5
REMARKS=6
URL="https://grd.aero-nav.com/"
CALLSIGN=7

"""
    format_url returns formated GRD URL
"""

def format_url(dep, arr):
    return f"{URL}?From={dep}&To={arr}"

"""
    Create file argument
"""
parser = argparse.ArgumentParser()
parser.add_argument("-file", "--file", type=str, required=False, default=None)
args = parser.parse_args()

"""
    Check is file argument empty. If it is show the error and exit
"""

if args.file == None:
    print("File not specified.")
    exit()

with open(args.file) as csvfile, open(f"1_{args.file}", 'w') as w:
    flights = csv.reader(csvfile, delimiter=',')

    results = csv.writer(w, delimiter=',')

    for flight in flights:
        page = requests.get(f"{format_url(flight[DEP], flight[ARR])}")
        soup = BeautifulSoup(page.content, 'html.parser')

        route = soup.find(id="Route0")

        if route:
            flight[ROUTE] = route.get_text()
            results.writerow(flight)
            print(f"Added route for {flight[CALLSIGN]}")

        else:
            results.writerow(flight)
            print("Not Found")