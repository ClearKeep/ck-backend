import logging
from logging.handlers import TimedRotatingFileHandler
import http.client

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



handler = logging.FileHandler('thanhpt1-vmo_log.log', 'a+')


handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter(u'%(asctime)s\t%(name)s\t%(levelname)s\t%(pathname)s:%(lineno)d\t%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

console_handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(console_handler)




if logger.getEffectiveLevel() == logging.DEBUG:
    # when logging at debug level, make http.client extra chatty too
    # http.client *uses `print()` calls*, not logging.
    http.client.HTTPConnection.debuglevel = 1

    http_client_logger = logging.getLogger("http.client")

    def print_to_log(*args, **kwargs):
        # TODO:
        # from inspect import getframeinfo, stack
        # caller = getframeinfo(stack()[1][0])
        # http_client_logger.debug(caller.filename, caller.lineno)

        http_client_logger.debug(" ".join(args))

    # monkey-patch a `print` global into the http.client module; all calls to
    # print() in that module will then use our print_to_log implementation
    http.client.print = print_to_log



def create_timed_rotating_log(path):
    # handler = TimedRotatingFileHandler(path,
    #                                    when='midnight',
    #                                    backupCount=1)

    # handler.suffix = "%Y-%m-%d"
    # formatter = logging.Formatter(u'%(asctime)s\t%(name)s\t%(levelname)s\t%(pathname)s:%(lineno)d\t%(message)s')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)

    pass