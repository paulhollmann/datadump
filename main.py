import requests
from bs4 import BeautifulSoup
import csv
import argparse

DEP=3
ARR=4
ROUTE=5
REMARKS=6
URL="https://grd.aero-nav.com/"
CALLSIGN=7

def format_url(dep, arr):
    return f"{URL}?From={dep}&To={arr}"

parser = argparse.ArgumentParser()
parser.add_argument("-file", "--file", type=str, required=False, default=None)
args = parser.parse_args()

if args.file == None:
    print("File not specified.")
    exit()

with open(args.file) as csvfile:
    flights = csv.reader(csvfile, delimiter=',')

    for flight in flights:
        page = requests.get(f"{format_url(flight[DEP], flight[ARR])}")
        soup = BeautifulSoup(page.content, 'html.parser')

        route = soup.find(id="Route0")

        if route:
            flight[ROUTE] = route.get_text()
            print(f"Added route for {flight[CALLSIGN]}")

        else:
            print("Not Found")