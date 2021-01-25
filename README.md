*I did this for job interview. Failed, but it was fun. Got permission to share*

# Currency conversion service without external python dependencies

## How to run:

1. Set service's address and port in settings.ini. Optionally run tests.py to check if configuration is correct. It should pass the first test, then fail
2. Launch server.py: python ./server.py
3. Run tests.py to check if everything works

Server expects to receive POST-requests with jsons lookining like {"Original_Currency": "short name of original currency in capslock. Say, 'USD'", "Converted_Currency": "short name of currency you are trying to convert it to. Say, 'RUB'", "Amount": amount of money you want to convert}. Answers with very same json, except it has additional 'Converted_Price' field containing the price of specified amount of original currency in new currency
