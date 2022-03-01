import csv

def save_job_csv(job_list, file_name):
  file = open(f"{file_name}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Company", "Title", "Place", "Date", "Apply"])
  for job in job_list:
    del job["company_img"]
    writer.writerow(list(job.values()))