from itertools import dropwhile
import csv
import os
import configparser
from urllib.request import urlretrieve
import progressbar
from dotenv import dotenv_values

env = dotenv_values('.ben')
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(), allow_no_value=True)
config.read('config.ini')

API_KEY = env['ANDROZOO_API_KEY']
APK_DIR = config['PATHS']['apk_dir']

API_URL = 'https://androzoo.uni.lu/api/download?apikey='+API_KEY+'&sha256={SHA}'

pbar = None
def show_progress_bar(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(max_value=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

benign_dir = os.path.join(APK_DIR, 'benign')
malign_dir = os.path.join(APK_DIR, 'malign')
if not os.path.exists(benign_dir):
    os.makedirs(benign_dir)
if not os.path.exists(malign_dir):
    os.makedirs(malign_dir)

with open(os.path.join(APK_DIR, 'sample.csv')) as f:
    reader = csv.DictReader(f)
    # Start from the last APK download, if defined
    for row in dropwhile(lambda x: x['sha256'] != config['ANDROZOO'].get('last_apk_install', fallback=x['sha256']), reader):
        # Set current download to the latest download
        config['ANDROZOO']['last_apk_install'] = row['sha256']
        with open('config.ini', 'w') as conf_file:
            config.write(conf_file)
        
        # Download file into proper directory
        dataset_url = API_URL.format(SHA=row['sha256'])
        file_path = row['sha256'] + '.apk'

        if int(row['vt_detection']) == 0:
            file_path = 'benign/' + file_path
        elif int(row['vt_detection']) > 5:
            file_path = 'malign/' + file_path

        print("Downloading:", row['sha256'])
        urlretrieve(dataset_url, os.path.join(APK_DIR, file_path), show_progress_bar)

# Once the APKs have all been successfully installed, comment out 'last_apk_install
config.remove_option('ANDROZOO', 'last_apk_install')
config.set('ANDROZOO', '; last_apk_install =', None)

with open('config.ini', 'w') as conf_file:
    config.write(conf_file)