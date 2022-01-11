# Prometheus exporter for Pimoroni Enviro+ Hat

This uses the [Pimoroni Enviro+](https://shop.pimoroni.com/products/enviro) HAT to send environmental monitoring stats to Prometheus.

## What Works, and What Doesn't

Usual disclaimer: I am not a programmer, so this may all be suuuuuper messy. 

I did not include support for the particulate matter sensor, since I don't have one of those to test with. 

The other sensors _do_ work. However, I've been unable to find any information (so far) as to what exactly the proximity sensor is measuring, or what the noise sensor is measuring. I assume noise level in db, but I can't find any documentation. Same for amplitude. The examples provided by Pimoroni are inconsistent, too. 

This also doesn't use the screen on the hat at all. 

I _think_ this should work with the regular Enviro (rather than Enviro+) HAT, but I have not tested this. 

## Requirements

1. Obviously, the [HAT](https://shop.pimoroni.com/products/enviro).
2. Raspberry PI. Any Raspberry PI -- this works very well on a Pi Zero.
3. A GPIO extention cable, or some other way to have the HAT not sit directly on the PI. The PI's CPU temperature will affect readings.
4. Prometheus server (obviously).

## Installation

This assumes you'll be using the default 'pi' user. 

1. Set up Raspberry PI with the latest 'lite' version of Raspberry PI OS.
2. Follow the instructions to installing the Pimoroni libraries [here](https://github.com/pimoroni/enviroplus-python/).
3. Install the Prometheus client python library using ```python3 -m pip install prometheus-client```
4. Download ```prometheus_enviroplus_exporter.py``` and put it in ```/usr/local/bin/```. Make sure it is executable.

## Test

Run the program manually using ```/usr/local/bin/prometheus_enviroplus_exporter.py```. If you don't see any errors, congratulations! It's probably working!

By default, the exporter listens on port 9155, so ```curl localhost:9155/metrics``` should show the metrics. 

## systemd

To get the thing to start automatically, download ```prometheus_enviroplus_exporter.service``` and place it in ```/etc/systemd/system/```. Then run ```sudo systemctl enable prometheus_enviroplus_exporter.service```. 

## Prometheus Configuration

This is dependent on your own setup, but I create a JSON file in wherever Prometheus' `base_node` data is (usually `/etc/prometheus_data/base_node`) called `enviro-<location>.json`, and it looks something like this:

```
[
  {
    "targets": [ "<ip address>:9155" ],
    "labels": {
      "hostname": "<hostname>",
      "location": "<location>"
    }
  }
]
```

This allows you to filter by, well, location. 
