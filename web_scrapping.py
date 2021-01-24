import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_rows", None)

var_covid = "https://en.wikipedia.org/wiki/COVID-19_pandemic"  # for brief info
var_site = "https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data"  # for worldwide
state_info = "https://news.google.com/covid19/map?hl=en-IN&gl=IN&ceid=IN%3Aen&mid=%2Fm%2F03rk0"

_request = requests.get(var_covid).text  # for brief info
var_requests = requests.get(var_site).text  # for worldwide
request_states = requests.get(state_info).text

# making soup of all sites, Returns the html code of the site

covid_soup = BeautifulSoup(_request, 'lxml')  # for brief info
soup = BeautifulSoup(var_requests, 'lxml')  # for worldwide
soup_i = BeautifulSoup(request_states, 'lxml')

para_tag = covid_soup.find_all('p')  # for var_covid
# print(para_tag).text


# for states of india
table_india = soup_i.find_all('tbody', class_='ppcUXd')  # type list
list_states_india = list()
list_td = list()
for i in table_india:
    tr = i.find_all('tr')
    for j in tr:
        th = j.find_all('th')
        for k in th:
            list_states_india.append(k.text)
        td = j.find_all('td')
        for l in td:
            list_td.append(l.text)


list_confirmed_india = list()
list_permillion = list()
list_recovered_india = list()
list_deaths_india = list()

infect_count_i = 0
while infect_count_i < len(list_td):
    list_confirmed_india.append(list_td[infect_count_i])
    infect_count_i += 5


million_count = 1
while million_count < len(list_td):
    list_permillion.append(list_td[million_count])
    million_count += 5
# print(list_permillion)

rec_count_i = 2
while rec_count_i < len(list_td):
    list_recovered_india.append(list_td[rec_count_i])
    rec_count_i += 5
# print(list_recovered)

death_count_i = 3
while death_count_i < len(list_td):
    list_deaths_india.append(list_td[death_count_i])
    death_count_i += 5
# print(list_deaths)

d_frame = pd.DataFrame(list(zip(list_states_india, list_confirmed_india, list_recovered_india, list_deaths_india)), columns=[
                       'States', 'Infections', 'Deaths', 'Recovered'])


# worldwide
var_table = soup.find("table", id="thetable")  # returns list
var_table_data = var_table.find_all('tr')  # table rows, is a list

list_country = list()
list_stats = list()
for tr in var_table_data:
    table_data = tr.find_all('td')  # not a list!
    table_h = tr.find_all('th')  # not a list!
    for stat in table_data:
        list_stats += [stat.text]
    for country in table_h:
        list_country += [country.text]

for i in list_country:
    if i == "\n":
        list_country.remove(i)


for i in list_stats:
    if i == "\n":
        list_stats.remove(i)


list_country_cleaned = list()
list_stats_cleaned = list()
list_infected = list()
list_recovered = list()
list_deaths = list()


for i in range(10, len(list_country)):
    list_country_cleaned.append(list_country[i].strip())


for j in range(0, 908):
    list_stats_cleaned.append(list_stats[j].strip())

for i in list_stats_cleaned:
    if "[" in i:
        list_stats_cleaned.remove(i)

# printing total cases
infected_counter = 0
while infected_counter < len(list_stats_cleaned):
    list_infected.append(list_stats_cleaned[infected_counter])
    infected_counter += 3


# printing death rates
death_counter = 1
while death_counter < len(list_stats_cleaned):
    list_deaths.append(list_stats_cleaned[death_counter])
    death_counter += 3
# print("\n\nList deaths : \n", list_deaths)

# printing recovered rates

recovd_counter = 2
while recovd_counter < len(list_stats_cleaned):
    list_recovered.append(list_stats_cleaned[recovd_counter])
    recovd_counter += 3
# print("\n\nList recovered\n", list_recovered)


table = pd.DataFrame(list(zip(list_country_cleaned, list_infected, list_deaths, list_recovered)), columns=[
    'Country', 'Infections', 'Deaths', 'Recovered'])


print("\nWhat is Covid-19?\n\n", para_tag[4].text,
      "\nSymptoms : \n\n", para_tag[2].text)
print("\nPreventive Measures : \n\n", para_tag[5].text)
print("\n\n\nHere is the state wise stats of India\n")
print(d_frame)
print("\n\n\n\nWorldWide Statistics of Covid-19\n")
print(table)
