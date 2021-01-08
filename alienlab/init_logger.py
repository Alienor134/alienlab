import colorlog, logging
import datetime
import shutil


# Use: 
# from alienlab.init_logger import logger
# logger.name = "file_name"
# logger.debug/info/warning/error/critical

"""
logging.basicConfig(filename="temp.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)



OUTPUT = 5
logging.addLevelName(OUTPUT, 'OUTPUT')
formatter = colorlog.ColoredFormatter(
                                log_colors={
                                    'DEBUG':    'cyan',
                                    'INFO':     'green',
                                    'WARNING':  'yellow',
                                    'ERROR':    'red',
                                    'CRITICAL': 'red,bg_white',
                                    'OUTPUT': 'yellow',
                                })

handler = logging.StreamHandler()
handler.setFormatter(formatter)



logger = logging.getLogger('Running')
logger.handlers = []
logger.propagate = False
logger.addHandler(handler)
logger.setLevel('OUTPUT')
"""

def get_logger(logger_name, file_location):

        # create logger 
        log = logging.getLogger(logger_name)
        log.setLevel(level=logging.DEBUG)

        # create formatter and add it to the handlers
        format_str = '%(asctime)s.%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        cformat = '%(log_color)s' + format_str
        colors = {'DEBUG': 'green',
                'INFO': 'cyan',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_purple'}
        formatter = colorlog.ColoredFormatter(cformat, date_format,
                                          log_colors=colors)

        # create file handler for logger.
        fh = logging.FileHandler(file_location + "/" + str(datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_')) + "archive.log")
        fh.setLevel(level=logging.DEBUG)
        fh.setFormatter(formatter)
        # reate console handler for logger.
        ch = logging.StreamHandler()
        ch.setLevel(level=logging.DEBUG)
        ch.setFormatter(formatter)

        # add handlers to logger.
        log.addHandler(fh)

        log.addHandler(ch)
        return  log 

logger = get_logger('temp', 'logs')

def move_log(logger, target):
    source = logger.handlers[0].baseFilename
    logging.shutdown()
    shutil.copy(source, target)