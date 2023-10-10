""" EPICS archiver appliance HTTP interface """
#!/usr/bin/python3

import json
import requests

REQUEST_PV_LIST = "getAllPVs"
REQUEST_CONSOLIDATE = "consolidateDataForPV"
REQUEST_PAUSE = "pauseArchivingPV"
REQUEST_RESUME = "resumeArchivingPV"
REQUEST_DETAILS = "getPVDetails"
REQUEST_ADD_PV = "archivePV"

class Archiver():
    """ Class definition """
    def __init__(self, server_ip, **args):
        self.mgmt_port = 17665
        self.retrieval_port = 17668
        self.server_ip = ""
        self.mgmt_url = ""
        self.retrieval_url = ""
        self.server_ip = server_ip

        for key, value in args.items():
            if key == "mgmt_port":
                self.mgmt_port = int(value)
            elif key == "retrieval_port":
                self.retrieval_port = int(value)

        self.mgmt_url = f"http://{self.server_ip}:{self.mgmt_port}/mgmt/bpl/"

    def get_pv_list(self):
        """ Retrive list of currently archived PVs. """
        request = requests.get(url=self.mgmt_url + REQUEST_PV_LIST, params={"limit": -1})
        if request.status_code != 200:
            return None

        return json.loads(request.text)

    def pause_pv(self, pv_name):
        """ Pause archiving for a single PV. """
        request = requests.get(url=self.mgmt_url + REQUEST_PAUSE, params={"pv": pv_name})
        if request.status_code != 200:
            return False
        return True

    def resume_pv(self, pv_name):
        """ Pause archiving for a single PV. """
        request = requests.get(url=self.mgmt_url + REQUEST_RESUME, params={"pv": pv_name})
        if request.status_code != 200:
            return False
        return True

    def consolidate_data(self, pv_name, target_storage):
        """ Consolidate the PV to the target storage. """
        if pv_name == "" or target_storage == "":
            raise ValueError("consolidate_data: PV name or target location is empty.")

        if self.pause_pv(pv_name) is False:
            print(f"PV {pv_name} was not paused successfully.")
            return

        request = requests.get(url=self.mgmt_url + REQUEST_CONSOLIDATE, params={"pv": pv_name, "storage": target_storage})
        if request.status_code != 200:
            print(f"Consolidation for PV {pv_name} failed.")

        if self.resume_pv(pv_name) is False:
            print(f"PV {pv_name} was not resumed successfully.")
            return

    def consolidate_all(self, target="LTS"):
        """ Consolidate all PVs in the server to the target storage (LTS by default) """
        pv_names = self.get_pv_list()
        for pv_name in pv_names:
            print("Consolidating data for PV %s" % pv_name)
            self.consolidate_data(pv_name=pv_name, target_storage=target)

    def get_pv_details(self, pv_name):
        """ Get PV Details. """
        request = requests.get(url=self.mgmt_url + REQUEST_DETAILS, params={"pv": pv_name})
        if request.status_code != 200:
            return None

        return json.loads(request.text)

    def archive_pv(self, pv_name, period, method="MONITOR"):
        """ Archive new PV. """
        request = requests.get(url=self.mgmt_url + REQUEST_ADD_PV, params={"pv": pv_name, "samplingperiod": period, "samplingmethod": method})
        if request.status_code != 200:
            print(f"PV {pv_name} was not added successfully.")
            return False

        print(f"PV {pv_name} added successfully.")
        return True

