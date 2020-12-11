from .client_group import *
import logging

def run():
        # init bob client
        two = ClientGroupTest('two', 2, 'localhost', 5000)
        two.subscribe()
        two.register_group_keys("test-group")
        message = input("Start message to group: \n")
        two.publish(message, "test-group")
        while True: #just for keep terminal and get value from keyboard
            message = input("")
            two.publish(message, "test-group")

if __name__ == '__main__':
    logging.basicConfig()
    run()