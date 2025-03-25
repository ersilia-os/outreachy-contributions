import subprocess
import time

subprocess.run(["ersilia", "fetch", "eos2gw4"], check=True)


server = subprocess.Popen(["ersilia", "serve", "eos2gw4"])
time.sleep(10)

subprocess.run(["ersilia", "run", "-i", "./data/bioavailability.csv", "-o", "./data/featurised_bioavailability.csv"], check=True)

print("featurisation completed, output saved as featurised_bioavailability.csv in data/")

server.terminate()


