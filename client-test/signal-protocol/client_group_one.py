from .client_group import *
import logging

def run():
        # init bob client
        one = ClientGroupTest('3de37c55-05a6-43c8-939b-32df536dabc7', 1, 'localhost', 5000)
        one.subscribe()
        one.register_group_keys("fdd4270d-cd4b-4358-98ab-8244a8afd39d")
        message = input("Start message to group: \n")
        one.publish(message, "test-group")
        while True: #just for keep terminal and get value from keyboard
            message = input("")
            one.publish(message, "test-group")

if __name__ == '__main__':
    logging.basicConfig()
    run()