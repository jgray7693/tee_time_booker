import sys
import requests
import datetime

# user settings, modify in userconfig.txt for now
# (maybe initialize userconfig.txt via cli on first run? can implement later)

# creating list object 'userconfig' and stripping whitespace
# global constants initialized from userconfig list
userconfig = [line.strip() for line in open('userconfig.txt')]
WEBSITE = userconfig[0]
USERNAME = userconfig[1]
PASSWORD = userconfig[2]
COURSE_ID = userconfig[3]
SCHEDULE_ID = userconfig[4]
# COURSE ABBREVIATION = userconfig[4]

# building URL constants from userconfig.txt to determine which course you want to book at
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
        print("Logged in!")
        print("=================")
        print("DEBUGGING INFO")
        print("=================")

        print("URL: ", response.url)
        print("Account Details: ", response.json())
    # error handling 
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

# return list of all available time slots

# find + book best time slot

# find + book least crowded course time slot

def main():
    print("running main()")
    login_result = userLogin(USERNAME, PASSWORD)

if __name__ == "__main__":
    main()