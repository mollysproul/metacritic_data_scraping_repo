import requests
from bs4 import BeautifulSoup
import datetime

CURRENT_DATE = datetime.date.today()

# ---------------------------------------DO-NOT-EDIT-ANYTHING-ABOVE-THIS-LINE----------------------------------------- #


START_DATE = CURRENT_DATE - datetime.timedelta(days=180)
END_DATE = CURRENT_DATE + datetime.timedelta(days=180)

OUTPUT_CSV = "metacritic_output.csv"





# ---------------------------------------DO-NOT-EDIT-ANYTHING-BELOW-THIS-LINE----------------------------------------- #




METACRITIC_LINK = "https://www.metacritic.com/feature/tv-premiere-dates"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/50.0.2661.102 Safari/537.36'}
MONTHS_DICT = {'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
               'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}


class airing:
    checked_this_round = 0
    notes = 'Unknown'
    network = 'Unknown'
    title = 'Unknown'
    type = 'Unknown'
    launch_date = 0
    twitter_tv_exists = 0
    fb_tv_exists = 0
    # 0 = active, 1=archives, 2=noAction
    location = -1

    def __iit__(self):
        self.checked_this_round = 0
        self.notes = 'Unknown'
        self.network = 'Unknown'
        self.title = 'Unknown'
        self.type = 'Unknown'
        self.launch_date = 0
        self.twitter_tv_exists = 0
        self.fb_tv_exists = 0
        # 0 = active, 1=archives, 2=noAction
        self.location = -1


    def analyze_self(self):
        print("reanalyzing self")
        if self.location != 0 and self.location != 1 and self.location != 2:
            self.location = -1
            print("status is now reset to default -1 status")
        #if type(launch_date) !=


    def set_values_by_dict(self, my_dict):
        notes_index = my_dict[NOTES_INDEX_LABEL]
        network_index = my_dict[NETWORK_INDEX_LABEL]
        title_index = my_dict[TITLE_INDEX_LABEL]
        type_index = my_dict[TYPE_INDEX_LABEL]
        launch_date_index = my_dict[LAUNCH_DATE_INDEX_LABEL]
        twitter_index = my_dict[TWITTER_TV_INDEX_LABEL]
        fb_index = my_dict[FB_TV_INDEX_LABEL]

        airing_data = my_dict['data']

        self.notes = airing_data[notes_index]
        self.network = airing_data[network_index]
        self.title = airing_data[title_index]
        self.type = airing_data[type_index]
        self.launch_date = slash_date_to_datetime(airing_data[launch_date_index])
        self.twitter_tv_exists = airing_data[twitter_index]
        self.fb_tv_exists = airing_data[fb_index]



def main():
    print("Running main()")
    metacritic_airings = load_metacritic_airings()

    assert len(metacritic_airings) > 0, 'No metacritic airings found'

    #for my_airing in metacritic_airings:
        #my_airing.checked_this_round = 1
        #if END_DATE >= my_airing.launch_date >= START_DATE:
            # is within date range
            # now try to find the airing in the google sheets
            #match_found = 0
        #print(my_airing)


    print("done running main()")





def load_metacritic_airings():
    print("running load_metacritic_airings()")

    # read in all metacritic shows
    r = requests.get(METACRITIC_LINK, headers=HEADERS)
    metacritic_soup = BeautifulSoup(r.text, "html.parser")
    #print(r.text)


    past_month = CURRENT_DATE.month

    month_int = -1
    day_int = -1
    year_int = CURRENT_DATE.year
    current_date = CURRENT_DATE

    tr_list_soup = metacritic_soup.find_all(["tbody"])

    metacritic_airings_list = []

    # load archives
    #archive_grid = load_data(METACRITIC_SPREADSHEET_ID, )

    # load
    for tbody in tr_list_soup:
        #print(tbody.text)
        for tr_soup in tbody.find_all("tr", class_=["even", "sublistbig"]):
            #print(tr_soup.text)
            #if ", " in tr_soup.text and " / " in tr_soup.text:
                #print(tr_soup.text)
            # try: print(tr_soup["class"])
            # except KeyError: print("key error")

            # if th class=title in this soup
            date_soup = tr_soup.find_all("th", class_="title")
            premiere_soup = tr_soup.find_all("td", class_="title")

            if len(date_soup) == 1:
                line = date_soup[0].get_text().strip()
                month_int = -1
                day_int = -1

                if "/" in line:
                    # The first premiere in a "new" year will have the date with the year at the end: SUN / FEBRUARY 27, 2022
                    if "," in line:
                        temp_line = line.split(', ')
                        year_string = temp_line[len(temp_line) - 1]
                        year_int = int(year_string)

                    for my_month in MONTHS_DICT:
                        if my_month in line:
                            month_int = MONTHS_DICT[my_month]

                    temp_line = line.replace(',', ' ').split(' / ')
                    temp_line = temp_line[len(temp_line) - 1].split(' ')  # July 2 or July 2, 2020
                    day_int = int(temp_line[1])

                    assert 1 <= month_int >= 12, "error converting this to a month: " + line
                    assert 1 <= day_int >= 31, "error converting this to a month: " + line

                    current_date = datetime.date(year_int, month_int, day_int)
                    # print(current_date)
                    past_month = month_int

            elif len(premiere_soup) == 1:
                # print("this is a premiere: ", premiere_soup[0].get_text().strip())
                current_airing = airing()
                current_airing.title = premiere_soup[0].get_text().strip()
                current_airing.launch_date = current_date
                td_soup = tr_soup.find_all("td")

                # find network
                network_soup = td_soup[len(td_soup) - 1]
                current_airing.network = network_soup.get_text().strip()
                if "," in current_airing.network:
                    current_airing.network = current_airing.network.split(",")[0].strip()

                img_soup = tr_soup.find_all("img")
                if len(img_soup) > 0:
                    for img_tags in img_soup:
                        alt_tag = img_tags['alt']
                        # print(alt_tag)
                        if alt_tag == "SPECIAL":
                            current_airing.type = "Special"
                        elif alt_tag == "MOVIE":
                            current_airing.type = "Movie"
                        elif alt_tag == "NEW":
                            current_airing.type = "Series"
                        elif alt_tag == "MINISERIES":
                            current_airing.type = "Miniseries"
                        else:
                            current_airing.network = alt_tag.strip()

                if current_airing.type == 'Unknown':
                    current_airing.type = "Series"
                print(current_airing.title, ", ", current_airing.type, ", ", current_airing.network,  ", ", current_airing.launch_date)
                metacritic_airings_list.append(current_airing)

    #go through this list, compare to archives
    return metacritic_airings_list






if __name__ == "__main__":
    main()