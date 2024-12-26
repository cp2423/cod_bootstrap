import os
import requests
import time


PWD = os.path.dirname(__file__)

missing = """
31829_B016765.tar.xz
31829_B016766.tar.xz
31829_B016767.tar.xz
31829_B016768.tar.xz
31829_B016769.tar.xz
31829_B016770.tar.xz
31829_B016771.tar.xz
31829_B016772.tar.xz
31829_B034746.tar.xz
31829_B034747.tar.xz
31829_B034748.tar.xz
31829_B034749.tar.xz
"""

def get_volumes_meta():
    with open(os.path.join(PWD, "volumes.txt")) as f:
        pairs = [line.split() for line in f.readlines()]
        return dict(pairs)

meta = get_volumes_meta()

url_stub = "https://central.bac-lac.canada.ca/.item/?op=jpg&app=microform&id="

# skip empty first line
for f in missing.splitlines()[1:]:
    time.sleep(2)
    vol = f[:13]
    pages = int(meta[vol])
    print(vol, pages)
    page_ids = [f"{vol}-{x:05d}" for x in range(pages)]
    for page_id in page_ids:
        url = f"https://central.bac-lac.canada.ca/.item/?op=jpg&app=microform&id={page_id}"
        resp = requests.get(url)

        if resp.status_code == 200:
            target = os.path.join(PWD, page_id + ".jpg")
            with open(target, "wb") as f:
                f.write(resp.content)
        else:
            # dunno what happened
            print(f"{url} failed with status code {resp.status_code}")