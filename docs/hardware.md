# Hardware recommendations

For simplicity, we recommend a system which has been tested to work. Feel free to change this. But note that some configuration would be needed.


## OS and computer recommendation

The computer does not have to be overly powerful. We assume a unix type system, which has been tested on a Linux machine.

We have used a [Dell Precision 5720](http://www.dell.com/en-us/work/shop/productdetails/precision-5720-aio/xctop5720aious "Dell Precision 5720 Store Page"), with 16 GB of RAM, i5-7600 processor and Ubuntu 16.04 pre-installed.

The following commands should be run in a terminal `Ctrl + Alt + T` then be base software is up to date.

````bash
sudo apt-get update

sudo apt-get upgrade
````

## Storage requirements

The image pyramid is large, approximately 12 TB in size.
This will need to be mounted (not symlinked), at a specific location.
For these purposes, we assume that you have a RAID setup mounted at `/FAFB_RAID`.

We have tested it with an external RAID-enclosure and have gotten adequate performance for CATMAID.

The details of our setup is a [Mobius™ 5-Bay FireWire 800 enclosure](https://oyendigital.com/hard-drives/store/3R5-EB3-M.html), and five [Seagate ST4000NM0035 4 TB HDDs](https://www.amazon.com/Seagate-ST4000NM0035-Enterprise-7200RPM-128MB/dp/B01FRC1GRQ/ "available, for example here") which gives acceptable performance.
Once these drives are inserted, these should be formatted, which is described [in the user manual](https://oyendigital.com/downloads/manuals/mobius_manual.pdf).

The disks should then be setup to allow easy mounting in the future.
Upon connecting to the computer, these will then need formatting.
One should first determine where the drive is located
````
lsblk --output NAME,LABEL,UUID,MOUNTPOINT,SIZE
````

This will give an output along the lines of:

````
NAME   LABEL     UUID                                 MOUNTPOINT                SIZE
sda                                                                           465.8G
├─sda1 ESP       CA75-A471                            /boot/efi                 600M
├─sda2 OS        D88D-F5C7                                                        3G
├─sda3 UBUNTU    8cec81af-9187-4e4c-9e71-1efbf75053b7 /                       430.5G
└─sda4           da65590e-d2ce-42ad-9422-04697f272ed5 [SWAP]                   31.7G
sdb                                                                            14.6T
````

You will want to look for a drive which has no LABEL, and a size of 14.6T.

Assuming this is located at `sdb` these can be formatted as following **NB: double check this location and change as appropriate, if it is listed as sdc change all sdb to sdc**
````
sudo parted -a optimal /dev/sdb mklabel gpt
sudo parted -a optimal /dev/sdb -- mkpart primary ext 1 -1
sudo mkfs.ext4 -b 4096 -i 65536 -L FAFB_RAID /dev/sdb1 -m 0
````

The location of the drives should then be set up and the drives mounted.
````
sudo mkdir /FAFB_RAID
sudo mount -L FAFB_RAID /FAFB_RAID
sudo chown -R $USER:$USER /FAFB_RAID
````

