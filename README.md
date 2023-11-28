# Inverter2iDMpump

## External Sources
- [https://github.com/robertdiers/kostal_idmpump](https://github.com/robertdiers/kostal_idmpump)
- [https://github.com/robertdiers/solar-monitor](https://github.com/robertdiers/solar-monitor)

## Setup:
* SMA inverter (SUNNY TRIPOWER 10.0 SE)
* OpenDTU for Hoymiles-inverter
* iDM Heat Pump AERO SLM 6-17 with "solar input" feature
* Raspbery Pi 3B+ with 2023-10-10-raspios-bookworm-arm64-lite.img

## main Python scripts (startup and cron triggered):
* init.py - initializes TimescaleDB tables as they are removed when device restarts
* inverter2idm.py - collect metrics, store them to database and write them to the iDM-pump, if a limit is reached

## Podman
```
sudo apt install -y podman buildah qemu-user-static python3-paho-mqtt python3-pymodbus python3-psycopg2
./image.sh
```

## TimescaleDB (please define your own password)
Using a ramdisk /mnt/ramdisk to store data in memory, sd card doesn't have to store it:
```
podman run -d --restart always --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password --mount type=tmpfs,destination=/mnt/ramdisk timescale/timescaledb:latest-pg13
```

## Grafana (please define your own password)
Dashboard JSON is placed in this repo:
create a directory grafanadata
```
podman run -d --name grafana --volume "$PWD/grafanadata:/var/lib/grafana" -p 3000:3000 --restart always grafana/grafana:latest
```

## EMQX (MQTT broker, please define your own password)
```
podman run -d --name emqx -p 18083:18083 -p 1883:1883 -v /tmp/data --restart always docker.io/library/emqx
```

## Cron 
add this to your /etc/crontab
```
# start container after reboot
@reboot	     pi podman start --all
# start python metric-script every 10 min 
*/10 * * * * pi /home/pi/inverter2idmpump/cron.sh 1>/dev/null 2>/dev/null
```

enable lingering for pi-user
```
loginctl enable-linger
```


