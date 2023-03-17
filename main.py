import logging, os, re

import requests
from dotenv import load_dotenv


def main():
        
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG, filename='visits.log',
                        format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%A %d %B %Y %H:%M')


    BASE_URL = "https://www.pythonanywhere.com"
    LOGIN_URL = f"{BASE_URL}/login/"

    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv('PASSWORD')
    APP_NAME = os.getenv('APP_NAME')


    with requests.Session() as s:
        s.get(LOGIN_URL)
        csrftoken = s.cookies.get("csrftoken", s.cookies.get('csrf', ''))
        payload = {
            'csrfmiddlewaretoken': csrftoken,
            'auth-username': USERNAME,
            'auth-password': PASSWORD,
            'login_view-current_step': 'auth'
        }

        headers = {
            "Referer": LOGIN_URL
        }
        login_response = s.post(LOGIN_URL, data=payload, headers=headers)

        logging.info(f"Initial login status: {login_response.status_code}")

        webapps_url = f"{BASE_URL}/user/{USERNAME}/webapps/"
        s.get(webapps_url)
        csrftoken = s.cookies.get("csrftoken", s.cookies.get('csrf', ''))
        payload = {
            'csrfmiddlewaretoken': csrftoken
        }

        headers = {
            'Referer': f"{BASE_URL}/user/{USERNAME}/webapps/"
        }

        extend_url = f"{BASE_URL}/user/{USERNAME}/webapps/{APP_NAME}/extend"
        extend_response = s.post(extend_url, data=payload, headers=headers)

        extended_date = re.search(r"<strong>(.*)</strong>",extend_response.text)

        if extended_date is not None:
            logging.info(f"Extended to {extended_date.groups()[0]}")

if __name__  == '__main__':
    main()

