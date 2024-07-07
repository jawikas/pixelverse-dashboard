import os
import sys
import time
from colorama import *
from faker import Faker
from src.core import Core, print_with_timestamp, print_line, countdown_timer
from src.core import mrh, hju, htm , kng, pth, bru, reset, print_banner
from src.Proxy import Proxy

fake = Faker()

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    clear()
    print_banner()
    init()
    core = Core()
    pro = Proxy()
    emails = core.generate_emails()
    proxies = pro.get_proxies()
    connect_imap = core.connect_imap()
    proxy_index = +1
    for index, email in enumerate(emails, start=1):
        if not proxies:
            print_with_timestamp(f"{kng}No proxies available. Retrieving new proxies")
            proxies = pro.get_proxies()
            if not proxies:
                print_with_timestamp(f"{mrh}Failed to retrieve proxies")
                break

        proxy = pro.get_random_proxy()

        while not pro.is_proxy_live(proxy):
            print_with_timestamp(f"{mrh}Inactive: {pth}{proxy}      ", end="\r",flush=True)
            proxy = pro.get_random_proxy()
            if not proxies:
                print_with_timestamp(f"{kng}No proxies available. retrieving new proxies")
                proxies = pro.get_proxies()
                if not proxies:
                    print_with_timestamp(f"{mrh}Failed to retrieve proxies")
                    break
                
            proxy = pro.get_random_proxy()

        if not proxies:
            print_with_timestamp(f"{mrh}No active proxies available")
            break
        
        print_with_timestamp(f"{hju}Active: {pth}{proxy}        ",flush=True)
        
        while True:
            print_with_timestamp(f"{kng}Register account {pth}{index}:")
            print_with_timestamp(f"{pth}{email}")
            
            if core.request_otp(email, proxy):
                print_with_timestamp(f"{hju}Succesfully request code")
                print_with_timestamp(f"{kng}Please wait a bit",end="\r",flush=True)
                time.sleep(10)
                body = core.search_email(connect_imap)
                code = core.extract_otp(body)
                print_with_timestamp(f"{hju}Received code : {pth}{code}",flush=True)
                
                data = core.verify_otp(email, code, proxy)
                if data and 'access_token' in data:
                    access_token = data['access_token']
                    print_with_timestamp(f"{hju}Access token received")
                    
                    if core.set_referrals(access_token, proxy):
                        print_with_timestamp(f"{pth}Successfully {hju}set referrals")
                        
                    if core.update_profile(access_token):
                        pet_id = "27977f52-997c-45ce-9564-a2f585135ff5"
                        pet_status, pet_data = core.purchase_pet(access_token, pet_id)
                        
                        if pet_status in [200, 201]:
                            if core.select_pet(access_token, pet_data):
                                if core.claim_reward(access_token):
                                    print_with_timestamp(hju + f"Referral no.{pth}{index} {hju}complete")
                                    print_line()
                                else:
                                    print_with_timestamp(f"{mrh}Failed to claim reward")
                            else:
                                print_with_timestamp(f"{mrh}Failed to select pet")
                            break
                        else:
                            print_with_timestamp(f"{mrh}Failed to purchase pet")
                            proxy = pro.get_random_proxy()
                            
                            if not proxies:
                                print_with_timestamp(f"{kng}No proxies available. Retrieving new proxies")
                                proxies = pro.get_proxies()
                                if not proxies:
                                    print_with_timestamp(f"{mrh}Failed to retrieve proxies")
                                    break
                            
                            proxy_index %= len(proxies)
                            proxy = proxies[proxy_index]
                            
                            while not pro.is_proxy_Active(proxy):
                                print_with_timestamp(f"{mrh}Inactive: {pth}{proxy}  ", end="\r", flush=True)
                                proxy = pro.get_random_proxy()
                                
                                if not proxies:
                                    print_with_timestamp(f"{kng}No proxies available. Retrieving new proxies")
                                    proxies = pro.get_proxies()
                                    if not proxies:
                                        print_with_timestamp(f"{mrh}Failed to retrieve proxies")
                                        break
                                
                                proxy_index %= len(proxies)
                                proxy = proxies[proxy_index]
                            
                            print_with_timestamp(f"{hju}Switched to : {pth}{proxy}")
                else:
                    print_with_timestamp(f"{mrh}Failed to verifying code")
                    print_line()
                    countdown_timer(5)
                    break

            else:
                print_with_timestamp(f"{mrh}Failed to request code")
                print_line()
                countdown_timer(5)
                break
            connect_imap.logout()

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print_with_timestamp(f"{mrh}Error: {type(e).__name__} {e}")
        