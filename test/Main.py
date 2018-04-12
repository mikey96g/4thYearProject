import csv

#Open/Create a file to append data
with open('Data123.csv', 'a', newline='') as csvFile:
    #Use csv Writer
    fieldnames = ['ID', 'Tweet']
    csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    csvWriter.writeheader()