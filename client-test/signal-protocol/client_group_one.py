from .client_group import *
import logging

def run():
        # init bob client
        one = ClientGroupTest('one', 1, 'localhost', 5000)
        one.subscribe()
        one.register_group_keys("test-group")
        message = input("Start message to group: \n")
        one.publish(message, "test-group")
        while True: #just for keep terminal and get value from keyboard
            message = input("")
            one.publish(message, "test-group")

if __name__ == '__main__':
    logging.basicConfig()
    run()