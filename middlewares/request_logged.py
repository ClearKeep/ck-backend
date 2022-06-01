import logging
import pprint
from functools import wraps
logger = logging.getLogger(__name__)

def request_logged(func):
    @wraps(func)
    async def deco(*args, **kwargs):
        try:
            # TODO: make more readable log, args,...
            logger.info(f"{func.__qualname__=}, "
                        f"{pprint.pformat(args)=}, "
                        f"{pprint.pformat(kwargs)=}, "
                        f"Request Object Type=<{type(args[1]).__name__}>, "
                        f"Object=<{args[1]}>")
        except Exception:
            logger.exception("Error while log request")
        func_ret = await func(*args, **kwargs)
        logger.info(f"{func_ret=}")
        return func_ret

    return deco
