#!/usr/bin/env python3


# Copyright 2019 Stichting Nederlandse Wetenschappelijk Onderzoek Instituten,
# ASTRON Netherlands Institute for Radio Astronomy
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# This is the Stager API wrapper module for the Lofar LTA staging service.
#
# It uses an xmlrpc proxy to talk and authenticate to the remote service. Your account credentials will be read from
# the awlofar catalog Environment.cfg, if present or can be provided in a .stagingrc file in your home directory.
#
# !! Please do not talk directly to the xmlrpc interface, but use this module to access the provided functionality.
# !! This is to ensure that when we change the remote interface, your scripts don't break and you will only have to
# !! upgrade this module.

__version__ = "1.5"

import sys
import os
import datetime
from os.path import expanduser
import threading

# Python2/3 dependent stuff
from sys import version_info
python_version = version_info.major
if python_version == 3:
    import xmlrpc.client as xmlrpclib
    string_types = str
else:
    import xmlrpclib
    string_types = basestring

from parsers._configparser import getConfigs

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


def stage(surls, send_notifications=True):
    """ Stage list of SURLs, optionally enable/disable email notifications """
    if isinstance(surls, str):
        surls = [surls]
    stageid = proxy.LtaStager.add_getid(surls, send_notifications)
    return stageid


def get_surls_online(stageid):
    """ Get a list of all files that are already online for a running request with given ID  """
    return proxy.LtaStager.getstagedurls(stageid)


def get_progress(status=None, exclude=False):
    """ Get a detailed list of all running requests and their current progress.
        As a normal user, this only returns your own requests.
        :param status: If set to a valid status then only requests with that
        status are returned.
        :param exclude: If set to True then the requests with status 'status' are
        excluded.
    """
    requests = {}
    try:
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
    except xmlrpclib.ProtocolError as error:
        print("AttributeError", error, sys.exc_info()[0])
    return requests


def download(surls, dir_to, SASidsCalibrator, SASidsTarget):
    """ Download file """
    config_file = "config.cfg"
    download_files = []
    dir_to_tmp = dir_to
    threads = []

    for surl in surls:
        if "sara" in surl:
            prefix = "https://lofar-download.grid.surfsara.nl/lofigrid/SRMFifoGet.py?surl="

        elif "juelich" in surl:
            prefix = "https://lofar-download.fz-juelich.de/webserver-lofar/SRMFifoGet.py?surl="

        else:
            prefix = "https://lta-download.lofar.psnc.pl/lofigrid/SRMFifoGet.py?surl="

        download_files.append(prefix + surl)

    def download_calibrator():
        for calSASid in SASidsCalibrator:
            dir_to = dir_to_tmp
            dir_to += "/" + "calibrators/" + str(calSASid) + "_RAW/"
            for file in download_files:
                if 'L' + str(calSASid) in file:
                    os.system("wget -P " + dir_to + " " + file)

        dir_to = dir_to_tmp
        for calSASid in SASidsCalibrator:
            dir_to = dir_to_tmp
            dir_to += "/" + "calibrators/" + str(calSASid) + "_RAW/"

            for file in os.listdir(dir_to):
                if 'L' + str(calSASid) in file:
                    if ".tar" in file:
                        t = threading.Thread(target=unarchive, args=(dir_to, file))
                        t.start()
                        threads.append(t)

    def download_target():
        for tarSASid in SASidsTarget:
            dir_to = dir_to_tmp
            dir_to += "/" + "targets/" + str(tarSASid) + "_RAW/"
            #for file in download_files:
                #if 'L' + str(tarSASid) in file:
                    #os.system("wget -P " + dir_to + " " + file)

        dir_to = dir_to_tmp
        for tarSASid in SASidsTarget:
            dir_to = dir_to_tmp
            dir_to += "/" + "targets/" + str(tarSASid) + "_RAW/"

            for file in os.listdir(dir_to):
                if 'L' + str(tarSASid) in file:
                    if ".tar" in file:
                        t = threading.Thread(target=unarchive, args=(dir_to, file))
                        t.start()
                        threads.append(t)

    if getConfigs("Operations", "which_obj", config_file) == "calibrators":
        download_calibrator()

    elif getConfigs("Operations", "which_obj", config_file) == "targets":
        download_target()
    else:
        download_calibrator()
        download_target()

    for t in threads:
        t.join()


def unarchive(dir_to, file):
    outname = dir_to + "/" + file.split("%")[-1]
    os.rename(dir_to + "/" + file, outname)
    os.system('tar -xvf ' + outname + " -C " + dir_to + "/")
    os.system('rm -r ' + outname)