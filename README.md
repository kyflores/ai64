# ai64
Running models of the Beaglebone AI64 Debian image

`host` folder contains code for use on a desktop PC, such as stuff
to prepare the BBAI64 rootfs, train a model, or quantize + calibrate a model

`device` folder contains code for use on the BBAI64 board, which may include
scripts for building TI components over the stock debian image, or code
to run models.

## Imaging the board
Two types of images are available to load onto an SD card.
[See the forum for a complete set of download links](https://forum.beagleboard.org/t/arm64-debian-11-x-bullseye-monthly-snapshots-2023-10-07/32318)
* Images with `flasher` in the name don't run a full desktop from SD card, instead they flash
  the internal emmc so the system can boot from that.
* Regular images boot and run from SD card.

I'm using `bbai64-debian-11.8-xfce-edgeai-arm64-2023-10-07-10gb.img.xz`, which has the edgeai
apps deployed to `/opt`.

## Building with the debian image
The BeagleBoard debian image can be used for a container to allow building stuff on a host
machine.
```
# Uncompress
unxz bbai64-debian-11.8-xfce-edgeai-arm64-2023-10-07-10gb.img.xz

# Unpacks 0.fat and 1.img, which are the two partitions in the image
7z x bbai64-debian-11.8-xfce-edgeai-arm64-2023-10-07-10gb.img

# Mount the image for reading
mkdir -p bbai64_root
sudo mount -o ro 1.img bbai64_root/

# Copy everything into a new dir
mkdir -p container
sudo cp -r bbai64_root/* container/

# Umount the image
sudo umount bbai64_root
```

Now, the device rootfs is in `container/` so we can run stuff in it. Since the device
is aarch64, and you are presumably on an AMD64 workstation, first `apt-get install qemu-user-static`,
which enables arm binaries in user mode.

Then to enter the container:
```
sudo systemd-nspawn \
    -D container \
    --bind-ro /etc/resolv.conf:/etc/resolv.conf
```
Add `--user debian` to run as user.

# Megvii YOLOX
export YOLOX_DATADIR=/home/kyle/Pictures/coco/
python -m yolox.tools.train -n yolox-s-ti-lite -d 1 -b 64 --fp16 -o [--cache]

python3 tools/export_onnx.py --output-name yolox_s.onnx -n yolox_s_ti_lite -c /home/kyle/Documents/bbai/edgeai-yolox/yolox-s-ti-lite_39p1_57p9_checkpoint.pth --export-det

# Quantizing
* clone edgeai-tidl-tools
* `SOC=am68pa bash setup.sh`


## Prebuilt packages
https://software-dl.ti.com/jacinto7/esd/tidl-tools/09_01_00_00/OSRT_TOOLS/ARM_LINUX/ARAGO/dlr-1.13.0-py3-none-any.whl
https://software-dl.ti.com/jacinto7/esd/tidl-tools/09_01_00_00/OSRT_TOOLS/ARM_LINUX/ARAGO/onnxruntime_tidl-1.14.0-cp310-cp310-linux_aarch64.whl
