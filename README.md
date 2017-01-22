# retrofitting-ip-doorbell-notify

[TOC]

## setup

### install middleware

```
$ sudo apt-get install python-rpi.gpio
```

### make configuration files

#### properties.json
create **properties.json** file in the same directory as main.py.

```
{
    "line_api_token" : "YOUR_TOKEN"
}
```

### auto run

open `/etc/rc.local` file and insert a follow line at before of `exit 0`

```text:/etc/rc.local
python /home/pi/src/door-line-notify-python/main.py &

```


## execute

```
$ sudo python main.py
```