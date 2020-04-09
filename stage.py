import sys
import argparse
from awlofar.toolbox.LtaStager import LtaStager


def parse_arguments():
    parser = argparse.ArgumentParser(description='''''')
    parser.add_argument('SURIs', type=str, nargs='+')
    parser.add_argument('SASids', type=str, nargs='+')
    arguments = parser.parse_args()
    return arguments


def start_staging(s_uris, sas_ids):
    for sas_id in sas_ids:
        stagger = LtaStager()
        stagger.stage_uris(s_uris[sas_id])


def main():
    args = parse_arguments()
    uris = args.SURIs
    sas_ids = args.SASids
    print (uris, sas_ids)
    #start_staging(uris, sas_ids)
    sys.exit(0)


if __name__ == "__main__":
    main()
