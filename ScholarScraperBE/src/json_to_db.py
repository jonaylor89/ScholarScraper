from entities.entity import Session, Base, engine
from entities.scholar import Scholar, ScholarSchema

import json

data = None

with open("scraper/data.json") as f:
    data = json.load(f)


def upload_scholar():

    session = Session()

    for name, info in data.items():

        scholar = Scholar(info["id"], name, "json file")

        new_scholar = ScholarSchema().dump(scholar).data

        print(json.dumps(new_scholar, indent=2))

        session.add(scholar)

        session.commit()

    session.close()


if __name__ == "__main__":
    upload_scholar()
