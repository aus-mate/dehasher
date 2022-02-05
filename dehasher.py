#!/usr/bin/python3
import requests
import argparse
import json
import csv

parser = argparse.ArgumentParser(description="Query DeHashed API and dump data to disk")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-q', dest='query', help='API query to execute, e.g. "-q google.co.uk"')
parser.add_argument('-o', dest="output_file", help='Name to use for output files, e.g. "-o dump" will output dump.json & dump.csv', required=True)
group.add_argument('-i', dest='input_file', help='Input JSON file for if not wanting to perform an API query (used for testing purposes to avoid spending API credits)')
args = parser.parse_args()

api_endpoint = "https://api.dehashed.com/search?query="

def are_we_done(dump, page):
    print("API credits remaining: " + str(dump['balance']))
    result_count = 0
    for i in dump['entries']:
        result_count += 1
    if (result_count == 10000) and (page != 3):
        return False
    else:
        return True

def apiReq(target, page, auth):
    return json.loads(requests.get(target + "&size=10000&page=" + str(page), headers = {"Accept": "application/json"}, auth = auth).text)

def query_api():
    api_user = input("Enter dehashed email address: ")
    api_key = input("Enter dehashed API key: ")
    target = api_endpoint + args.query + "&size=10000&page="
    auth = (api_user, api_key)
    print("\nQuerying dehashed API...")
    for page in range(1, 4):
        dump = apiReq(target, page, auth)
        if page == 1:
            fulldump = dump
        else:
            fulldump["entries"].extend(dump["entries"])
        if are_we_done(dump, page):
            print("Finished!")
            break
        else:
            print("Paginating...")           
    print("\nWriting JSON file: " + args.output_file + ".json")
    with open(args.output_file + ".json", 'w') as outfile:
        json.dump(fulldump, outfile)
    parse_to_csv(fulldump)

def parse_to_csv(fulldump):
    results = []
    for i in fulldump['entries']:
        if i['email'] != None and i['email'] != "":
            results.append([i['email'], i['password'], i['hashed_password'], i['database_name']])
    export_csv(results)

def export_csv(results):
    results.insert(0,["Email Address", "Password", "Hash", "Database"])
    print("Writing CSV file: " + args.output_file + ".csv")
    with open(args.output_file + ".csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(results)

def main():
    if args.query:
        query_api()
    elif args.input_file:
        with open(args.input_file, "r") as infile:
            parse_to_csv(json.load(infile))

if __name__ == "__main__":
    main()