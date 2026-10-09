[HamTec-IC7100-705-Style (1).zip](https://github.com/user-attachments/files/33263912/HamTec-IC7100-705-Style.1.zip)


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
# HamTec IC-7100 Linux Control Panel

A Raspberry Pi 4 touchscreen control panel for the Icom IC-7100, with an IC-705-inspired frequency display, spectrum and waterfall layout.

**Version:** 0.1 prototype  
**Platform:** Linux / Raspberry Pi OS  
**Radio controls:** Receive frequency and operating mode

This is an independent HamTec project, not official Icom software. Physical CI-V and USB audio operation still need testing with an IC-7100.

## Features

- Large frequency display and touch-friendly controls.
- Band presets for 80m, 40m, 20m, 15m, 10m, 6m, 2m and 70cm.
- USB, LSB, CW, CW-R, AM, FM, RTTY, RTTY-R and DV modes.
- Direct frequency entry in MHz.
- Tuning buttons, arrow keys and mouse-wheel tuning.
- Selectable tuning steps.
- Animated demo spectrum and waterfall.
- Optional live USB receive-audio waterfall.
- CI-V acknowledgement checking and radio readback.
- Full-screen display.
- Local operation without a cloud service.
- No transmit/PTT commands are implemented.

## Screenshots

The image links below will display once you capture the screenshots on your Pi and save them at the specified paths. Screenshots have not yet been captured.

### Main panel

![HamTec IC-7100 demo panel](docs/screenshots/panel-demo.png)

The demo waterfall is simulated. The S-meter graphic is illustrative.

### Frequency entry

![Direct frequency entry](docs/screenshots/frequency-entry.png)

Keep the `docs/screenshots` folder alongside this README when copying the project into a repository.

## Waterfall capabilities

| Source | Display | Status |
| --- | --- | --- |
| Demo | Simulated RF spectrum and waterfall | Included |
| IC-7100 USB audio | Live received-audio spectrum, 0–3 kHz | Implemented; hardware testing required |
| Wideband RF | IC-705-style wide RF bandscope | Not implemented |

The IC-7100 USB audio and narrow IF output should not be assumed to supply the IC-705’s native wideband spectrum data.

This version processes received **AF audio**, not the radio’s 12 kHz IF output. A wideband RF waterfall needs a suitable separate SDR/IF source and further integration.

## Requirements

- Raspberry Pi 4 and a suitable Pi power supply.
- Raspberry Pi OS with a desktop environment.
- Chromium browser.
- Landscape touchscreen or a monitor, keyboard and mouse.
- A 1024×600 or larger display is the design target.
- Icom IC-7100 with its original control head connected.
- USB-A to mini-B data cable.
- Internet connection for dependency installation.

The radio requires its normal power supply.

## 1. Download and extract

Download `HamTec-IC7100-Pi-Panel.zip` onto your Pi.

These commands assume the ZIP is in your Downloads folder:

```bash
sudo apt update
sudo apt install -y unzip python3 python3-venv libportaudio2

mkdir -p "$HOME/hamtec"

unzip "$HOME/Downloads/HamTec-IC7100-Pi-Panel.zip" \
  -d "$HOME/hamtec"

cd "$HOME/hamtec/ic7100-panel"
```

If the ZIP is saved elsewhere, change the path in the `unzip` command.

Back up an existing installation before extracting over it.

## 2. Run the demo

No radio connection or Python dependencies are needed for demo mode.

```bash
cd "$HOME/hamtec/ic7100-panel"
python3 server.py
```

Leave the terminal running.

Open Chromium on the Pi and visit:

**http://127.0.0.1:7100**

You should see:

- DEMO MODE.
- A frequency display starting at 14.200.000 MHz.
- An animated simulated waterfall.
- Band presets and tuning controls.

Try entering a frequency, selecting a band and changing mode.

Press **Ctrl+C** in the terminal to stop the server.

## 3. Install radio and audio dependencies

Stop the demo server, then run:

```bash
cd "$HOME/hamtec/ic7100-panel"

python3 -m venv .venv
. .venv/bin/activate

python -m pip install -r requirements.txt
```

Activate the virtual environment whenever you open a new terminal:

```bash
cd "$HOME/hamtec/ic7100-panel"
. .venv/bin/activate
```

## 4. Connect the IC-7100

1. Power the radio normally.
2. Leave the original control head connected.
3. Connect the Pi to the radio’s main-unit USB socket using a USB-A to mini-B data cable.
4. Close other applications using the radio’s serial port.

Find the USB serial devices:

```bash
ls -l /dev/serial/by-id/
```

If that directory is unavailable, try:

```bash
ls -l /dev/ttyUSB*
```

Choose the interface used for **CI-V control**, rather than the second data/GPS interface.

Use the persistent `/dev/serial/by-id/...` path where possible.

### Serial permission errors

If access is denied:

```bash
sudo usermod -aG dialout "$USER"
```

Log out and back in, or reboot, before retrying.

Do not run the application as root.

## 5. Match CI-V settings

Check the radio’s CI-V settings in its Set menu.

The application defaults are:

| Setting | Value |
| --- | --- |
| CI-V baud rate | 19200 |
| CI-V address | 88 hexadecimal |

If your radio uses different settings, supply matching values when starting the server.

The `--address` argument is hexadecimal: `88` means `0x88`.

## 6. Start live radio control

Activate the virtual environment:

```bash
cd "$HOME/hamtec/ic7100-panel"
. .venv/bin/activate
```

Replace `YOUR_ICOM_CIV_DEVICE` with the exact device name found earlier:

```bash
python server.py \
  --port /dev/serial/by-id/YOUR_ICOM_CIV_DEVICE \
  --baud 19200 \
  --address 88
```

Open:

**http://127.0.0.1:7100**

The panel shows **CI-V CONNECTED** after valid frequency and mode replies arrive.

Check that the displayed frequency matches the physical radio. Make a small tuning change and confirm it on the radio, then check mode selection.

Without an audio device selected, live CI-V mode has no spectrum source.

## 7. Enable the live audio waterfall

On the IC-7100:

- Set **ACC/USB Output Select** to **AF**.
- Adjust **ACC/USB AF Level** for a usable signal without clipping.

List audio devices:

```bash
python -m sounddevice
```

Find the numeric input-device index for the Icom USB audio device.

Stop the existing server with **Ctrl+C**.

The following example assumes the audio input index is `3`. Replace it with your actual index:

```bash
python server.py \
  --port /dev/serial/by-id/YOUR_ICOM_CIV_DEVICE \
  --baud 19200 \
  --address 88 \
  --audio-device 3
```

The panel should show:

**LIVE AF · 0–3 kHz**

The selected device must support mono input at 48 kHz.

Audio-device indices may change after reconnecting USB or rebooting. List the devices again if necessary.

This feature displays received audio frequencies. Audio playback and remote audio streaming are not implemented.

## 8. Full-screen and kiosk mode

Use the panel’s **FULL SCREEN** button.

Alternatively, leave the server running and open another terminal on the Pi desktop:

```bash
chromium --kiosk http://127.0.0.1:7100
```

If your browser command is `chromium-browser`, use:

```bash
chromium-browser --kiosk http://127.0.0.1:7100
```

Press **Alt+F4** to close the kiosk window.

Automatic startup is not configured by this project.

The server listens on the Pi’s loopback address. Open the URL on the Pi itself.

## 9. Capture screenshots

### Main panel screenshot

Start the demo server:

```bash
cd "$HOME/hamtec/ic7100-panel"
python3 server.py
```

In a second terminal:

```bash
cd "$HOME/hamtec/ic7100-panel"
bash docs/capture-screenshot.sh
```

The script uses your installed Chromium browser and saves:

`docs/screenshots/panel-demo.png`

### Frequency-entry screenshot

1. Open the panel in Chromium.
2. Tap the large frequency display.
3. Use your desktop screenshot application to capture the window.
4. Save the image as:

`docs/screenshots/frequency-entry.png`

The screenshots will then appear in this README on Markdown viewers that support relative image paths.

## Controls

| Control | Action |
| --- | --- |
| Frequency display | Enter a frequency in MHz |
| Band preset | Set preset frequency and mode |
| Mode selector | Change operating mode |
| + / − | Tune by the selected step |
| Up / down arrows | Tune when a dialog or form control does not have focus |
| Mouse wheel over frequency | Tune up or down |
| Waterfall click | Tune in simulated RF demo mode only |
| Span | Change simulated RF span |
| Running / Paused | Pause or resume scope animation |
| Center | Clear waterfall history and redraw labels |
| Full Screen | Toggle browser fullscreen |
| Setup | Display connection guidance |

Radio polling continues while the scope animation is paused.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Browser cannot connect | Keep the server running and open the URL on the Pi |
| Address already in use | Stop the previous server or select another HTTP port |
| No serial device | Check radio power and the USB data cable |
| Permission denied | Add your user to `dialout`, then log out and back in |
| No CI-V reply | Check the selected port, baud rate, address and radio power |
| Radio rejected command | Check whether the selected mode or frequency is supported |
| No waterfall in CI-V mode | Start with `--audio-device`; serial control alone supplies no spectrum |
| Audio device fails | Select an input supporting mono 48 kHz |
| Flat audio waterfall | Check AF output selection, AF level and received signal |
| Frequency labels show 0–3 kHz | Expected for the live audio waterfall |
| Missing Python module | Activate `.venv` and install `requirements.txt` |
| S-meter does not move | The meter is currently illustrative |

To use another HTTP port:

```bash
python server.py --http-port 7101
```

Then open:

**http://127.0.0.1:7101**

## Software tests

Run:

```bash
cd "$HOME/hamtec/ic7100-panel"
. .venv/bin/activate
python -m unittest -v test_radio.py
```

The five tests cover:

- Frequency byte encoding.
- Receive-frequency ranges.
- Invalid BCD data.
- Serial echo and acknowledgement handling.
- Rejection of unsupported control requests.

Software tests and JavaScript syntax checks passed during development. Physical radio, USB audio and browser operation still require testing on the Pi.

## Current limitations

The following are not implemented:

- Live S-meter.
- Wideband RF spectrum input.
- VFO A/B switching.
- Filter controls.
- Audio playback.
- Transmit/PTT controls.
- Automatic startup.

Band presets are starting points for receive tuning, not a transmit band-plan guide.

## Project files

| File | Purpose |
| --- | --- |
| `server.py` | Local server, CI-V controls and optional audio FFT |
| `web/index.html` | Touchscreen interface |
| `requirements.txt` | Hardware/audio dependencies |
| `test_radio.py` | Software tests |
| `docs/capture-screenshot.sh` | Main-panel screenshot capture |
| `docs/screenshots/` | README screenshot images |

## Official references

- [Icom IC-7100 product page and manuals](https://www.icomjapan.com/lineup/products/IC-7100EUR/)
- [Raspberry Pi OS documentation](https://www.raspberrypi.com/documentation/computers/os.html)


Tests cover BCD byte order, invalid frequencies, malformed BCD, serial echo/ACK handling and rejection of unsupported/transmit API requests. The browser and real USB hardware still require testing on your Pi.

Official reference: https://www.icomjapan.com/lineup/products/IC-7100EUR/ (Full Manual, CI-V command reference and connector settings).
