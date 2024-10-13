import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Holiday:
    def __init__(self, country, year, month, day): #contrusctor variable 
        self.country = country
        self.year = year
        self.month = month
        self.day = day
        self.get_data()

    def get_data(self): #retrieve API data and calculate and output if holiday or not 
        try:
            response = requests.get(f"https://holidays.abstractapi.com/v1/?api_key=e6b0b7ef63f64332832fec73065e557a&country={self.country}&year={self.year}&month={self.month}&day={self.day}")
            response.raise_for_status()  # Check for HTTP errors
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            self.is_holiday = False
            self.date = f"{self.year}-{self.month.zfill(2)}-{self.day.zfill(2)}"
            self.description = "N/A"
            return
        
        response_json = response.json()
        if response_json: #check if the response is empty meaning there is not a holiday
            try:
                holiday_data = response_json[0]
                self.type = holiday_data.get("type", "N/A")
                if self.type == "National": #only want it if it's a national holiday
                    self.date = holiday_data.get("date", f"{self.year}-{self.month.zfill(2)}-{self.day.zfill(2)}")
                    self.description = holiday_data.get("name", "N/A")
                    self.is_holiday = True
                    return self.is_holiday
                else:
                    self.date = f"{self.year}-{self.month.zfill(2)}-{self.day.zfill(2)}" #if not a national then scrap it
                    self.description = "N/A"
                    self.is_holiday = False
                    return self.is_holiday
            except (IndexError, KeyError):
                self.date = f"{self.year}-{self.month.zfill(2)}-{self.day.zfill(2)}"
                self.description = "N/A"
                self.is_holiday = False
                return self.is_holiday
        else:
            self.date = f"{self.year}-{self.month.zfill(2)}-{self.day.zfill(2)}"
            self.description = "N/A"
            self.is_holiday = False
            return self.is_holiday
    
    def hol_print(self):
        if self.is_holiday:
            print(f"This holiday is {self.date}")
            print(f"The holiday is {self.description} and is a {self.type} holiday")
        else:
            print("This is not a holiday")

class Tenor:
    @staticmethod
    def get_valid_tenor():
        while True:
            tenor_input = input("Input tenor (e.g., 1W, 3M): ").upper()
            if len(tenor_input) > 1 and tenor_input[:-1].isdigit() and tenor_input[-1] in ['W', 'M']:
                num = int(tenor_input[:-1])
                period = tenor_input[-1]
                if 1 <= num <= 12:
                    return num, period
            print("Invalid tenor. Please enter a number from 1 to 12 followed by 'W' (week) or 'M' (month).")
    
    def __init__(self):
        self.num, self.period = self.get_valid_tenor()

def apiinputs(): 
    currencies = {
        "JPY": "JP",
        "GBP": "GB",
        "EUR": "FR",
        "NZD": "NZ",
        "AUD": "AU",
        "NOK": "NO",
        "SEK": "SE",
        "CAD": "CA",
        "CHF": "CH"
    }

    in_currency = input("Input currency: ").upper() #input currency
    while in_currency not in currencies:#validate entry
        print("Error, that is not a currency")
        in_currency = input("Input currency: ").upper()
    country = currencies[in_currency]#entry is the key and checks against dictionary

    while True:
        date_str = input("Input today's date (YYYY/MM/DD): ")#input date 
        try:
            date = datetime.strptime(date_str, "%Y/%m/%d")
            break  # Exit the loop once a valid date is entered
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY/MM/DD format.")

    return country, date

def calculate_value_date(date):
    cal_twoGBdays = Holiday()

def calculate_expiry_date(date, num, period):
    match period:
        case "W":
            future_date = date + relativedelta(weeks=num)
        case "M":
            future_date = date + relativedelta(months=num)
        case _:
            print("Invalid period")
            return None, None, None
    date_str = future_date.date()#todays date plus whatever tenor was inputted, so can use this for D and W, for M and Y we will have to add 2 to it and then add the value    
    print("Expiry Date:", date_str)#
    
    return future_date
    
def date_seperate(future_date):# Convert year, month, and day to strings
    year = str(future_date.year)
    month = str(future_date.month).zfill(2)  # Ensure month is two digits
    day = str(future_date.day).zfill(2)      # Ensure day is two digits
    return year, month, day


def suggested_new_expirydate(is_holiday, future_date):
    if is_holiday == True:
        new_future_date = future_date + relativedelta(days=-2)
        date_str = new_future_date.date()
        print(f"Suggested new Value date is {date_str}")


tenor = Tenor()
country, date = apiinputs()
future_date = calculate_expiry_date(date, tenor.num, tenor.period)
year, month, day = date_seperate(future_date)
my_holiday = Holiday(country, year, month, day)
my_holiday.hol_print()
is_holiday = my_holiday.is_holiday
suggested_new_expirydate(is_holiday, future_date)