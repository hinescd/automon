# Automon

Automon is a tool that uses xrandr to automatically configure monitors as they are connected and disconnected.

## Dependencies

Automon uses PyYAML to read configuration files.

## Configuration

Automon uses the file ```~/.automon.yaml``` to decide how to configure monitors. The file declares which screen (if any) is the laptop screen, which file to read for lid status, and a collection of profiles for monitors. A profile is a list of configurations for monitors. Multiple profiless can be defined for a given set of monitors, and writing ```next``` or ```prev``` to the named pipe ```/tmp/automon_pipe``` will cause automon to change to the next or previous profile for the connected monitors. See the following for a sample configuration file:

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
      output: HDMI-1
      mode: auto
    - 
      output: eDP-1
      'off': ~ # off is in quotes because it's a reserved word in YAML. ~ shows that this xrandr flag does not have a value
  - -
      output: eDP-1
      mode: 1280x800
```

This configuration has three defined profiles: two for when HDMI-1 and eDP-1 are connected, and one for when only eDP-1 is connected. If only HDMI-1 is connected, it will default to ```mode: auto```.

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
