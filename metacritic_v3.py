import requests
from bs4 import BeautifulSoup
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


CURRENT_DATE = datetime.datetime.now()

# ---------------------------------------DO-NOT-EDIT-ANYTHING-ABOVE-THIS-LINE----------------------------------------- #


START_DATE = CURRENT_DATE - datetime.timedelta(days=180)
END_DATE = CURRENT_DATE + datetime.timedelta(days=180)

OUTPUT_CSV = CURRENT_DATE.strftime('%Y%m%d') + "_metacritic_data.csv"


# ---------------------------------------DO-NOT-EDIT-ANYTHING-BELOW-THIS-LINE----------------------------------------- #

METACRITIC_LINK = "https://www.metacritic.com/feature/tv-premiere-dates"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/50.0.2661.102 Safari/537.36'}

MONTHS_DICT = {'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
               'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}


#labels should be consistent, (also index labels for dictionaries)
NOTES_HEADING_LABEL = 'notes'
NETWORK_HEADING_LABEL = 'network'
TITLE_HEADING_LABEL = 'title'
TYPE_HEADING_LABEL = 'type'
LAUNCH_DATE_HEADING_LABEL = 'launch_date'
TWITTER_TV_HEADING_LABEL = 'twitterTV_exists'
FB_TV_HEADING_LABEL = 'fbTV_exists'

# Labels of the worksheets within the "Metacritic" Spreadhseet
ACTIVE_WORKSHEET_LABEL = "Active"
NO_ACTION_WORKSHEET_LABEL = "NoAction"
ARCHIVES_WORKSHEET_LABEL = "Archives"


class airing:
    checked_this_round = 0
    notes = ''
    network = 'Unknown'
    title = 'Unknown'
    type = 'Unknown'
    launch_date = 'Unknown'
    twitter_tv_exists = ''
    fb_tv_exists = ''
    # 0 = active, 1=archives, 2=noAction
    location = -1

    def __iit__(self):
        self.checked_this_round = 0
        self.notes = ''
        self.network = 'Unknown'
        self.title = 'Unknown'
        self.type = 'Unknown'
        self.launch_date = 'Unknown'
        self.twitter_tv_exists = ''
        self.fb_tv_exists = ''
        # 0 = active, 1=archives, 2=noAction
        self.location = -1

    def __str__(self):
        return "checked_this_round = %d\n" \
               "notes = %s\n" \
               "network = %s\n" \
               "title = %s\n" \
               "type = %s\n" \
               "launch_date = %s\n" \
               "twitter_tv_exists = %s\n" \
               "fb_tv_exists = %s\n" \
               "location = %d\n" % (self.checked_this_round, self.notes, self.network, self.title, self.type,
                                  self.launch_date, self.twitter_tv_exists, self.fb_tv_exists, self.location)

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
    # Get airings that we have in canvs (via the Metacritic spreadhseet)
    # Get airings listed on Metacritic Website
    # Compare the Airings


    #print(telemedicine)
    #load_all_airings()

    #print(archives_worksheet_data)




    print("Running main()")

    #List of all of the airings currently visible on the metacritic website
    metacritic_airings = load_metacritic_airings()

    assert len(metacritic_airings) > 0, 'No metacritic airings found'

    print("done running main()")
    return

# returns a dictionary of data (in "airings" class form) and indicies for the main headers
# dict[data] = list
# dict['notes_index']
def load_all_airings():

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    metacritic_sheet = client.open('Metacritic')

    active_worksheet_data = metacritic_sheet.worksheet(ACTIVE_WORKSHEET_LABEL).get_all_records()
    no_action_worksheet_data = metacritic_sheet.worksheet(NO_ACTION_WORKSHEET_LABEL).get_all_records()
    archives_worksheet_data = metacritic_sheet.worksheet(ARCHIVES_WORKSHEET_LABEL).get_all_records()

    spreadsheet_airings = []

    for airing_dict in active_worksheet_data:
        temp_airing = airing()
        temp_airing.notes = airing_dict[NOTES_HEADING_LABEL]
        temp_airing.network = airing_dict[NETWORK_HEADING_LABEL]
        temp_airing.title = airing_dict[TITLE_HEADING_LABEL]
        temp_airing.type = airing_dict[TYPE_HEADING_LABEL]
        temp_airing.launch_date = airing_dict[LAUNCH_DATE_HEADING_LABEL]
        temp_airing.twitter_tv_exists = airing_dict[TWITTER_TV_HEADING_LABEL]
        temp_airing.fb_tv_exists = airing_dict[FB_TV_HEADING_LABEL]
        temp_airing.location = 0

        spreadsheet_airings.append(temp_airing)

    for airing_dict in no_action_worksheet_data:
        temp_airing = airing()
        temp_airing.notes = airing_dict[NOTES_HEADING_LABEL]
        temp_airing.network = airing_dict[NETWORK_HEADING_LABEL]
        temp_airing.title = airing_dict[TITLE_HEADING_LABEL]
        temp_airing.type = airing_dict[TYPE_HEADING_LABEL]
        temp_airing.launch_date = airing_dict[LAUNCH_DATE_HEADING_LABEL]
        temp_airing.twitter_tv_exists = airing_dict[TWITTER_TV_HEADING_LABEL]
        temp_airing.fb_tv_exists = airing_dict[FB_TV_HEADING_LABEL]
        temp_airing.location = 1
        spreadsheet_airings.append(temp_airing)

    for airing_dict in archives_worksheet_data:
        temp_airing = airing()
        temp_airing.notes = airing_dict[NOTES_HEADING_LABEL]
        temp_airing.network = airing_dict[NETWORK_HEADING_LABEL]
        temp_airing.title = airing_dict[TITLE_HEADING_LABEL]
        temp_airing.type = airing_dict[TYPE_HEADING_LABEL]
        temp_airing.launch_date = airing_dict[LAUNCH_DATE_HEADING_LABEL]
        temp_airing.twitter_tv_exists = airing_dict[TWITTER_TV_HEADING_LABEL]
        temp_airing.fb_tv_exists = airing_dict[FB_TV_HEADING_LABEL]
        temp_airing.location = 2
        print(temp_airing)
        spreadsheet_airings.append(temp_airing)

    print(len(spreadsheet_airings))



    #return return_me

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

                    assert 1 <= month_int <= 12, "error converting this to a month: " + line
                    assert 1 <= day_int <= 31, "error converting this to a month: " + line

                    current_date = datetime.date(year_int, month_int, day_int)
                    # print(current_date)
                    past_month = month_int

            elif len(premiere_soup) == 1:
                # print("this is a premiere: ", premiere_soup[0].get_text().strip())
                current_airing = airing()
                current_airing.title = premiere_soup[0].get_text().replace("  Trailer", "").strip()
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
                            current_airing.fb_tv_exists = "No"
                        elif alt_tag == "NEW":
                            current_airing.type = "Series"
                        elif alt_tag == "MINISERIES":
                            current_airing.type = "Miniseries"
                        else:
                            current_airing.network = alt_tag.strip()

                if current_airing.type == 'Unknown':
                    current_airing.type = "Series"

                if current_airing.network == "Reelz" or current_airing.network == "Smithsonian":
                    current_airing.notes = "Don't track this network"

                print(current_airing.notes, ",", current_airing.title, ", ", current_airing.type, ", ", current_airing.network,  ", ", current_airing.launch_date, ",", current_airing.twitter_tv_exists, ",", current_airing.fb_tv_exists)
                metacritic_airings_list.append(current_airing)

    #go through this list, compare to archives
    return metacritic_airings_list


if __name__ == "__main__":
    main()