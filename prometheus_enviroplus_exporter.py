#!/usr/bin/env python3

import time
import os
from prometheus_client import start_http_server, Gauge, Enum
import requests
from bme280 import BME280
from enviroplus import gas
from enviroplus.noise import Noise

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

# Temp sensor
bme280 = BME280()
# Light/prox sensor
ltr559 = LTR559()
# Noise sensor
noise = Noise()

port = 9892

# Check to see if gas sensor is present. 
try:
  test = gas.read_oxidising()
except:
  nogas=1

# Prometheus metrics
TEMP = Gauge('enviroplus_temperature', 'Current temperature in C')
PRESSURE = Gauge('enviroplus_pressure', 'Barometric pressure in hPa')
HUMIDITY = Gauge('enviroplus_humidity', 'Current humidity %')
LIGHT = Gauge('enviroplus_light', 'Light level in lux')
PROX = Gauge('enviroplus_proximity', 'Proximity')
if (nogas != 1):
    OXIDISED = Gauge('enviroplus_oxidised', 'Oxidisation in kO')
    REDUCED  = Gauge('enviroplus_reduced', 'Reduced gas in KO')
    NH3 = Gauge('enviroplus_nh3', 'NH3 level in kO')
NOISE_L = Gauge('enviroplus_noise_l', 'Low-Frequency Noise Level in db(?)')
NOISE_M = Gauge('enviroplus_noise_m', 'Mid-Frequency Noise Level in db(?)')
NOISE_H = Gauge('enviroplus_noise_h', 'High-Frequency Noise Level in db(?)')
NOISE_A = Gauge('enviroplus_noise_a', 'Noise Amplitude')

if __name__ == '__main__':
    # Start http server
    start_http_server(port)
    # Metrics generation loop.
    while True:
        TEMP.set(bme280.get_temperature())
        LIGHT.set(ltr559.get_lux())
        PROX.set(ltr559.get_proximity())
        PRESSURE.set(bme280.get_pressure())
        HUMIDITY.set(bme280.get_humidity())
        if (nogas != 1):
            OXIDISED.set(gas.read_oxidising())
            REDUCED.set(gas.read_reducing())
            NH3.set(gas.read_nh3())
        low, mid, high, amp = noise.get_noise_profile()
        NOISE_L.set(low)
        NOISE_M.set(mid)
        NOISE_H.set(high)
        NOISE_A.set(amp)
