from utils.logger import *


def request_logged(func):
    async def deco(*args, **kwargs):
        # TODO: thanhpt1-vmo/fix-this
        # Before request handlers
        try:
            print("Request Object Type=", type(args[1]).__name__)
            print(args[1])
            logger.info("Request Object Type=" + type(args[1]).__name__)
            logger.info(args[1])
        except Exception:
            logger.warning("thanhpt1-vmo/TODO-fix-this/Error when request_logged", exc_info=True)
        return await func(*args, **kwargs)

    return deco
