#import client
from .client import ClientTest
import logging

def run():
        # init alice client
        alice = ClientTest('alice', '54321', 'localhost', 5000)
        alice.subscribe()
        alice.register_keys(1, 1)

        message = input("Start message to bob: \n")
        alice.publish(message, 'bob')
        while True: #just for keep terminal and get value from keyboard
            message = input("")
            alice.publish(message, 'bob')

if __name__ == '__main__':
    logging.basicConfig()
    run()