# This is the Stager API wrapper module for the Lofar LTA staging service.
#
# It uses an xmlrpc proxy to talk and authenticate to the remote service. Your account credentials will be read from
# the awlofar catalog Environment.cfg, if present or can be provided in a .stagingrc file in your home directory.
#
# !! Please do not talk directly to the xmlrpc interface, but use this module to access the provided functionality.
# !! This is to ensure that when we change the remote interface, your scripts don't break and you will only have to
# !! upgrade this module.

__version__ = "1.3"

import datetime
from os.path import expanduser
import os
import glob

# Python2/3 dependent stuff
from sys import version_info

python_version = version_info.major
if python_version == 3:
    import xmlrpc.client as xmlrpclib

    string_types = str
else:
    import xmlrpclib

    string_types = basestring

user = None
passw = None
try:
    f = expanduser("~/.awe/Environment.cfg")
    with open(f, 'r') as file:
        print("%s - stager_access: Parsing user credentials from \"%s\"" % (datetime.datetime.now(), f))
        for line in file:
            if line.startswith("database_user"):
                user = line.split(':')[1].strip()
            if line.startswith("database_password"):
                passw = line.split(':')[1].strip()
except IOError:
    f = expanduser("~/.stagingrc")
    with open(f, 'r') as file:
        print("%s - stager_access: Parsing user credentials from \"%s\"" % (datetime.datetime.now(), f))
        for line in file:
            if line.startswith("user"):
                user = line.split('=')[1].strip()
            if line.startswith("password"):
                passw = line.split('=', 1)[1].strip()

print("%s - stager_access: Creating proxy" % (datetime.datetime.now()))
proxy = xmlrpclib.ServerProxy("https://" + user + ':' + passw + "@webportal.astron.nl/service-public/xmlrpc")
LtaStager = proxy.LtaStager

def stage(surls):
    if isinstance(surls, str):
        surls = [surls]
    stageid = proxy.LtaStager.add_getid(surls)
    return stageid

def get_status(stageid):
    return proxy.LtaStager.getstatus(stageid)

def abort(stageid):
    return proxy.LtaStager.abort(stageid)

def get_surls_online(stageid):
    return proxy.LtaStager.getstagedurls(stageid)

def get_srm_token(stageid):
    return proxy.LtaStager.gettoken(stageid)

def reschedule(stageid):
    return proxy.LtaStager.reschedule(stageid)

def get_progress(status=None, exclude=False):
    all_requests = proxy.LtaStager.getprogress()
    if status is not None and isinstance(status, string_types):
        if python_version == 3:
            all_items = all_requests.items()
        else:
            all_items = all_requests.iteritems()
        if exclude is False:
            requests = {key: value for key, value in all_items if value["Status"] == status}
        else:
            requests = {key: value for key, value in all_items if value["Status"] != status}
    else:
        requests = all_requests
    return requests

def reschedule_on_status(status=None):
    if status is not None and isinstance(status, string_types) and (status == "on hold" or status == "aborted"):
        requests = get_progress(status)
        for key in requests.keys():
            reschedule(int(key))
    else:
        print("The parameter status is either None, not a string neither of \"on hold\" nor \"aborted\".")

def get_storage_info():
    return proxy.LtaStager.getsrmstorageinfo()

def prettyprint(dictionary, indent=""):
    if type(dictionary) is dict:
        for key in sorted(dictionary.keys()):
            item = dictionary.get(key)
            if type(item) is dict:
                print("%s+ %s" % (indent, str(key)))
                prettyprint(item, indent=indent + '  ')
            else:
                print("%s- %s\t->\t%s" % (indent, str(key), str(item)))
    else:
        print("stager_access: This prettyprint takes a dict only!")


def reschedule_on_hold():
    reschedule_on_status("on hold")

def print_on_hold():
    requests = get_progress("on hold")
    prettyprint(requests)

def reschedule_aborted():
    reschedule_on_status("aborted")

def print_aborted():
    requests = get_progress("aborted")
    prettyprint(requests)

def print_running():
    requests = get_progress("success", True)
    prettyprint(requests)

def download(surls, dirTO):
    prefix = "https://lofar-download.grid.surfsara.nl/lofigrid/SRMFifoGet.py?surl="

    downloadFiles = [prefix + surl for surl in surls]

    for file in downloadFiles:
        os.system("wget " + file + " -P " + dirTO)

    for filename in glob.glob(dirTO + "*SB*.tar*"):
        outname = filename.split("%")[-1]
        os.rename(filename, outname)
        os.system('tar -xvf ' + outname)
        os.system('rm -r ' + outname)
        print(outname + ' untarred.')

'''
stageID = 37384

surls = get_surls_online(stageID)
print("status", get_status(stageID))
print("srm url", surls)
print("srm token", get_srm_token(stageID))
stageID = str(stage(surls))  # create new stage
print("stageID", stageID)
'''


