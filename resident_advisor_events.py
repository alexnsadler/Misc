"""
Program to web scrape artists' event information.

Artists' upcoming events' information is scraped from www.residentadvisor.net.
"""

import google_calendar_login
import csv
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# List of artists in all lowercase that are on www.residentadvisor.net
ARTISTS = [" "]
# Location of the csv file information is to be written to
CSV_LOCATION = ""
# User's email address and password
EMAIL = ""
PASSWORD = ""


class ArtistInfo:
    """Class for finding, writing, and uploading to google cal artist info."""

    def __init__(self, artist_list, csv_location):
        """Define the initial arguments for the ArtistInfo class.

        Input: artist_list is a list of artists
        """
        self.artist_list = artist_list
        self.csv_location = csv_location
        # Initial headers for the csv file
        self.csv_list = [["Subject", "Start Date", "Location"]]

    def scrape_artist_info(self):
        """Export artist upcoming performance information to a csv.

        Input: a list of artists in all lowercase, string format

        Output: artist tour information as a list of lists.
        """
        for artist in self.artist_list:

            # open the html file for the artist on RA and parse it
            urllink = "https://www.residentadvisor.net/dj/" + artist
            page = requests.get(urllink)
            soup = BeautifulSoup(page.content, 'html.parser')

            # tries to find the header corresponding to "Upcoming Events"
            try:
                events_list = soup.find(id="items").find_all("h1")
            except:  # if there are no upcoming events for the artist, pass
                print artist, "has no upcoming events, or isn't on RA."
                pass
            else:
                for idx in range(len(events_list)):
                    # Check to see if the date ends with "/" for html processing
                    if events_list[idx].get_text()[-2] == "/":
                        event_text = events_list[idx].get_text()

                        # Reformats the date to proper csv upload format
                        date = ((event_text.replace("/", "")).
                                            replace(",", "").strip())
                        formated_date = (datetime.strptime(date, "%a %d %b %Y")
                                         .strftime("%m/%d/%Y"))

                        # The event info is in events_list[idx + 1]
                        event = events_list[idx + 1].get_text()
                        # Location info is in event_info
                        location = event[event.find("at") + 3:]

                        event_info = event[:event.find("at")]

                        title_info = (u' '.join((artist.title(), "at",
                                      location, "at", event_info)).
                                      encode('utf-8').strip())

                        # Append to csv_list
                        self.csv_list.append([title_info, formated_date,
                                              location])

        print "Loaded all artists' upcoming events."

        return self.csv_list

    def write_to_csv(self):
        """Write a a list of lists to a csv file.

        Input: csv_list is a list of lists (generated from scrape_artist_info)
        with artist's event information. csv_location is the file location for
        the input to be written to.

        Output: a csv file with the information from csv_list
        """
        with open(self.csv_location, "wb") as output:
            writer = csv.writer(output, lineterminator='\n')
            for title, date, loc in self.csv_list:
                if isinstance(title, str):
                    title = unicode(title, 'utf-8')
                writer.writerow([title.encode('utf-8'), date.encode('utf-8'),
                                 loc.encode('utf-8')])

        print "All artists' upcoming events loaded to csv."


obj = ArtistInfo(ARTISTS, CSV_LOCATION)
obj.scrape_artist_info()
obj.write_to_csv()
google_calendar_login.open_calendar(EMAIL, PASSWORD)
