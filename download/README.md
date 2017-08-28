# FAFB Download Script

This script will download the entire traceable dataset (~12TB).
It will do so one section at a time, checking 

Note that the ```--dryrun``` flag can be used to test the download without extracting any of the images to disk.

## Usage
### Sample usage (direct with Python)
First, install required libraries:

```
pip3 install requests progressbar2
```

Next, run the script specifying the directory you wish the data to be saved:

```
python3 download_sections.py --datapath /path/to/save/data/to
```

### Sample usage (via docker image)
_Suggested for MacOS without Python3 installed_

Build the docker image:
```
docker build . -t fafb_download
```

Then run the container, being sure to mountain the destination volume:
```
docker run --volume /path/to/save/data/to:/data --rm fafb_download --datapath /data --dryrun
```

## Notes
### Resuming the download
The script will automaticle create a file called ```checkpoints.txt``` in the download directory to keep track of complete sections.  When resumed, the script will resume from where it left off.