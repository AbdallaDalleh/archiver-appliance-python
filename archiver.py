""" EPICS archiver appliance HTTP interface """
#!/usr/bin/python3

import json
import requests

class Archiver():
    """ Class definition """
    def __init__(self, **args):
        self.mgmt_port = 17665
        self.retrieval_port = 17668
        self.server_ip = ""
        self.mgmt_url = ""
        self.retrieval_url = ""

        for key, value in args.items():
            if key == "server_ip":
                self.server_ip = value
            elif key == "mgmt_port":
                self.mgmt_port = int(value)
            elif key == "retrieval_port":
                self.retrieval_port = int(value)

        self.mgmt_url = f"http://{self.server_ip}:{self.mgmt_port}/mgmt/bpl/"

    def get_pv_list(self):
        """ Retrive list of currently archived PVs. """
        request = requests.get(url=self.retrieval_url + "", params={"limits": -1}, timeout=-1)
        if request.status_code != 200:
            return None

        return json.loads(request.text)
    
    def consolidate_data(self, **args):
        """ Consolidate the PV to the target storage. """
        pv_name = ""
        target_storage = ""
        for key, value in args.items():
            if key == "pv":
                pv_name = value
            elif key == "target":
                target_storage = value
            else:
                raise KeyError("consolidate_data: Invalid key passed")
        
        if pv_name == "" or target_storage == "":
            raise ValueError("consolidate_data: PV name or target location is empty.")

