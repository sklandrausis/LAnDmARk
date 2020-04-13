#!/usr/bin/env python3
import sys
import argparse
from awlofar.toolbox.LtaStager import LtaStager


def parse_arguments():
    parser = argparse.ArgumentParser(description='''''')
    parser.add_argument('SASids', type=str)
    parser.add_argument('SURIs', type=str)
    arguments = parser.parse_args()
    return arguments


def start_staging(s_uris, sas_ids):
    for sas_id in sas_ids:
        stagger = LtaStager()
        stagger.stage_uris(s_uris[sas_id])


def main():
    args = parse_arguments()
    uris = args.SURIs.split("&")
    sas_ids = [int(sas_id) for sas_id in args.SASids.split("_")]

    s_uris = dict()
    for sas_id in range(0, len(sas_ids)):
        s_uris[sas_ids[sas_id]] = []
        for u in uris:
            s_uris[sas_ids[sas_id]].extend(u[0:len(u) - 1].split("#"))

    start_staging(s_uris, sas_ids)
    sys.exit(0)


if __name__ == "__main__":
    main()
