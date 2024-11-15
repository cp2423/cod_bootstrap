import os
import requests

FOLDER = "/Users/chris/Dev/cod_records/aws/extracted/"
vol = '31829_B016737'

i = -1
images = [fp for fp in os.scandir(FOLDER + vol)]
images.sort(key=lambda fp: fp.name)

for fp in images:
    i += 1
    no = fp.name[14:19]
    if i != int(no):
        print(fp)
        break

print(i)
padded = str(i).zfill(5)
target_filename = f"{FOLDER}{vol}/{vol}-{padded}.jpg"
print(target_filename)
exists = (os.path.exists(target_filename))
print(exists)

if not exists:
    url = f"https://central.bac-lac.gc.ca/.item/?op=img&app=microform&id={vol}-{padded}"
    print(url)
    resp = requests.get(url)
    with open(target_filename, 'wb') as fh:
        fh.write(resp.content)
    print("Downloaded :)")