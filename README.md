# Pixelverse Dashboard

Pixelverse Dashboard is a Python application designed to automate the process of [Pixelverse](https://dashboard.pixelverse.xyz/) registering accounts, requesting and verifying OTPs, setting referrals, updating profiles, purchasing pets, selecting pets, and claiming rewards on the Pixelverse platform. It also includes proxy management to avoid rate limiting and ensure smooth operations.

Website : https://dashboard.pixelverse.xyz/

### Buy me Coffee ☕ 
```
0x705C71fc031B378586695c8f888231e9d24381b4
```

## Features

- **Email Generation**: Automatically generates realistic email addresses using the Faker library.
- **Proxy Management**: Fetches and validates proxies to prevent rate limiting and ensure continuous operation.
- **Account Registration**: Registers new accounts using the generated email addresses.
- **OTP Request and Verification**: Requests and verifies OTPs for account registration.
- **Referral Setting**: Automatically sets referrals for registered accounts.
- **Profile Update**: Updates the profile of registered accounts.
- **Pet Purchase and Selection**: Purchases and selects pets for registered accounts.
- **Reward Claiming**: Claims rewards for registered accounts.

## Prerequisites

- Python 3.7+
- `requests` library
- `concurrent.futures` library
- `faker` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/jawikas/pixelverse-dashboard.git
    cd pixelverse-dashboard
    ```
    
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create an outlook or hotmail account
   - Create an [account here](https://www.microsoft.com/id-id/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook?)
   - You can choose @hotmail.com or @outlook.com
   - Create a password
   - Save your email and password on `config.json`

5. Create or edit a `congfig.json` file with your configuration:
    ```json
    {
        "email": "yourEmail@hotmail.com",
        "password": "yourPassword",
        "referrals": "yourReferral",
        "count": 50
    }
    ```

## Usage

1. Run the application:
    ```bash
    python main.py
    ```

2. Go to outlook inbox `(junk)` and find email from pixelverse 
3. Open the email and add pixelverse OTP email to main inbox `(add / move to inbox)`

#### Note : Make sure on the `first run` the otp email from pixelverse is not in your junk mail.

![image](https://github.com/jawikas/pixelverse-dashboard/assets/63976518/72d8e4ed-b1d3-4c3e-9733-0483945189d5)

## Configuration

### Proxy Management

The proxy management system is designed to fetch, validate, and rotate proxies to avoid rate limiting. You can modify the proxy sources in the `Proxy` class in `proxy.py`.

### Email Generation

The `generate_emails` method in the `Core` class uses the Faker library to generate realistic email addresses. You can customize the email generation logic as needed.

### Core Operations

The `Core` class handles all interactions with the Pixelverse API, including requesting OTPs, verifying OTPs, setting referrals, updating profiles, purchasing pets, selecting pets, and claiming rewards. Ensure that your configuration in the `config.json` file is accurate to avoid issues.


## License
This project is licensed under the NONE License.

## Contact
If you have any questions or suggestions, please feel free to contact at [ https://t.me/itsjaw_real ].

## Thanks to

unknown source but thanks

---

**Disclaimer**: This application is for educational purposes only. Use it responsibly and at your own risk.
