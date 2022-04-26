import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title","company","location","link"])
  
  for j in jobs:
    for i in j:
      writer.writerow(list(i.values()))