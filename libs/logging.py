import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class CustomHttpJsonHandler(logging.Handler):

    def __init__(self, url: str, silent: bool = True):
        '''
        Initializes the custom http handler
        Parameters:
        url (str): The URL that the logs will be sent to
        silent (bool): If False the http response and logs will be sent
                       to STDOUT for debug
        '''
        self.url = url
        self.silent = silent

        # sets up a session with the server
        self.MAX_POOLSIZE = 100
        self.session = session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json'
        })
        self.session.mount('https://', HTTPAdapter(
            max_retries=Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=[403, 500]
            ),
            pool_connections=self.MAX_POOLSIZE,
            pool_maxsize=self.MAX_POOLSIZE
        ))

        super().__init__()

    def emit(self, record):
        '''
        This function gets called when a log event gets emitted. It recieves a
        record, formats it and sends it to the url
        Parameters:
            record: a log record
        '''
        log_entry = self.format(record)
        response = self.session.post(self.url, data=log_entry)

        if not self.silent:
            print(log_entry)
            print(response.content)
