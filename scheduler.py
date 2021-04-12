from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import logging.handlers
from datetime import datetime, timedelta
from Crawler import BlogSpider
import os
import pathlib
import shutil
import requests
#### Variables ###############
BASE_DIR = str(pathlib.Path().absolute())


##### Logging configuration ######################

logfile_name = 'request.log'
logging.basicConfig(filename=logfile_name, level=logging.DEBUG, format='%(asctime)s | %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p')
handler = logging.handlers.RotatingFileHandler(
    logfile_name, maxBytes=20000000, backupCount=5)
logging.getLogger().addHandler(handler)
##### Logging configuration ######################

##### Tarea que se ejecuta cada minuto ######################

def delete_folders(path_to_delete):
    shutil.rmtree(path_to_delete) if os.path.isdir(path_to_delete) else print('deleted')

def task():
    logging.info("Ejemplo de restistro de un procedimiento normal")
    print('Start task %s' % datetime.now())
    
    banner = os.path.abspath("./assets/banner")
    news = os.path.abspath("./assets/news")
    contracts = os.path.abspath("./assets/contracts")

    if os.path.isfile(BASE_DIR+'/assets/home.json'):
        os.remove(BASE_DIR+'/assets/home.json')
        print('deleted')

    delete_folders(banner)
    delete_folders(contracts)
    delete_folders(news)

    os.system('scrapy runspider Crawler.py -o assets/home.json')
    logging.error("Error %s" % 'Ejemplo de registro de un error')

##### Tarea que se ejecuta cada minuto ######################


##### Displarador de la tarea ######################
sched = BlockingScheduler()
sched.add_job(task, 'interval', seconds=60)
sched.start()
##### Displarador de la tarea ######################
