#!/usr/bin/env python3
import sys
import argparse
from services.stager_access import download


def parse_arguments():
    parser = argparse.ArgumentParser(description='''''')
    parser.add_argument('surls', type=str)
    parser.add_argument('dir_to', type=str)
    parser.add_argument('SASidsCalibrator', type=str)
    parser.add_argument('SASidsTarget', type=str)
    arguments = parser.parse_args()
    return arguments


def main():
    args = parse_arguments()
    surls = list(set(args.surls.split("#")))
    dir_to = args.dir_to
    SASidsCalibrator = [int(s) for s in args.SASidsCalibrator.split("_")]
    SASidsTarget = [int(s) for s in args.SASidsTarget.split("_")]
    download(surls, dir_to, SASidsCalibrator, SASidsTarget)
    sys.exit(0)


if __name__ == "__main__":
    main()