import datetime as dt
import http.client
import http.client
import logging
import os
import re
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import pytz


def setup_logging(log_file_name):
    class PackagePathFilter(logging.Filter):
        def filter(self, record):
            pathname = Path(record.pathname)
            record.relativepath = None
            abs_sys_paths = map(os.path.abspath, sys.path)
            for path in sorted(abs_sys_paths, key=len, reverse=True):  # longer paths first
                if pathname.as_posix().startswith(Path(path).as_posix()):
                    # TODO: fix this hard-code "ck-backend-internal"
                    record.relativepath = os.path.relpath(str(pathname), path) if 'ck-backend' in str(
                        pathname) else str(pathname)
                    break
            return True

    class FormatterCustom(logging.Formatter):
        def __init__(self, *args, **kwargs):
            fmt = '[%(levelname).1s][%(asctime)s][%(name)30s] ' \
                  '"%(relativepath)s:%(lineno)d".%(funcName)s()>>> %(message)s'
            super().__init__(fmt=fmt, *args, **kwargs)

        def formatTime(self, record, *_unused_args, **_unused_kwargs) -> str:
            # TODO: Low-priority/ fix VN timezone hard-code
            record_datetime = dt.datetime.fromtimestamp(record.created, tz=pytz.timezone("Asia/Ho_Chi_Minh"))
            main_str = record_datetime.strftime("%a %y%m%d %H%M-%S.%f")[:-3]
            timezone_offset = record_datetime.strftime("%z")
            return f"{main_str}{timezone_offset}"

    # TODO: use 'midnight' for long-running mode
    # when='midnight',
    # Use when='S' and interval=3 to test rotating logs,
    # use backupCount=10 when need to delete old logs
    timed_rotating_file_handler = TimedRotatingFileHandler(log_file_name, when='H', interval=1, backupCount=0,
                                                           encoding='utf8')
    timed_rotating_file_handler.suffix = "%Y%m%dT%H-%M-%S.log"  # Force .log file extension
    timed_rotating_file_handler.extMatch = re.compile(r"^.*\d{2}-\d{2}-\d{2}.log$")  # For auto-delete old logs

    console_handler = logging.StreamHandler()
    timed_rotating_file_handler.addFilter(PackagePathFilter())
    console_handler.addFilter(PackagePathFilter())
    timed_rotating_file_handler.setFormatter(FormatterCustom())
    console_handler.setFormatter(FormatterCustom())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(timed_rotating_file_handler)
    root_logger.addHandler(console_handler)

    # TODO: IMP/URGENT/ fix this hard-code debug mode
    logging.getLogger("asyncio").setLevel(logging.DEBUG)

    if root_logger.getEffectiveLevel() <= logging.DEBUG:
        # when logging at debug level, make http.client extra chatty too
        # http.client *uses `print()` calls*, not logging.
        http.client.HTTPConnection.debuglevel = 1
        http_client_logger = logging.getLogger("http.client")

        def print_to_log(*args, **_unused_kwargs):
            # TODO: clear this
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
