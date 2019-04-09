
-> # Selenium Web Scraper <-

-> Python and Selenium scrapping google scholar <-

-----------------------

# Names to parse
- Irfan Ahmed
- Tomasz Arodz
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
- Tarynn Witten
- Cang Ye
- Hong-Sheng Zhou

---------------------

# Optimizations
* Download the html for a publication and parse that to allow for parallelization without the browser thinkings we're DOSing it
    * Using ScraPY or BeautifulSoup
* Switch drivers sometimes to confuse google's algorithms
* Email report to me of the changes since the last parse (python smtp library)
* Use configuration file

-------------------------------------

# To Parse
- **FROM SCHOLAR**
    [x] Total Citations
    [x] Publications IDs 
- **FROM PUBLICATIONS**
    [] Publication ID
    [x] Date of publications
    [x] Number of citations
    [] Publication ID of citations

----------------------------------

# Algorithm

## Build Database

Grab the total citations for each researcher
for each of their publications then
    Grab name, date of publishing, id

    for each citation of that publication then
        grab name, date of publish (citation date), and id
    end
end 

## Event loop

Check the total citations
if there is a change then
    Go through the publications looking for the number of changes

    once found then
        go through that publication to find the exact publication to cite it and parse it
        i.e. Get data, publication id, and title of the new citation
    end
end