#!/usr/bin/env python

##########################################################################
#
# Written my Janis Steinbergs
#
##########################################################################
#
# History
# 03/10/2019 Changed for the use with argparse and added basic documentation -- MI
#
#10/10/2019 adjusted axes add SAS id on data points add improve documentation -- JS
#
#05/11/2019 add colorbar -- JS

import sys
import argparse
from astropy.io import ascii
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import astropy.coordinates as coord
import astropy.units as u
import coloredlogs, logging


def main(csvFILE, radius=20.5, type="all"):
    """
    # radius = 20.5 in degrees.
    # type what to plot calibrtor, traget, imaging only or all

    #function open and parse csv file, that contains coordinates and QA values
    #function plot QA values map
    """
    coloredlogs.install(level='PRODUCTION')
    logger = logging.getLogger('QA_sky_overview')

    area = np.pi * radius ** 2

    # open and parse input csv file
    data = ascii.read(csvFILE)
    ras = coord.Angle(data["col3"][2:len(data["col3"])], unit=u.degree)
    ras = ras.wrap_at(180*u.degree)
    decs = coord.Angle(data["col4"][2:len(data["col4"])], unit=u.degree)
    sas_ids = data["col5"][2:len(data["col5"])]

    calibrators_qa_flags = data["col8"][2:len(data["col8"])]
    target_qa_flags = data["col11"][2:len(data["col11"])]
    target_qa_notes = data["col12"][2:len(data["col12"])]
    imaging_qa_flags = data["col13"][2:len(data["col13"])]
    imaging_qa_notes = data["col14"][2:len(data["col14"])]
    s0 = [(float(so.split(",")[0].split("=")[-1]), float(so.split(",")[1].split("=")[-1])) for so in target_qa_notes]
    s0_mean = [np.mean(soi) for soi in s0]
    s0_std = [np.std(soi) for soi in s0]
    

    for i in range(0, len(s0)):
        if s0_std[i] >= s0_mean[i] * 0.10:
            logger.warning("Warning standard deviation is equal to or larger than 10% from mean value of velocity of diffractive scale")

    rms = [float(iqn.split("=")[-1]) for iqn in imaging_qa_notes]

    z_calibrator = []
    z_target = []
    z_imaging = []

    l_calibrator = set()
    l_target = set()
    l_imaging = set()

    for c in calibrators_qa_flags:
        if c == "good":
            z_calibrator.append(1)
            l_calibrator.add("Good")

        elif c == "intermediate":
            z_calibrator.append(0.9)
            l_calibrator.add("Intermediate")

        elif c == "poor":
            z_calibrator.append(0.8)
            l_calibrator.add("Poor")

        elif c == "bad":
            z_calibrator.append(0.7)
            l_calibrator.add("Bad")

        else:
            z_calibrator.append(0.6)
            l_calibrator.add("Not processed")

    for c in target_qa_flags:
        if c == "good":
            z_target.append(1)
            l_target.add("Good")

        elif c == "intermediate":
            z_target.append(0.9)
            l_target.add("Intermediate")

        elif c == "poor":
            z_target.append(0.8)
            l_target.add("Poor")

        elif c == "bad":
            z_target.append(0.7)
            l_target.add("Bad")

        else:
            z_target.append(0.6)
            l_target.add("Not processed")

    for c in imaging_qa_flags:
        if c == "good":
            z_imaging.append(1)
            l_imaging.add("Good")

        elif c == "intermediate":
            z_imaging.append(0.9)
            l_imaging.add("Intermediate")

        elif c == "poor":
            z_imaging.append(0.8)
            l_imaging.add("Poor")

        elif c == "bad":
            z_imaging.append(0.7)
            l_imaging.add("Bad")

        else:
            z_imaging.append(0.6)
            l_imaging.add("Not processed")

    c_calibrator = []
    c_target = []
    c_imaging = []

    color = ["black", "red", "yellow", "blue", "green"]

    if 0.6 in z_calibrator:
        c_calibrator.append(color[0])

    if 0.7 in z_calibrator:
        c_calibrator.append(color[1])

    if 0.8 in z_calibrator:
        c_calibrator.append(color[2])

    if 0.9 in z_calibrator:
        c_calibrator.append(color[3])

    if 1 in z_calibrator:
        c_calibrator.append(color[4])

    if 1 in z_target:
        c_target.append(color[0])

    if 0.9 in z_target:
        c_target.append(color[1])

    if 0.8 in z_target:
        c_target.append(color[2])

    if 0.7 in z_target:
        c_target.append(color[3])

    if 0.6 in z_target:
        c_target.append(color[4])

    if 1 in z_imaging:
        c_imaging.append(color[0])

    if 0.9 in z_imaging:
        c_imaging.append(color[1])

    if 0.8 in z_imaging:
        c_imaging.append(color[2])

    if 0.7 in z_imaging:
        c_imaging.append(color[3])

    if 0.6 in z_imaging:
        c_imaging.append(color[4])

    # Summary info
    print('Plotting info about %d processed pointings' % len(calibrators_qa_flags))
    # print the number of processed calibrators / targets / imaged pointings
    # plotting section

    x_lim_single_plot = (min(ras.degree) -5, max(ras.degree) +5)
    y_lim_single_plot = (min(decs.degree)-600, max(decs.degree) +600)   

    if type == "all":

        fig1 = plt.figure(figsize=(radius, radius))
        fig1.tight_layout(pad=0, h_pad=0, w_pad=0, rect=None)
        plt.gca().invert_xaxis()
        scatter1 = plt.scatter(ras.degree, decs.degree, s=area, cmap="plasma", c=z_calibrator, edgecolor='black', alpha=0.7, linewidths=5)
        plt.title("Calibrator QA values")
        plt.colorbar(ticks=[t for t in np.linspace(min(z_calibrator), 1,  len(c_calibrator))], shrink=0.3, orientation="horizontal")
        plt.grid(True)
        plt.xlabel("RA, Degrees")
        plt.ylabel("DEC, Degrees")
        plt.xlim(x_lim_single_plot)
        plt.ylim(y_lim_single_plot)
        
        fig2 = plt.figure(figsize=(radius, radius))
        fig2.tight_layout(pad=0, h_pad=0, w_pad=0, rect=None)
        plt.gca().invert_xaxis()
        scatter2 = plt.scatter(ras.degree, decs.degree, s=area, cmap="plasma", c=s0_mean, edgecolor='black', alpha=0.7, linewidths=5)
        plt.legend(*scatter2.legend_elements(),loc="lower left", title="mean value of velocity of diffractive scale")
        plt.title("Target QA values")
        plt.colorbar(ticks=s0_mean, shrink=0.3, orientation="horizontal")
        plt.grid(True)
        plt.xlabel("RA, Degrees")
        plt.ylabel("DEC, Degrees")
        plt.xlim(x_lim_single_plot)
        plt.ylim(y_lim_single_plot)

        
        fig3 = plt.figure(figsize=(radius, radius))
        fig3.tight_layout(pad=0, h_pad=0, w_pad=0, rect=None)
        plt.gca().invert_xaxis()
        scatter3 = plt.scatter(ras.degree, decs.degree, s=area, cmap="plasma", c=rms, edgecolor='black', alpha=0.7, linewidths=5)
        plt.legend(*scatter3.legend_elements(),loc="lower left", title="rms values")
        plt.title("Imaging QA values")
        plt.colorbar(ticks=rms, shrink=0.5, orientation="horizontal")
        plt.grid(True)
        plt.xlabel("RA, Degrees")
        plt.ylabel("DEC, Degrees")
        plt.xlim(x_lim_single_plot)
        plt.ylim(y_lim_single_plot)
        plt.show()

    elif type == "calibrator":
        plt.figure(figsize=(5, 5))
        plt.gca().invert_xaxis()
        cm = mpl.colors.ListedColormap(c_calibrator)
        plt.scatter(ras.degree, decs.degree, s=area, cmap=cm, c=z_calibrator, edgecolor='black', alpha=0.5)
        plt.title("Calibrator QA values")
        plt.xlabel("RA, Degrees")
        plt.ylabel("DEC, Degrees")
        plt.xlim(x_lim_single_plot)
        plt.ylim(y_lim_single_plot)
        cbar_1 = plt.colorbar(ticks=[t for t in np.linspace(min(z_calibrator), 1, len(c_calibrator))], shrink=0.3, orientation="horizontal")
        cbar_1.ax.set_yticklabels(list(l_calibrator))
        for i, txt in enumerate(sas_ids):
            plt.annotate(txt, (ras[i].degree, decs[i].degree))
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    elif type == "target":
        plt.figure(figsize=(5, 5))
        plt.gca().invert_xaxis()
        cm = mpl.colors.ListedColormap(c_target)
        plt.scatter(ras.degree, decs.degree, s=area, cmap=cm, c=z_target, edgecolor='black', alpha=0.5)
        plt.title("Target QA values")
        plt.xlabel("RA, Degrees")
        plt.ylabel("DEC, Degrees")
        plt.xlim(x_lim_single_plot)
        plt.ylim(y_lim_single_plot)
        cbar_1 = plt.colorbar(ticks=[t for t in np.linspace(min(z_target), 1, len(c_target))], shrink=0.3, orientation="horizontal")
        cbar_1.ax.set_yticklabels(list(l_target))
        for i, txt in enumerate(sas_ids):
            plt.annotate(txt, (ras[i].degree, decs[i].degree))
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    elif type == "imaging":
        plt.figure(figsize=(5, 5))
        plt.gca().invert_xaxis()
        cm = mpl.colors.ListedColormap(c_imaging)
        plt.scatter(ras.degree, decs.degree, s=area, cmap="yet", c=z_imaging, edgecolor='black', alpha=0.5)
        plt.title("Imaging QA values")
        plt.xlabel("RA, Degrees")
        plt.ylabel("DEC, Degrees")
        plt.xlim(x_lim_single_plot)
        plt.ylim(y_lim_single_plot)
        cbar_1 = plt.colorbar(ticks=[t for t in np.linspace(min(z_imaging), 1, len(c_imaging))], shrink=0.3, orientation="horizontal")
        cbar_1.ax.set_yticklabels(list(l_imaging))
        for i, txt in enumerate(sas_ids):
            plt.annotate(txt, (ras[i].degree, decs[i].degree))
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate data quality overview sky plots of a given list of pointing.')
    parser.add_argument('inFILE', type=str, help='Specify the input csv file.')
    parser.add_argument('--inRADIUS', type=float, default=200.5, help='Sky projected cone radius [in degree] of each pointing (default: 2.)')
    parser.add_argument('--type', type=str, default="all", choices=['all','calibrator','target', 'imaging'], help='Plot types all, calibrator, target, imaging')
    args = parser.parse_args()
    # start running script
    main(args.inFILE, args.inRADIUS, args.type)
    sys.exit(0)
