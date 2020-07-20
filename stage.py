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
        print(s_uris[sas_id])
        stagger = LtaStager()
        stagger.stage_uris(set(s_uris[sas_id]))


def main():
    args = parse_arguments()
    uris = args.SURIs[0:len(args.SURIs) - 1].split("#")
    sas_ids = [int(sas_id) for sas_id in args.SASids.split("_")]

    s_uris = dict()
    for sas_id in range(0, len(sas_ids)):
        s_uris[sas_ids[sas_id]] = set()

        for uri in uris:
            if "L" + str(sas_ids[sas_id]) in uri:
                s_uris[sas_ids[sas_id]].add(uri)

    start_staging(s_uris, sas_ids)
    sys.exit(0)


if __name__ == "__main__":
    main()
