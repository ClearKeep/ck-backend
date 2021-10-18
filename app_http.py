from utils.config import get_system_config
from utils.logger import *
from src.controllers import app
import asyncio

async def start_http_server():
    # start http api
    http_port = get_system_config()['http_port']
    print("HTTP listening on port {}..".format(http_port))
    logger.info("HTTP listening on port {}..".format(http_port))
    app.run(host="0.0.0.0", port=str(http_port), threaded=False, processes=3, debug=False)


if __name__ == '__main__':
    asyncio.run(start_http_server())
