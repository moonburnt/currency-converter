# Server that runs converter

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as up
import cgi
import json
import logging
from sys import exit
from converter import Converter as cv

PROGNAME = "USD to RUB exchange service"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(name)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S'))
log.addHandler(handler)

class ConversionServer(BaseHTTPRequestHandler):
    def set_headers(self):
        '''Setting up headers'''
        log.debug(f"Setting up headers")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def send_answer(self, answer_dictionary):
        '''Receives dic(answer_dictionary), preserves it and sends to whoever made request'''
        log.debug(f"Processing answer")
        self.set_headers()

        response = json.dumps(answer_dictionary)
        log.debug(f"Message is: {response}, attempting to send")
        self.wfile.write(bytes(response, "utf-8"))
        log.debug(f"Successfully sent answer")

    def send_error(self):
        '''Sends standart 400 error'''
        log.debug('Invalid content, sending error 400')
        self.send_response(400)
        self.end_headers()

    def do_GET(self):
        '''Answering get requests'''
        log.debug(f"Got GET request, processing answer")
        dic = {'status': 'up'}
        self.send_answer(dic)

    def do_POST(self):
        '''Answering post requests'''

        log.debug(f"Got POST request, determining its type")
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        if ctype != 'application/json':
            self.send_error()
            return

        log.debug('Determining content-type length')
        length = int(self.headers.get('content-length'))
        log.debug('Getting post content')
        raw_post_content = up.parse_qsl(self.rfile.read(length), keep_blank_values=1)
        log.debug(f"Raw post content is {raw_post_content}. Getting json")
        raw_json, trash = raw_post_content[0]
        log.debug(f"Raw json is {raw_json}, turning into python dictionary")
        data = json.loads(raw_json)
        log.debug(f"Received data is {data}. Processing")

        try:
            converter = cv()

            oc = data["Original_Currency"]
            cc = data["Converted_Currency"]
            amount = data["Amount"]

            converted_price = converter.convert(oc, cc, amount)
            log.debug(f"Converted price is {converted_price}")
            data['Converted_Price'] = converted_price
        except Exception as e:
            log.error(f"An error has occured: {e}")
        else:
            self.send_answer(data)

        self.send_error()

if __name__ == "__main__":
    import configparser

    CONFIG = 'settings.ini'

    log.info(f"Attempting to start {PROGNAME}")

    log.info(f"Getting configuration data")
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

    server = HTTPServer((HOSTNAME, PORT), ConversionServer)
    log.info(f"Launching web server on http://{HOSTNAME}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.warning(f"Manually interrupting server")
        server.server_close()
    except Exception as e:
        log.error(f"An error has occured: {e}")
        log.warning(f"Interrupting server due to critical error")
        server.server_close()

    log.info("Server has been stopped")
