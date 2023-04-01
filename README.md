# XFCE Dynamic Workspaces

## This project aims to provide XFCE with dynamic workspaces similar to those found in the GNOME desktop environment.
Compatibility

This project has only been tested on XFCE, but it should work on other desktop environments as long as they are compatible with wnck and wmctrl. If there are issues with windows that should not be taken into consideration when handling workspaces, they can be added to the blacklist.
Installation

    Clone the repository:

    bash

git clone https://github.com/your_username/xfce-dynamic-workspaces.git

Install the required dependencies:

sudo apt install python3-gi python3-gi-cairo gir1.2-wnck-3.0 gir1.2-notify-0.7

Make the script executable:

bash

    chmod +x xfce-dynamic-workspaces.py

    Add the script to autostart:
        Navigate to "Session and Startup" from the XFCE settings menu.
        Click on the "Application Autostart" tab.
        Click on the "Add" button.
        In the "Name" field, enter "XFCE Dynamic Workspaces".
        In the "Command" field, enter the path to the script, e.g., "/path/to/xfce-dynamic-workspaces.py".
        Click on the "OK" button.

Usage

To use the dynamic workspaces, simply run the script. Whenever a workspace is added or removed, a notification will be displayed.
License

This project is licensed under the MIT License - see the LICENSE file for details.
