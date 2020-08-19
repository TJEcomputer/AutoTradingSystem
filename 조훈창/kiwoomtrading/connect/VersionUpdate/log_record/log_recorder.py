import logging , datetime
import logging.handlers

def recorder_time(name):
    dt = datetime.datetime.now()
    nowdate = dt.strftime('%Y-%m-%d')

    log_filename='c:/users/TJ/Desktop/python/kiwoomtrading/connect/VersionUpdate/log_record/{}-versionupdate.log'.format(nowdate)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s : %(message)s ", "%Y-%m-%d %H:%M:%S")

    file_handler = logging.handlers.TimedRotatingFileHandler(filename=log_filename, when='midnight', encoding='utf-8')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


