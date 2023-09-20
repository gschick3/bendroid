# Bendroid

Using Benford's Law to detect Android malware.

## Setup
1. Create new conda environment using `conda create -n <name> -f environment.yml`
    * At the moment, this is only compatible with Windows
2. Create `.ben` file in the format of `.example.ben`
3. Run the `download_apks.ipynb` notebook to get latest csv of all Androzoo APKs, unzip it, and download APKs (these steps will take a few hours)