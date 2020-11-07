import logging , datetime
import logging.handlers
import time
import os

class Log:
    def __init__(self,name):
        self.name = name
        self.start = time.time()
        dir = ['full','DL','ML','RL','API']
        for i in dir:
            path = '.\\log\\'
            if not os.path.exists(path + i):
                os.makedirs(path+i)
    def dir_recorder(self,name=None):
        dt = datetime.datetime.now()
        loggername=self.name
        nowdate = dt.strftime('%Y%m%d')
        path = '.\\log\\full\\'
        if path is not None:
            path = '.\\log\\' + name +'\\'
        log_filename='{}.log'.format(nowdate)
        full_path = path + log_filename

        logger_dir = logging.getLogger(loggername)
        logger_dir.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s : %(message)s ", "%Y-%m-%d %H:%M:%S")

        file_handler = logging.handlers.TimedRotatingFileHandler(filename=full_path, when='midnight', encoding='utf-8')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger_dir.addHandler(stream_handler)
        logger_dir.addHandler(file_handler)
        return logger_dir

    def ML_recorder(self,text):
        log_full = self.dir_recorder('full')
        log_dir = self.dir_recorder('ML')
        log_full.info(text)
        log_dir.info(text)
    def DL_recorder(self,text):
        log_full = self.dir_recorder('full')
        log_dir = self.dir_recorder('DL')
        log_full.info(text)
        log_dir.info(text)
    def API_recorder(self,text):
        log_full = self.dir_recorder('full')
        log_dir = self.dir_recorder('API')
        end = time.time()
        min = int((end - self.start) // 60)
        sec = int((end - self.start) % 60)
        msg = f'진행 시간 - {str(min).zfill(2)}:{str(sec).zfill(2)} | {text} '
        log_full.info(msg)
        log_dir.info(msg)
    def RL_recorder(self,text):
        log_full = self.dir_recorder('full')
        log_dir = self.dir_recorder('RL')
        end = time.time()
        min = int((end - self.start) // 60)
        sec = int((end - self.start) % 60)
        msg = f'진행 시간 - {str(min).zfill(2)}:{str(sec).zfill(2)} | {text} '
        log_full.info(msg)
        log_dir.info(msg)

