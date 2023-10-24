#!/usr/bin/env python3

import gi
gi.require_version('Wnck', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Wnck, Gtk, Notify
import signal
import os
import subprocess
import sys


class DynamicWorkspaces:
    # Self initialization
    def __init__(self, DEBUG=False):
        self.DEBUG = DEBUG
        self.window_blacklist = [
            "Skrivebord",
            "Desktop",
            "xfdashboard",
            "xfce4-panel",
            "plank",
            "xfce4-notifyd",
            "Whisker Menu"
        ]
        self.window_classrole_blacklist = [
            "tilix.quake"
        ]
        self.last = 0
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.screen = Wnck.Screen.get_default()
        self.popup = Notify.Notification.new("")
        self.popup.set_timeout(1)
        Notify.init("Workspace Switch Notifier")

    # Notification handling
    def update_notification(self, in_screen, in_previously_active_workspace):
        # Gets the current amount of workspaces
        try:
            workspace_num = str(
                self.screen.get_active_workspace().get_number() + 1)
        except:
            workspace_num = None
        if workspace_num:
            self.popup.update(f"Workspace {workspace_num}")
            try:
                # Try to activate, but in some cases (like screensaver), this can't be done.
                self.popup.show()
            except:
                pass

    # Main logic for handling of dynamic workspaces
    def handle_dynamic_workspace(self, in_screen, in_window):
        # Gets the current workspaces
        try:
            workspaces = self.screen.get_workspaces()
            workspaces_len = len(workspaces)
        except:
            workspaces = None
        # Initiates necessary scope variables and counts the windows on the relevant workspaces
        if workspaces:
            last = 0
            next_last = 0
            # Removes blacklisted windows from the list of visible windows
            windows = self.remove_blacklist(self.screen.get_windows())
            # Counts windows
            for window in windows:
                # Checks if the window is on the last workspace
                if window.is_on_workspace(workspaces[-1]):
                    last += 1
                if workspaces_len > 1:
                    # Checks if the window is on the workspace before the last
                    if window.is_on_workspace(workspaces[-2]):
                        next_last += 1
            # Main logical operations for removing last/last two workspaces
            if last > 0:
                self.add_workspace(workspaces_len)
            if workspaces_len > 1:
                if last == 0 and next_last == 0:
                    self.pop_workspace(workspaces_len)
        # Refresh the current workspaces and windows
        try:
            workspaces = self.screen.get_workspaces()
            workspaces_len = len(workspaces)
        except:
            workspaces = None
        # If there are more than 2 workspaces, iterate through all the workspaces
        # except the last one and check if they are empty. If they are, remove them.
        if workspaces_len > 2:
            windows = self.remove_blacklist(self.screen.get_windows())
            for i, workspace in enumerate(workspaces[:-1]):
                if self.screen.get_active_workspace() is not workspace and self.screen.get_workspaces()[-1] is not workspace:
                    workspace_empty = True
                    for window in windows:
                        if window.is_on_workspace(workspace):
                            workspace_empty = False
                            break
                    if workspace_empty:
                        if not (workspace == self.screen.get_workspaces()[-1]):
                            self.remove_workspace_by_index(i)
        # Update last workspace
        try:
            self.last = self.screen.get_active_workspace().get_number()
        except AttributeError:
            pass

    # Removes blacklisted windows from the list of visible windows
    def remove_blacklist(self, windows):
        i = 0
        while len(windows) > i:
            # print(windows[i].get_name())
            if windows[i].is_sticky():
                windows.pop(i)
                i -= 1
            elif windows[i].get_name() in self.window_blacklist:
                windows.pop(i)
                i -= 1
            elif windows[i].get_role() is not None:
                if '.'.join((windows[i].get_class_instance_name(), windows[i].get_role())) in self.window_classrole_blacklist:
                    windows.pop(i)
                    i -= 1
            i += 1
        if self.DEBUG:
            for window in windows:
                print(window.get_name())
        return windows

    # Functions for handling adding/removal of workspaces. These functions just work as
    # an interface to send shell commands with wmctrl.
    def add_workspace(self, workspaces_len):
        os.system(f"wmctrl -n {workspaces_len + 1}")

    def pop_workspace(self, workspaces_len):
        if len(self.screen.get_workspaces()) > 2:
            os.system(f"wmctrl -n {workspaces_len - 1}")

    # Removes a workspace by index using wmctrl
    def remove_workspace_by_index(self, index):
        # Get curent workspace number
        workspace_num = None
        try:
            workspace_num = self.screen.get_active_workspace().get_number()
        except AttributeError:
            pass
        # Get current workspaces using wmctrl
        workspaces = subprocess.check_output("wmctrl -d", shell=True).decode("utf-8").splitlines()
        # Get current windows and their workspaces
        windows = self.screen.get_windows()
        # Filter out the windows that don't have workspaces or are on any workspace
        # on a lower index than the workspace to be removed
        windows = [window for window in windows if window.get_workspace() is not None and window.get_workspace().get_number() > index]
        for window in windows:
            # Move the windows that are left one workspace to the left
            window.move_to_workspace(self.screen.get_workspaces()[window.get_workspace().get_number() - 1])
        self.pop_workspace(len(workspaces))
        # Make sure you stay on the workspace
        if workspace_num and self.last < workspace_num:
            os.popen(f"wmctrl -s {index}")

    # Assigns functions to Wnck.Screen signals. Check out the API docs at
    # "http://lazka.github.io/pgi-docs/index.html#Wnck-3.0/classes/Screen.html"
    def connect_signals(self):
        os.system("wmctrl -n 1")  # Resets the amount of workspaces to 1
        self.screen.connect("active-workspace-changed", self.update_notification)
        self.screen.connect("active-workspace-changed", self.handle_dynamic_workspace)
        self.screen.connect("workspace-created", self.handle_dynamic_workspace)
        self.screen.connect("workspace-destroyed", self.handle_dynamic_workspace)
        self.screen.connect("window-opened", self.handle_dynamic_workspace)
        self.screen.connect("window-closed", self.handle_dynamic_workspace)
        Gtk.main()


# Starts the program
if __name__ == '__main__':
    DEBUG = False
    for arg in sys.argv:
        if arg == "--debug":
            print("Debug mode enabled")
            DEBUG = True
    print("Started workspace indicator")
    workspace_handler = DynamicWorkspaces(DEBUG)
    workspace_handler.connect_signals()
