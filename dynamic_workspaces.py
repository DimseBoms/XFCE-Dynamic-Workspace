#!/usr/bin/env python3

from gi.repository import Wnck, Gtk, Notify
import signal
import os


class workspaceIndicator:

    # Self initialization
    def __init__(self):
        self.window_blacklist = [
            "Skrivebord",
            "Desktop",
            "xfdashboard",
            "xfce4-panel",
            "plank"]
        self.first = True
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.screen = Wnck.Screen.get_default()
        self.popup = Notify.Notification.new("")
        self.popup.set_timeout(1)
        Notify.init("Workspace Switch Notifier")

    # Notification handling
    def fire_switch(self, in_screen, in_previously_active_workspace):
        # Gets the current amount of workspaces
        try:
            workspace_num = str(
                self.screen.get_active_workspace().get_number() + 1)
        except:
            workspace_num = None
        if workspace_num:
            self.popup.update(f"Arbeidsområde {workspace_num}")
            self.popup.show()

    # Main logic for handling of dynamic workspaces
    def dynamic_workspace(self, in_screen, in_window):
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
            # Calls the function to remove blacklisted windows
            windows = self.remove_blacklist(self.screen.get_windows())
            # Counts windows
            #print('\n[List of windows currently not blacklisted]:\n')
            for window in windows:
                # print(window.get_name())
                if window.is_on_workspace(workspaces[-1]):
                    last += 1
                if workspaces_len > 1:
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
        # Initiate logic to remove windowless workspaces at the start/in the middle
        #if workspaces_len > 1:
        #    windows = self.remove_blacklist(self.screen.get_windows())
        #    if workspaces:
        #        crunch = {}
        #        i = 0
        #    for window in windows:
        #        if window.get_workspace() not in crunch:
        #            crunch[window.get_workspace()] = [
        #                window]
        #        else:
        #            crunch[window.get_workspace()].append(
        #                window)
        #    # Passing list of windows and their respective workspaces to the crunch function
        #    self.crunch_workspace(crunch, workspaces)

    # Removes blacklisted windows from the list of visible windows
    def remove_blacklist(self, windows):
        i = 0
        while len(windows) > i:
            if windows[i].get_name() in self.window_blacklist:
                windows.pop(i)
                i -= 1
            i += 1
        return windows

    # Moves all windows from the workspace next to the selected workspace to
    # the last workpsace one workspace to the left.
    #def move_windows(self, workspace, windows):
    #    pass

    # Functions for handling adding/removal of workspaces. These functions just work as
    # an interface to send shell commands with wmctrl.
    def add_workspace(self, workspaces_len):
        os.system(f"wmctrl -n {workspaces_len + 1}")

    def pop_workspace(self, workspaces_len):
        os.system(f"wmctrl -n {workspaces_len - 1}")

    # Logic for checking workspaces at the start/in the middle
    #def crunch_workspace(self, crunch, workspaces):
    #    ws_len = len(workspaces)
    #    i = 0
    #    while ws_len >= 2 and i <= ws_len:
    #        print(f'ws_len: {ws_len}\ni: {i}')
    #        workspace = workspaces[i]
    #        if workspace not in crunch and self.screen.get_active_workspace() is not workspace:
    #            self.move_windows(workspace, self.remove_blacklist(self.screen.get_windows()))
    #            self.pop_workspace(ws_len)
    #            i-=1
    #            ws_len-=1
    #        i+=1
    #        if ws_len == 2:
    #            break

    # Assigns functions to Wnck.Screen signals. Check out the API docs at
    # "http://lazka.github.io/pgi-docs/index.html#Wnck-3.0/classes/Screen.html"
    def main(self):
        os.system("wmctrl -n 1")
        self.screen.connect("active-workspace-changed", self.fire_switch)
        self.screen.connect("active-workspace-changed", self.dynamic_workspace)
        self.screen.connect("window-opened", self.dynamic_workspace)
        self.screen.connect("window-closed", self.dynamic_workspace)
        Gtk.main()


# Starts the program
if __name__ == '__main__':
    print("Started workspace indicator")
    indicator = workspaceIndicator()
    indicator.main()
