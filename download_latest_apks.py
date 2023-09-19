from urllib.request import urlretrieve
import progressbar
import gzip, shutil
import os

url = 'https://androzoo.uni.lu/static/lists/latest_with-added-date.csv.gz'
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'APKs', 'latest_with-added-date.csv.gz')

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

path, headers = urlretrieve(url, filename, show_progress_bar)

print("Unzipping...")
with gzip.open(path, 'rb') as f_in:
    with open(path.rstrip('.gz'), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print("Done.")