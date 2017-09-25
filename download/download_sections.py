#!/usr/bin/env python3

#
# This script will download data tiles associated with the full fly brain and expand them to local storage.
# This is based on download_sections.sh and is based on iterating through sections 1-7062
#

import argparse
import csv
import io
import tarfile
import hashlib
import os

import requests
import progressbar

BUFFER_SIZE=1024*1024

class StreamWrapper:
    """Wrapper to print status bars & calculate checksums on the tar inputs stream."""
    def __init__(self, stream, total_size=0, name=""):
        self.stream = stream
        self.total_size = total_size
        self.bytes_read = 0
        self.hash = hashlib.md5()
        widgets = [name, ' ', progressbar.Percentage(), ' ', progressbar.Bar(), ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
        self.pbar =  progressbar.ProgressBar(widgets=widgets, max_value=self.total_size).start()
        
    def read(self, bufsize=BUFFER_SIZE):
        result = self.stream.read(bufsize)
        self.hash.update(result)
        self.bytes_read += len(result)
        self.pbar.update(self.bytes_read)
        return result

    def gethash(self):
        return self.hash

    def close(self):
        # Keep reading the data beyond the end of the tar stream to get the correct hash.
        while self.read():
            continue
        self.pbar.finish()

class InvalidChecksum(Exception):
    def __init__(self):
        pass

class CheckpointFile():
    """Naively store a list of downloaded sections in a text file to allow for resumption of downloads."""
    def __init__(self, filename):
        self.filename = filename
        self.sections = set()
        self.readCheckpoint()

    def __contains__(self, section):
        return section in self.sections

    def addSection(self, section):
        self.sections.add(section)

    def readCheckpoint(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    self.sections.add(int(line.strip()))
    
    def writeCheckpoint(self):
        with open(self.filename, "w") as f:
            for section in sorted(self.sections):
                f.write("%d\n" % section)
            

def get_checksums(url):
    print("Downloading hash file...")
    reader = csv.reader(io.StringIO(requests.get(url).text), delimiter='\t')
    checksums = {}
    for checksum, filename in reader:
        checksums[filename] = checksum
    print("Done")
    return checksums

def get_single_file(url, dest, dryrun=False):
    """Download a single file."""
    print("Downloading %s" % url)
    r = requests.get(url, stream=True)
    if not dryrun:
        print("Saving to %s" % dest)
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(chunk_size=BUFFER_SIZE): 
                if chunk:
                    f.write(chunk)

def get_archive(url, path, checksum=None, dryrun=False, name=""):
    print("Downloading %s" % url)
    r = requests.get(url, stream=True)
    total_size = int(r.headers['content-length'])
    stream = StreamWrapper(r.raw, total_size=total_size, name=name)
    tar = tarfile.open(mode='r|', fileobj=stream, bufsize=BUFFER_SIZE)
    for tarinfo in tar:
        if tarinfo.name.endswith(".jpg"):
            if not dryrun:
                tar.extract(tarinfo, path, set_attrs=False)
    tar.close()
    stream.close()
    if stream.gethash().hexdigest() != checksum:
        print("Warning: Hash values do not match for %s" % url)
        print("Got %s, expected %s" % (stream.gethash().hexdigest(), checksum))
        raise InvalidChecksum()
    else:
        print("Hashes match (%s)" % (stream.gethash().hexdigest()))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--source", default="http://temca2data.janelia.org", help="Base URL to download data from")
    parser.add_argument("--datapath", required=True, help="Path to store image data")
    parser.add_argument("--checkpointfile", default="checkpoint.txt", help="Filename (under datapath) to checkpoint")
    parser.add_argument("--checksumfile", default="temca2_md5.md5", help="Filename (under source) to find md5 file")
    parser.add_argument("--dryrun", default=False, action="store_true", help="Read-only: do not extract tar archives")
    parser.add_argument("--first", default=1, type=int, help="First section to download")
    parser.add_argument("--last", default=7062, type=int, help="Last section to download")
    parser.add_argument("--version", default=14, type=int, help="Alignment version number")

    args = parser.parse_args()

    checksums = get_checksums("%s/v%d/%s" % (args.source, args.version, args.checksumfile))
    checkpoint = CheckpointFile("%s/%s" % (args.datapath, args.checkpointfile))

    # Download the empty tile.  This should be part of the docker image.
    get_single_file("%s/images/black.jpg" % args.source, "%s/black.jpg" % args.datapath, args.dryrun)

    for layer in range(args.first, args.last+1):
        if layer in checkpoint:
            print ("Already downloaded %d; skipping" % layer)
            continue
        filename = "temca2.%d.0.%d.tar" % (args.version, layer)
        layer_url = "%s/v%d/%s" % (args.source, args.version, filename)
        get_archive(layer_url, args.datapath, checksum=checksums[filename], dryrun=args.dryrun, name=str(layer))
        checkpoint.addSection(layer)
        checkpoint.writeCheckpoint()

if __name__ == "__main__":
    main()
