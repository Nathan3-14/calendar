from betterjson import BetterJson

data = BetterJson("data.json")

for date in ["01/01", "02/01", "03/01", "04/01", "05/01"]:
    for exam in data.get(f"exams.{date}"):
        print(f"{date} {exam['name']}")
    print("")
    