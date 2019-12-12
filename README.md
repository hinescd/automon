# Automon

Automon is a tool that uses xrandr to automatically configure monitors as they are connected and disconnected.

## Dependencies

Automon uses PyYAML to read configuration files.

## Configuration

Automon uses the file ```~/.automon.yaml``` to decide how to configure monitors. The file declares which screen (if any) is the laptop screen, which file to read for lid status, and a collection of profiles for monitors. A profile is a list of configurations for monitors. See the following for a sample configuration file:

```yaml
--- 
laptop-screen: eDP-1
lid: /proc/acpi/button/lid/LID/state
profiles: 
  - - 
      output: HDMI-1
      mode: auto
    - 
      output: eDP-1
      left-of: HDMI-1
      mode: auto
  - -
      output: eDP-1
      mode: 1280x800
```

This configuration has eDP-1 placed to the left of HDMI-1 when both monitors are connected, and sets the resolution of eDP-1 to 1280x800 when it is on its own. Since there is no configuration specified for when HDMI-1 is connected but the laptop lid is closed, it will default to ```mode: auto```.

In order for config changes to be reloaded, automon must be restarted.

## Running

Run automon with Python 3.

```
python3 automon.py
```

It is recommended to configure your window manager to run automon as a background process on startup. Instructions for doing so vary by window manager.

```
python3 automon.py &
```
