#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2016 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""This is meant to hold utility scripts for geo_location

"""
from __future__ import absolute_import, division, print_function

from hera_mc import geo_location, mc

import copy
import matplotlib.pyplot as plt

def split_arrays(args):
    """Get split out of the various sub-arrays.  Return dictionary keyed on type, with list of station_names"""
    sub_array_designators = ['HH','PI','PH','PP','S','N']
    sub_arrays = {}
    for sad in sub_array_designators:
        sub_arrays[sad] = []
    db = mc.connect_to_mc_db(args)
    with db.sessionmaker() as session:
        locations  = session.query(geo_location.GeoLocation).all()
        for a in locations:
            for sad in sub_array_designators:
                try:
                    hh = int(a.station_name)
                    test_for_sub = 'HH'[:len(sad)]
                except ValueError:
                    test_for_sub = a.station_name[:len(sad)]
                if test_for_sub == sad:
                    sub_arrays[sad].append(a.station_name)
    return sub_arrays

def plot_arrays(args, sub_arrays, overplot=None):
    """Plot the various sub-array types"""
    markers = {'HH':'ro','PH':'rs','PI':'gs','PP':'bd','S':'bs'}
    vpos = {'E':0,'N':1,'Z':2}
    plt.figure(args.xgraph+args.ygraph)
    db = mc.connect_to_mc_db(args)
    with db.sessionmaker() as session:
        for key in sub_arrays.keys():
            for loc in sub_arrays[key]:
                for a in session.query(geo_location.GeoLocation).filter(geo_location.GeoLocation.station_name==loc):
                    v = [a.easting,a.northing,a.elevation]
                plt.plot(v[vpos[args.xgraph]],v[vpos[args.ygraph]],markers[key])
    if overplot:
        plt.plot(overplot[vpos[args.xgraph]],overplot[vpos[args.ygraph]],'ys', markersize=10,label=overplot[3])
        plt.legend(loc='upper right')
    if args.xgraph!='Z' and args.ygraph!='Z':
        plt.axis('equal')
    plt.plot(xaxis=args.xgraph,yaxis=args.ygraph)
    plt.show()

def locate_station(args, sub_arrays):
    db = mc.connect_to_mc_db(args)
    try:
        station_search = int(args.locate)
        station_desig = geo_location.GeoLocation.station_number
    except ValueError:
        if args.locate[0] == 'H':
            station_search = args.locate[1:]
        else:
            station_search = args.locate
        station_desig = geo_location.GeoLocation.station_name
    with db.sessionmaker() as session:
        for a in session.query(geo_location.GeoLocation).filter(station_desig==station_search):
            for key in sub_arrays.keys():
                if a.station_name in sub_arrays[key]:
                    this_sub_array = key
                    break
            v = [a.easting,a.northing,a.elevation,a.station_name]
            if args.verbosity=='m' or args.verbose=='h':
                print('station_name: ',a.station_name)
                print('\tstation_number: ',a.station_number)
                print('\teasting: ',a.easting)
                print('\tnorthing: ',a.northing)
                print('\televation: ',a.elevation)
                print('\tsub-array: ',this_sub_array)
            else:
                print(a,this_sub_array)
    return v

if __name__=='__main__':
    parser = mc.get_mc_argument_parser()
    parser.add_argument('-g','--graph',help="Graph data of all elements",action='store_true')
    parser.add_argument('-s','--show',help='Graph and locate a station (same as geo.py -gl XX)',default=False)
    parser.add_argument('-l','--locate',help="Print out location of given station_name. Prepend with 'h' for HH station_name. Integer if station_number",default=False)
    parser.add_argument('-v','--verbosity',help="Set verbosity {l,m,h}.",default="m")
    parser.add_argument('-x','--xgraph',help='X-axis of graph {N,E,Z} [E]',default='E')
    parser.add_argument('-y','--ygraph',help='Y-axis of graph {N,E,Z} [N]',default='N')
    args = parser.parse_args()
    args.xgraph = args.xgraph.upper()
    args.ygraph = args.ygraph.upper()
    sub_arrays = split_arrays(args)
    located = None
    if args.show:
        args.locate = args.show 
        args.graph = True
    if args.locate:
        args.locate = args.locate.upper()
        located = locate_station(args, sub_arrays)
    if args.graph:
        plot_arrays(args,sub_arrays,located)