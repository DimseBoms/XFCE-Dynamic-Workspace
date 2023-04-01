# XFCE Dynamic Workspaces

This project aims to provide XFCE with dynamic workspaces similar to those found in the GNOME desktop environment.

## Compatibility

This project has only been tested on XFCE, but it should work on other desktop environments as long as they are compatible with wnck and wmctrl. If there are issues with windows that should not be taken into consideration (panels, docks, etc) when handling workspaces, they can be added to the blacklist inside the script itself (self.window_blacklist).

## Installation:
```bash
# Clone the repository:

git clone https://github.com/DimseBoms/XFCE-Dynamic-Workspace

# Install the required dependencies:

sudo apt install python3-gi wmctrl

# Usage

python3 ./XFCE-Dynamic-Workspace/dynamic_workspaces.py
```

## Add the script to autostart:

Add an autostart entry with
```
exec=/path/to/python3 /path/to/script/dynamic_workspaces.py
```