# switchmate

A python-based command line utility for controlling
[Switchmate](https://www.mysimplysmarthome.com/products/switchmate-switches/) switches.

Now with Flask server!

## Installation

	$ sudo pip3 install -r requirements.txt

## Usage

    python3 -m app.switchmate scan [options]
    python3 -m app.switchmate status [options]
    python3 -m app.switchmate <mac_address> status [options]
    python3 -m app.switchmate <mac_address> switch (on | off)
    python3 -m app.switchmate <mac_address> toggle
    python3 -m app.switchmate <mac_address> battery-level
    python3 -m app.switchmate <mac_address> debug

	$ sudo python3 -m app.switchmate scan
	Scanning...
	Found Switchmates:
	ee:0d:eb:e4:3f:0d
	e4:ee:fc:66:48:aa
	c9:5e:b2:60:37:01

	$ sudo python3 -m app.switchmate status --timeout=2
	Looking for switchmate status...
	ee:0d:eb:e4:3f:0d off
	e4:ee:fc:66:48:aa off
	c9:5e:b2:60:37:01 on

	$ sudo python3 -m app.switchmate ee:0d:eb:e4:3f:0d status
	Looking for switchmate status...
	ee:0d:eb:e4:3f:0d off

	$ sudo python3 -m app.switchmate ee:0d:eb:e4:3f:0d switch on
	Switched!

	$ sudo python3 -m app.switchmate ee:0d:eb:e4:3f:0d toggle
	Switched on!

	$ sudo python3 -m app.switchmate ee:0d:eb:e4:3f:0d battery-level
	Battery level: 45%

## Usage (Flask)

	$ sudo python3 -m app.server
	 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

	GET /iot/switchmate?timeout=1
	Response:
	[["[MAC_ADDRESS_1]", "[off/on]"], ["[MAC_ADDRESS_2]", "[off/on]"], ...]

	POST /iot/switchmate
	Body:
	{"mac_address": "[MAC_ADDRESS]"}
	Response:
	{"status": "done"}