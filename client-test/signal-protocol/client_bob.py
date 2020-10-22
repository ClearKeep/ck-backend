#import client
from .client import *
import logging

def run():
        # init bob client
        bob = ClientTest('bob', '54321', 'localhost', 5000)
        bob.subscribe()
        bob.register_keys(1, 1)
        message = input("Start message to alice: \n")
        bob.publish(message, 'alice')
        while True: #just for keep terminal and get value from keyboard
            message = input("")
            bob.publish(message, 'alice')

if __name__ == '__main__':
    logging.basicConfig()
    run()