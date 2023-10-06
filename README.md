# Bendroid

Using Benford's Law to detect Android malware.

## Setup
1. Create new conda environment using `conda create -n <name> -f environment.yml`
    * At the moment, this is only compatible with Windows
2. Create `.ben` file in the format of `.example.ben`
3. Edit `project_dir` in `config.ini`
4. Run the `download_apks_dataset.ipynb` notebook to compile the benign and malign APKs sample list
    * This includes downloading/unzipping the CSV, converting it to HDF5 for faster access, and collecting benign and malign samples into `samples.csv`
5. Run `download_apks.py` to download all APKs in `samples.csv`