from crontab import CronTab
import os
from utils.logger import *


def cron_tab_update_turn_server():
    try:
        # run in the first time
        os.system('ENV=production /usr/bin/python3 -m client.client_nts')
        # set cronjob in next time
        cron = CronTab(user='ubuntu')
        cron.remove_all()
        job = cron.new(command='cd /home/ubuntu/prod-clk328/ck-backend && ENV=production /usr/bin/python3 -m client.client_nts')
        #job.day.every(1)
        job.setall('0 0 * * *')
        cron.write()
        logger.info("Cronjob cron_tab_update_turn_server set")

    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    cron_tab_update_turn_server()
