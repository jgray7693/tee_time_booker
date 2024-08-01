import sys
import requests
import datetime

# user settings, modify in userconfig.txt for now. will eventually make this configurable via CLI
# creating list object 'userconfig' and stripping whitespace
# global constants initialized from userconfig list
userconfig = [line.strip() for line in open('userconfig.txt')]
WEBSITE = userconfig[0]
USERNAME = userconfig[1]
PASSWORD = userconfig[2]
COURSE_ID = userconfig[3]
SCHEDULE_ID = userconfig[4]
# COURSE ABBREVIATION = userconfig[4]

# user parameters for finding specific tee times
# TODO: we will move this to a preferences/modifiable user config system later, set predefined vals for now
HOLES = 18
AVAILABLE_SPOTS = 1
MAX_PLAYERS = 4


# building URL constants from userconfig.txt to determine which course to book at
LOGIN_URL = WEBSITE+"/index.php/api/booking/users/login"

# old, keeping here just incase. payload in userLogin contains course_id instead
# LOGIN_URL = WEBSITE+"/index.php/booking/"+COURSE_ID+"/"+SCHEDULE_ID+"#/login"

# handle user auth, return error if login incorrect
# call this in main initially before any other functions
def userLogin(username, password): 
    # dictionary for http req header content defs
    # saving this for later lol https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    # data payload
    payload = {"api_key":"no_limits", "booking_class_id":None,
               "password":password, "username":username, "course_id":COURSE_ID}
    # object built from sending POST request to URL constant defined by userconfig.txt 
    response = requests.post(LOGIN_URL, data=payload)
    # checking for status code 200 ('ok') - if not ok, return 401 Client Error
    try:
        response = requests.post(LOGIN_URL, data=payload, headers=headers)
        response.raise_for_status()  # this will raise an HTTPError if the response was an error
        print("=================")
        print("LOGGED IN!")
        print("=================")

        print("URL: ", response.url)
        # print("Account Details: ", response.json())
    # error handling 
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

def getOpenTeeTimes(date):
    url = f"{WEBSITE}/index.php/api/booking/times?time=all&{date}&holes={HOLES}&players=0&booking_class=929&schedule_id=1470&schedule_ids%5B%5D=1470&schedule_ids%5B%5D=1490&specials_only=0&api_key=no_limits"
    response = requests.get(url)
    try:
        response.raise_for_status
        open_tee_times = response.json()
        return open_tee_times
    except requests.exceptions.RequestException as e:
        print(f"An error occurred when fetching open tee times: {e}")
        return None


def main():
    userLogin(USERNAME, PASSWORD)
    while True:
        print("\nMain Menu:")
        print("1. Check date for open tee times")
        print("2. PLACEHOLDER")
        print("3. PLACEHOLDER")
        print("4. Exit")
        choice = input("Enter your choice (1-4):")
        
        if choice == "1":
            date = input("Enter the desired date to check for open tee times (MM-DD-YYYY). Leave blank to check todays times.\n")
            open_tee_times = getOpenTeeTimes(date)
            if open_tee_times:
                print("Open Times:")
                for tee_time in open_tee_times:
                    print(tee_time)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid selection. Please enter a number between 1-4.")
            
            
if __name__ == "__main__":
    main()