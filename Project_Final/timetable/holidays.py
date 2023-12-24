from datetime import datetime
from bs4 import BeautifulSoup
import requests
from .models import Holiday

def add_update_holidays():
    current_datetime = datetime.now()

    # If current date is a Monday,
    if current_datetime.weekday() == 0:
        soup = BeautifulSoup(
            requests.get("https://www.mom.gov.sg/employment%20practices/public%20holidays").text,
            'html.parser'
            )

        holiday_elems = soup.find_all("td", class_= "cell-holiday-name")

        for holiday in holiday_elems:
            # Extract name and date from the <td> element
            name = holiday.contents[0].strip()  # Get the first child and remove leading/trailing whitespace
            extracted_date = holiday.find("span", class_="text-date-mobile").get_text(strip=True)

            if len(extracted_date.split('-')) > 1:
                dates = extracted_date.split(",")[0].split("-")
                start_date = dates[0].strip()
                end_date = dates[0].strip()

                print("Name:", name)
                print(f"Date: {start_date} to {end_date}")
                print("-" * 20)

                holiday = Holiday(
                    name = name,
                    start_date = datetime.strptime(start_date, '%d %B %Y'),
                    end_date = datetime.strptime(end_date, '%d %B %Y'),
                )

            else:
                # Print the extracted information
                date = extracted_date.split(",")[0].strip()

                print("Name:", name)
                print("Date:", date)
                print("-" * 20)

                holiday = Holiday(
                    name = name,
                    start_date = datetime.strptime(date, '%d %B %Y'),
                    end_date = datetime.strptime(date, '%d %B %Y'),
                )

            holiday.save()

        # print("Holidays updated")

    else:
        # print("No holidays updated")
        pass
