# HamTec IC-7100 Raspberry Pi panel — v0.1

Local Linux browser panel inspired by the IC-705 screen organization. Designed for a Raspberry Pi 4 with a landscape touch display; 1024×600 or larger is preferred. It adapts to smaller displays. This is an independent project, not Icom software.

## What works

- Demo receive control and an animated simulated RF waterfall.
- USB CI-V frequency and mode control with ACK checking, echo rejection and radio readback.
- Band presets, direct MHz entry, tuning step, wheel/arrow tuning, pause and fullscreen.
- Optional live USB receive-audio FFT waterfall (0–3 kHz).
- Server listens on loopback only. No transmit commands are implemented.

Live CI-V and audio have not been tested with physical hardware. The S-meter graphic is illustrative. There is no live RF-wideband spectrum source, audio playback, VFO A/B switching, filter control, PTT or boot service yet. Scope clicks tune only in simulated RF mode. Live AF is an audio-frequency display, not a calibrated RF bandscope. The 12 kHz IF output requires a separate processing implementation; this version expects the radio output set to AF.

## Quick demo on Raspberry Pi OS

Unzip the project, open a terminal in this folder and run:

```bash
python3 server.py
```

Open `http://127.0.0.1:7100` in Chromium. The demo uses only Python's standard library. You may also open `web/index.html` to inspect the layout, but interactive controls require the server.

## Connect your IC-7100

Use a USB-A to mini-B DATA cable between the Pi and the IC-7100 main unit. Keep the original control head connected. Match the radio CI-V baud rate and address (the application defaults are 19200 and hexadecimal 88). Choose the USB serial interface that carries CI-V, not the second data/GPS interface. Do not run another application on the same serial port.

Install dependencies:

```bash
sudo apt update
sudo apt install python3-venv libportaudio2
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
ls -l /dev/serial/by-id/
```

If serial access is denied, add your user to the dialout group and log out/in:

```bash
sudo usermod -aG dialout "$USER"
```

Start with your actual serial path:

```bash
python3 server.py --port /dev/serial/by-id/YOUR_ICOM_CIV_DEVICE --baud 19200 --address 88
```

The interface shows CI-V connected only after frequency and mode replies arrive. A missing or rejected reply is displayed as an error. Validate frequency and mode changes against the physical radio before regular use. Close the server with Ctrl+C.

## Live receive-audio waterfall

On the radio, select AF for ACC/USB output and adjust the USB AF output level. List capture devices:

```bash
python3 -m sounddevice
```

Choose the numeric input index for the Icom USB audio device. For example, if it is index 3:

```bash
python3 server.py --port /dev/serial/by-id/YOUR_ICOM_CIV_DEVICE --audio-device 3
```

The selected device must support mono input at 48 kHz. The spectrum switches to a clearly labeled 0–3 kHz AF scale. Start without `--audio-device` if audio setup fails. Audio-device selection is supplied at launch rather than in the screen.

## Touchscreen kiosk

With the server running, use your installed Chromium command:

```bash
chromium --kiosk http://127.0.0.1:7100
```

Some Raspberry Pi OS releases use `chromium-browser` instead. Use the Full Screen button for normal desktop testing. Pi startup/autostart configuration depends on your OS version and desktop session and is not changed by this project.

## Wideband waterfall next step

A 705-style wide RF display needs an appropriate separate SDR/IF source and a synchronization layer linking its center frequency to the IC-7100. Do not buy a receiver until the desired HF/VHF/UHF coverage and signal connection are decided. The IC-7100 USB AF or narrow IF output should not be assumed to provide the IC-705's native wideband scope data.

## Verification

```bash
python3 -m unittest -v test_radio.py
```

Tests cover BCD byte order, invalid frequencies, malformed BCD, serial echo/ACK handling and rejection of unsupported/transmit API requests. The browser and real USB hardware still require testing on your Pi.

Official reference: https://www.icomjapan.com/lineup/products/IC-7100EUR/ (Full Manual, CI-V command reference and connector settings).
