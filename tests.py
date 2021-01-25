# testing our tool

import urllib
import logging
from sys import exit
import json
import converter
import configparser

CONFIG = 'settings.ini'

#SERVER_ADDRESS = "http://localhost:8080"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(name)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S'))
log.addHandler(handler)

print(f"Checking if content of {CONFIG} is valid")
try:
    log.debug(f"Attempting to parse {CONFIG}")
    cp = configparser.ConfigParser()
    cp.read(CONFIG)

    HOSTNAME = cp['Server']['Host']
    log.debug(f"Got hostname: {HOSTNAME}")
    PORT = int(cp['Server']['Port'])
    log.debug(f"Got port: {PORT}")
except Exception as e:
    log.error(f"An error has occured: {e}")
    log.warning(f"Couldnt process configuration file. Abort")
    exit(1)

SERVER_ADDRESS = f"http://{HOSTNAME}:{PORT}"

print("Testing if our converter works with ints")
converter = converter.Converter()
try:
    x = converter.convert('USD', 'RUB', 5)
    log.debug(f"Got {x}")
    print("Seems like everything is fine!")
except Exception as e:
    log.error(f"An error has occured: {e}")
    print("Looks like something went wrong :( Aborting")
    exit(1)

print("Testing if our converter works with floats")
try:
    x = converter.convert('USD', 'RUB', 3.54)
    log.debug(f"Got {x}")
    print("Seems like everything is fine!")
except Exception as e:
    log.error(f"An error has occured: {e}")
    print("Looks like something went wrong :( Aborting")
    exit(1)

print("Testing how our server handles empty get requests")
try:
    log.debug(f"Sending GET to {SERVER_ADDRESS}")
    response = urllib.request.urlopen(SERVER_ADDRESS)
    data = response.read()
    log.debug(f"Got {data}")
    print("Seems like everything is fine!")
except Exception as e:
    log.error(f"An error has occured: {e}")
    print("Looks like something went wrong :( Aborting")
    exit(1)

print("Testing how our server handles valid post requests")
try:
    message = {"Original_Currency": "USD", "Converted_Currency": "RUB", "Amount": 32}
    jmessage = json.dumps(message)
    encoded_message = bytes(jmessage, 'utf-8')
    headers = {'Content-Type': 'application/json'}
    post_request = urllib.request.Request(SERVER_ADDRESS, encoded_message, headers)
    post_response = urllib.request.urlopen(post_request)
    data = post_response.read()
    log.debug(f"Got {data}")
    print("Seems like everything is fine!")
except urllib.error.HTTPError as e:
    log.debug(f"Got {e}")
    print(f"Server has successfully returned status code {e}")
except Exception as e:
    log.error(f"An error has occured: {e}")
    print("Looks like something went wrong :( Aborting")
    exit(1)

print("Testing how our server handles non-json post requests")
try:
    message = {"Original_Currency": "USD", "Converted_Currency": "RUB", "Amount": 5}
    jmessage = json.dumps(message)
    encoded_message = bytes(jmessage, 'utf-8')
    headers = {'Content-Type': 'application'}
    post_request = urllib.request.Request(SERVER_ADDRESS, encoded_message, headers)
    post_response = urllib.request.urlopen(post_request)
except urllib.error.HTTPError as e:
    log.debug(f"Got {e}")
    print(f"Server has successfully returned status code {e}")
except Exception as e:
    log.error(f"An error has occured: {e}")
    print("Looks like something went wrong :( Aborting")
    exit(1)

print("Testing how our server handles invalid jsons in post requests")
try:
    message = {"Original_Currency": "USD", "Converted_Currency": "RUB"}
    jmessage = json.dumps(message)
    encoded_message = bytes(jmessage, 'utf-8')
    headers = {'Content-Type': 'application/json'}
    post_request = urllib.request.Request(SERVER_ADDRESS, encoded_message, headers)
    post_response = urllib.request.urlopen(post_request)
    print(post_response)
except urllib.error.HTTPError as e:
    log.debug(f"Got {e}")
    print(f"Server has successfully returned status code {e}")
except Exception as e:
    log.error(f"An error has occured: {e}")
    print("Looks like something went wrong :( Aborting")
    exit(1)

print("Successfully passed all available tests!")
