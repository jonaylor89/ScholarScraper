
-> # Selenium Web Scraper <-

-> Python and Selenium scrapping google scholar <-

-----------------------

# Names to parse
- Irfan Ahmed
- Tomasz Arodz
- Caroline Budwell
- Eyuphan Bulut
- Alberto Cano
- Krzysztof Cios
- Robert Dahlberg
- Kostadin Damevski
- Thang Dinh
- Debra Duke
- Carol Fung
- Preetam Ghosh
- Vojislav Kecman
- Bartosz Krawczyk
- Lukasz Kurgan
- John D. Leonard II
- Changqing Luo
- Milos Manic
- Bridget McInnes
- Tamer Nadeem
- Zachary Whitten
- Tarynn Witten
- Cang Ye
- Hong-Sheng Zhou

---------------------

# Possible Optimizations
* Download the html for a publication and parse that to allow for parallelization without the browser thinkings we're DOSing it
    * BeautifulSoup does stuff for that
* Switch drivers sometimes to confuse google's algorithms

-------------------------------------

# To Parse
- **FROM SCHOLAR**
    - Total Citations
    - Publications IDs
- **FROM PUBLICATIONS**
    - Publication ID
    - date of publications
    - Publication ID of citations

----------------------------------

# Algorithm

## Build Database

(Saturday)
Grab the total citations for each researcher
for each of their publications then
    Grab name, date of publishing, id

    for each citation of that publication then
        grab name, date of publish (citation date), and id
    end
end 

## Event loop

(Sunday)
Check the total citations
if there is a change then
    Go through the publications looking for the number of changes

    once found then
        go through that publication to find the exact publication to cite it and parse it
        i.e. Get data, publication id, and title of the new citation
    end
end