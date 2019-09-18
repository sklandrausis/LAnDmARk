''' This is the Stager API wrapper module for the Lofar LTA staging service.
It uses an xmlrpc proxy to talk and authenticate to the remote service. Your account credentials will be read from
the awlofar catalog Environment.cfg, if present or can be provided in a .stagingrc file in your home directory.
!! Please do not talk directly to the xmlrpc interface, but use this module to access the provided functionality.
!! This is to ensure that when we change the remote interface, your scripts don't break and you will only have to
!! upgrade this module.'''

__version__ = "1.3"

import datetime
import glob
import os
from os.path import expanduser
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
    ''' Stage urls'''

    if isinstance(surls, str):
        surls = [surls]
    stageid = proxy.LtaStager.add_getid(surls)
    return stageid

def get_surls_online(stageid):
    ''' Get staget urls '''
    return proxy.LtaStager.getstagedurls(stageid)

def get_progress(status=None, exclude=False):
    ''' Get progress of staging '''
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


def download(surls, dir_to, SASidsCalibrator, SASidsTarget):
    ''' Download file '''
    download_files = []

    for surl in surls:

        if "sara" in surl:
            prefix = "https://lofar-download.grid.surfsara.nl/lofigrid/SRMFifoGet.py?surl="

        elif "juelich" in surl:
            prefix = "https://lofar-download.fz-juelich.de/webserver-lofar/SRMFifoGet.py?surl="

        else:
            prefix = "https://lta-download.lofar.psnc.pl/lofigrid/SRMFifoGet.py?surl="

        download_files.append(prefix + surl)

    for file in download_files:
        os.system("wget " + file + " -P " + dir_to)

    for filename in os.listdir(dir_to):
        if ".tar" in filename:
            outname = dir_to + "/" + filename.split("%")[-1]
            os.rename(dir_to + "/" + filename, outname)
            os.system('tar -xvf ' + outname + " -C " + dir_to + "/")
            os.system('rm -r ' + outname)

    for filename in os.listdir(dir_to):
        for calSASid in SASidsCalibrator:
            if 'L' + str(calSASid) in filename:
                os.system("mv " + dir_to + "/" + filename + "  " + dir_to + "/" + "calibrators/" + str(calSASid) + "_RAW/")

        for tarSASid in SASidsTarget:
            if 'L' + str(tarSASid) in filename:
                os.system("mv " + dir_to + "/" + filename + "  " + dir_to + "/" + "targets/" + str(tarSASid) + "_RAW/")
