import win32serviceutil
import win32service
import win32event
import winreg
import hashlib
import servicemanager
import socket
import os
import sys
import time
import dropbox

BUF_SIZE = 4194304

""" 
    Windows service to sync dropbox folder to local folder for backup
    Requires registry entries at HKEY_LOCAL_MACHINE\SOFTWARE\DropboxSync
        access_key          dropbox access key
        source_folder       folder in dropbox account to sync from
        destination_folder  where to sync to
"""


class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "DropboxSync"
    _svc_display_name_ = "Dropbox Sync"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.service_stop_requested = False
        self.access_key = ""
        self.source_folder = ""
        self.destination_folder = ""
        self.get_settings()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPING,
                              (self._svc_name_, ""))
        self.service_stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                          servicemanager.PYS_SERVICE_STARTED,
                          (self._svc_name_, ""))
        self.main()

    def main(self):
        timer = 0
        while True:
            if self.service_stop_requested:
                break
            time.sleep(5)
            if timer < 120:
                timer += 1
            else:
                servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                      0xF000,
                                      (self._svc_name_, "Entering sync loop")
                                      )
                timer = 0
                self.sync_files()

    def get_settings(self):
        try:
            registry = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\DropboxSync", access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            self.access_key = winreg.QueryValueEx(registry, "access_key")
            self.source_folder = winreg.QueryValueEx(registry, "source_folder")
            self.destination_folder = winreg.QueryValueEx(registry, "destination_folder")
        except:
            print("Unable to access registry!")
            self.SvcStop()
            #exit(1)

    def sync_files(self):
        if not os.path.exists(self.destination_folder):
            sys.exit(1)
        elif not os.path.isdir(self.destination_folder):
            sys.exit(1)

        dbx = dropbox.Dropbox(self.access_key)
        files = dbx.files_list_folder(self.source_folder)
        results = files.entries
        while files.has_more:
            files = dbx.files_list_folder_continue(files.cursor)
            results += files.entries

        for entry in results:
            target = self.destination_folder + entry.name
            if not os.path.isfile(target) or entry.content_hash != self.get_hash(target):
                dbx.files_download_to_file(target, entry.path_display)

    @staticmethod
    def get_hash(file):
        try:
            with open(file, "rb", buffering=0) as f:
                hash_value = hashlib.sha256()
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    else:
                        hash_value.update(hashlib.sha256(data).digest())
            return hash_value.hexdigest()
        except:
            return 0


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(AppServerSvc)