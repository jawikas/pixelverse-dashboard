import re
import json
import time
import imaplib
import requests
from colorama import *
from faker import Faker
from email import policy
from datetime import datetime
from email.parser import BytesParser
from src.headers import get_headers
from email.header import decode_header

mrh = Fore.LIGHTRED_EX
pth = Fore.LIGHTWHITE_EX
hju = Fore.LIGHTGREEN_EX
kng = Fore.LIGHTYELLOW_EX
bru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
htm = Fore.LIGHTBLACK_EX

def print_with_timestamp(message, **kwargs):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flush = kwargs.pop('flush', False)
    end = kwargs.pop('end', '\n')
    print(f"{htm}[{current_time}] {message}", flush=flush, end=end)

def print_line():
    print_with_timestamp(pth + "~" * 40)

def countdown_timer(seconds):
    while seconds:
        menit, detik = divmod(seconds, 60)
        jam, menit = divmod(menit, 60)
        jam = str(jam).zfill(2)
        menit = str(menit).zfill(2)
        detik = str(detik).zfill(2)
        print(f"{pth}please wait until {jam}:{menit}:{detik} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print("                          ", flush=True, end="\r")

fake = Faker()


def print_banner():
    banner = r"""
    ██╗████████╗███████╗     ██╗ █████╗ ██╗    ██╗
    ██║╚══██╔══╝██╔════╝     ██║██╔══██╗██║    ██║
    ██║   ██║   ███████╗     ██║███████║██║ █╗ ██║
    ██║   ██║   ╚════██║██   ██║██╔══██║██║███╗██║
    ██║   ██║   ███████║╚█████╔╝██║  ██║╚███╔███╔╝
    ╚═╝   ╚═╝   ╚══════╝ ╚════╝ ╚═╝  ╚═╝ ╚══╝╚══╝  """ 
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(hju + "    Pixelverse Dashboard Auto Referral")
    print(mrh + f"    NOT FOR SALE = Free to use")
    print(mrh + f"    before start please '{hju}git pull{mrh}' to update bot\n")

class Core:
    def __init__(self, access_token=None):
        with open('config.json', 'r') as file:
            self.config = json.load(file)

        self.email = self.config['email']
        self.password = self.config['password']
        self.referrals = self.config['referrals']
        self.count = self.config['count']
        self.fake = Faker()
        self.access_token = access_token
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Origin': 'https://dashboard.pixelverse.xyz',
            'Referer': 'https://dashboard.pixelverse.xyz/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36'
        }

    def generate_emails(self):
        email_parts = self.email.split('@')
        generated_emails = []

        for _ in range(self.count):
            random_name = self.fake.user_name()
            generated_email = f'{email_parts[0]}+{random_name}@{email_parts[1]}'
            generated_emails.append(generated_email)
            
        generated_emails.sort()
        
        print_with_timestamp(hju + f"Creating {self.count} Emails")
        return generated_emails

    def connect_imap(self):
        mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        mail.login(self.email, self.password)
        return mail
    
    def search_email(self, mail):
        mail.select('inbox')
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        for email_id in reversed(email_ids):
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = BytesParser(policy=policy.default).parsebytes(response_part[1])
                    msg_subject = decode_header(msg['Subject'])[0][0]
                    if isinstance(msg_subject, bytes):
                        msg_subject = msg_subject.decode()
                    if 'Pixelverse Authorization' in msg_subject:
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                if content_type == 'text/plain':
                                    body = part.get_payload(decode=True).decode()
                                    return body
                        else:
                            body = msg.get_payload(decode=True).decode()
                            return body
        return None
    
    def extract_otp(self, body):
        otp_match = re.search(r'Here is your Pixelverse OTP: (\d+)', body)
        return otp_match.group(1) if otp_match else None

    def request_otp(self, email, proxy):
        url = 'https://api.pixelverse.xyz/api/otp/request'
        payload = {'email': email}
        proxies = {'http': f'http://{proxy}'}
        try:
            response = requests.post(url, proxies=proxies, json=payload)
            time.sleep(0.1)
            if response.status_code == 429:
                print_with_timestamp(f"{kng}{response.reason}, switching",flush=True)
                return False
            response.raise_for_status()
            return response.status_code in [200, 201]
        except (ValueError, json.JSONDecodeError, requests.RequestException) as e:
            print_with_timestamp(f"{mrh}Error: {e.response.text}",end="\r",flush=True)
            return False

    def verify_otp(self, email, otp, proxy):
        url = 'https://api.pixelverse.xyz/api/auth/otp'
        payload = {
            'email': email,
            'otpCode': otp
        }
        proxies = {'http': f'http://{proxy}'}
        try:
            response = requests.post(url, proxies=proxies, json=payload)
            response.raise_for_status()
            data = response.json()
            data['refresh_token'] = response.cookies.get('refresh-token')
            data['access_token'] = data['tokens']['access']
            return data
        except (ValueError, json.JSONDecodeError, requests.RequestException) as e:
            print_with_timestamp(f"{mrh}Error: {e.response.text}")
            return None

    def set_referrals(self, access_token, proxy):
        url = f'https://api.pixelverse.xyz/api/referrals/set-referer/{self.referrals}'
        self.headers['Authorization'] = access_token
        proxies = {'http': f'http://{proxy}'}
        try:
            response = requests.put(url, proxies=proxies, headers=self.headers)
            time.sleep(0.1)
            response.raise_for_status()
            return response.status_code in [200, 201]
        except (ValueError, json.JSONDecodeError, requests.RequestException) as e:
            print_with_timestamp(f"{mrh}Error: {e}")
            return None

    def update_profile(self, access_token):
        url = "https://api.pixelverse.xyz/api/users/@me"
        self.headers = get_headers(access_token)
        payload = {
            "updateProfileOptions": {
                "username": fake.user_name(),
                "biography": fake.sentence()
            }
        }
        try:
            response = requests.patch(url, headers=self.headers, json=payload)
            time.sleep(0.1)
            if response.status_code == 200:
                print_with_timestamp(pth + f"Profile {hju}updated successfully")
            else:
                print_with_timestamp(mrh + f"Failed to update profile. Status: {response.status_code}, Respons: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print_with_timestamp(mrh + f"Error: {e}")
            return False

    def purchase_pet(self, access_token, pet_id):
        url = f"https://api.pixelverse.xyz/api/pets/{pet_id}/buy"
        self.headers = get_headers(access_token)
        try:
            response = requests.post(url, headers=self.headers)
            time.sleep(0.1)
            if response.status_code in [200, 201]:
                print_with_timestamp(pth + f"Pet {hju}successfully purchased")
                return response.status_code, response.json()
            else:
                print_with_timestamp(mrh + f"Failed to buy a pet. Status: {response.status_code}, Respons: {response.text}")
            return None, None
        except Exception as e:
            print_with_timestamp(mrh + f"Error: {e}")
            return None, None

    def select_pet(self, access_token, pet_data):
        pet_id = pet_data['id']
        url = f"https://api.pixelverse.xyz/api/pets/user-pets/{pet_id}/select"
        self.headers = get_headers(access_token)
        try:
            response = requests.post(url, headers=self.headers)
            time.sleep(0.1)
            if response.status_code == 201:
                print_with_timestamp(pth + f"Pet {hju}successfully selected!")
                return True
            elif response.status_code == 200:
                print_with_timestamp(pth + f"Pet  {hju}has been selected before")
                return True
            elif response.status_code == 400:
                if response.json().get('message') == "You have already selected this pet":
                    print_with_timestamp(pth + f"Pet {hju}has been selected")
                    return True
                else:
                    print_with_timestamp(mrh + f"Failed to select a pet. Status: {response.status_code}, Respons: {response.json()}")
            else:
                print_with_timestamp(mrh + f"Failed to select a pet. Status: {response.status_code}, Respons: {response.text}")
            return False
        except Exception as e:
            print_with_timestamp(mrh + f"Error: {e}")
            return False

    def claim_reward(self, access_token):
        url = "https://api.pixelverse.xyz/api/daily-reward/complete"
        self.headers = get_headers(access_token)
        try:
            response = requests.post(url, headers=self.headers)
            time.sleep(0.1)
            if response.status_code in [200, 201]:
                print_with_timestamp(pth + f"Daily {hju}reward successfully claimed!")
                return True
            else:
                print_with_timestamp(mrh + f"Failed to claim daily reward. Status: {response.status_code}, Respons: {response.text}")
        except Exception as e:
            print_with_timestamp(mrh + f"Failed to claim daily reward: {str(e)}")
        return False


    

