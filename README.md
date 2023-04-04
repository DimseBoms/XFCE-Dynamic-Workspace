# XFCE Dynamic Workspaces
This project aims to provide XFCE with dynamic workspaces similar to those found in the GNOME desktop environment. Use in conjunction with Xfdashboard and you got yourself a Gnome lite.

## Compatibility
This project has only been tested on XFCE, but it should work on other desktop environments as long as they are compatible with wnck and wmctrl. If there are issues with windows that should not be taken into consideration (panels, docks, etc) when handling workspaces, they can be added to the blacklist inside the script itself (see `Adding windows to the blacklist`). It will only work on X11 though as libwnck and wmctrl do not support wayland.

## Installation:
```bash
# Install the required dependencies:
# Ubuntu/Debian
sudo apt install python3-gi libwnck-3.0 wmctrl
# Fedora
sudo dnf install python3-gobject libwnck3 wmctrl

# Clone the repository:
git clone https://github.com/DimseBoms/XFCE-Dynamic-Workspace

# Usage
python3 ./XFCE-Dynamic-Workspace/dynamic_workspaces.py
```

## Adding windows to the blacklist
If you are having issues and workspaces seem to pile up getting added one after another in a continous loop, you most likely have a special window that needs to be blacklisted. To add the window to the blacklist you can add a new entry to the list inside the code (self.window_blacklist on line 18). To find out which window is giving you trouble you can start the script manually with the `--debug` flag to make it print all window names. It is usually a dock, panel or some other type of "static", special window that is the culprit.

## Add the script to autostart:
Add an autostart entry with the exec=
```
/path/to/python3 /path/to/script/dynamic_workspaces.py
```
