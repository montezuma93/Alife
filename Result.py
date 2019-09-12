import csv
import os

for config in range(10):
    for result in range(5):
        file_to_check = './Config'+str(config)+'-'+str(result)+'-results.csv'
        print(file_to_check)
        if os.path.isfile(file_to_check):
            if result > 0:
                print("here")
                rows_to_append = []
                with open(file_to_check, "r", encoding="utf-8", errors="ignore") as scraped:
                    reader = csv.reader(scraped, delimiter=';')
                    for row in reader:
                        if row:  # avoid blank lines
                            row_to_append = row
                            row_to_append[0]=result+1
                            rows_to_append.append(row_to_append)
                scraped.close
                os.remove(file_to_check)
                with open('Config' + str(config) + '-0-results.csv', 'a', newline='') as csvFile:
                    writer = csv.writer(csvFile, delimiter =";")
                    writer.writerows(rows_to_append)
                csvFile.close()