# -*- coding: utf-8 -*-
import sys

import yaml
from loguru import logger

#####################################################################################
LOG_TEMPLATE = "mytemplate2"
LOG_CONFIG_PATH = "config_log.yaml"


#####################################################################################
def logger_setup(log_config_path: str = None, log_template: str = "default", **kwargs):
    """ Generic Logging setup

      Overide logging using loguru setup
      1) Default Config using log_level and log_format.
      2) Custom config from log_config_path .yaml file
      3) Use shortname log, log2, logw, loge for logging output

    Options
    #logger.add(log_file_name,level=level,format=format,
    #    rotation="30 days", filter=None, colorize=None, serialize=False, backtrace=True, enqueue=False, catch=True)


    """
    try:
        with open(log_config_path, "r") as fp:
            cfg = yaml.safe_load(fp)

    except Exception as e:
        print("Using Default logging setup")
        cfg = {"log_level": "INFO", "handlers": {"default": [{"sink": "sys.stdout"}]}}

    ########## Parse handlers  ####################################################
    globals_, handlers = cfg, cfg.pop("handlers")[log_template]

    for handler in handlers:
        if handler["sink"] == "sys.stdout":
            handler["sink"] = sys.stdout
        elif handler["sink"] == "sys.stderr":
            handler["sink"] = sys.stderr

        # override globals values
        for key, value in handler.items():
            if key in globals_:
                globals_[key] = value

        handler.update(globals_)

    ########## Addon config  ##############################################
    logger.configure(handlers=handlers)
    logger.level("TIMEIT", no=22, color="<cyan>")
    return logger


##### Initialization ####################################################
logger_setup(log_config_path=LOG_CONFIG_PATH, log_template=LOG_TEMPLATE)


def log(*s):
    logger.info(",".join([str(t) for t in s]))


def log2(*s):
    logger.debug(",".join([str(t) for t in s]))


def log3(*s):  ### Debuggine level 2
    logger.log("debug2", ",".join([str(t) for t in s]))


def logw(*s):
    logger.warning(",".join([str(t) for t in s]))


def logc(*s):
    logger.critical(",".join([str(t) for t in s]))


def loge(*s):
    logger.error(",".join([str(t) for t in s]))


def test():
    log("info")
    log2("debug")


if __name__ == "__main__":
    test()
