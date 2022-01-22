import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["website", "title", "company", "location", "link", "worktime","pay","tag"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return