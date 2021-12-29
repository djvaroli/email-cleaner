python3 -m pip install -qq -r requirements.txt && python3 remove_blacklisted_emails.py
printf "TWILIO_ACCOUNT_SID=<>
TWILIO_AUTH_TOKEN=<>
FROM_PHONE_NUMBER=<>
DEFAULT_NUMBER=<>" >> .env