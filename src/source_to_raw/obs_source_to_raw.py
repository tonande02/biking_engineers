from datetime import datetime
import urllib.request 

def get_raw_obs(year, month):
    url = "https://data.urbansharing.com/oslobysykkel.no/trips/v1/"
    month = str(month)
    if len(month) == 1:
        month = "0" + month
    url += str(year) + "/" + month + ".json"
    print(url)
    filename = "data/raw/obs_" + str(year) + "-" + month + ".json"
    print(filename)
#    urllib.request.urlretrieve(url, filename)

# This fuction calls get_raw_obs with all months from the inputed year and month until
# current month if there is no input for to year and month
def get_all_raw_obs_from(from_year, from_month, to_year = None, to_month = None):
    months_in_years = []
    if to_year == None:
        to_year = datetime.now().year
    if to_month == None:
        to_month = datetime.now().month
    years = list(range(from_year, to_year+1))
    if len(years) == 1:
        for month in range(from_month, to_month+1):
            months_in_years.append(str(years[0]) + "-" + str(month))
    elif len(years) == 2:
        for month in range(from_month, 13):
            months_in_years.append(str(years[0]) + "-" + str(month))
        for month in range(1, to_month+1):
            months_in_years.append(str(years[1]) + "-" + str(month))
    else:
        months_in_first_year = range(from_month, 13)
        months_in_last_year = range(1, to_month+1)
        middle_years = years[1:-1]

        for month in months_in_first_year:
            months_in_years.append(str(years[0]) + "-" + str(month))
        for year in middle_years:
            for month in range(1, 13):
                months_in_years.append(str(year) + "-" + str(month))
        for month in months_in_last_year:
            months_in_years.append(str(years[-1]) + "-" + str(month))
    print(months_in_years)
    for month in months_in_years:
        get_raw_obs(month.split("-")[0], month.split("-")[1])


#get_raw_obs(2020, 3)
#get_all_raw_obs_from(2019, 1, 2019, 1)
