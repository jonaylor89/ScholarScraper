
import scholarly

import json
from random import randint, shuffle
from time import sleep

def main():

    output = {}

    cs_researchers = [
            "Alberto Cano",
    ]
    """
            "Tomasz Arodz",
            "Eyuphan Bulut",
            "Irfan Ahmed",
            "Krzysztof J Cios",
            "Kostadin Damevski",
            "Thang N. Dinh",
            "Carol Fung",
            "preetam ghosh",
            "Vojislav Kecman",
            "Bartosz Krawczyk",
            "Lukasz Kurgan",
            "John D. Leonard II",
            "Changqing Luo",
            "Milos Manic",
            "Bridget T. McInnes",
            "Tamer Nadeem",
            "Tarynn M Witten",
            "Cang Ye",
            "Hong-Sheng Zhou",
    ]
    """

    shuffle(cs_researchers)

    for i, researcher in enumerate(cs_researchers):
        query = scholarly.search_author(researcher)
        author = next(query).fill()

        print(author.publications[0])
        print(author.publications[0].fill())

        cites = author.publications[0].get_citedby()
        for x in range(5):
            print(next(cites))

        """
        for pub in author.publications:
            print("________________________")
            pub.fill()

        output[researcher] = author.__str__().replace("\'", "\"")

        print(author)
        print("-----------------------------")


        print(f"{i}" * 50)

        sleep(randint(1, 2))

         
    with open("output.json", 'w+') as f:
        json.dump(output, f)

    """

if __name__ == '__main__':
    main()
