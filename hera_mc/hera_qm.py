# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Handling quality metrics of HERA data.

"""
from __future__ import absolute_import, division, print_function

import numpy as np
from astropy.time import Time
from astropy.coordinates import EarthLocation
from sqlalchemy import Column, BigInteger, Float, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property

from hera_mc import geo_handling
from . import MCDeclarativeBase, DEFAULT_GPS_TOL, DEFAULT_DAY_TOL, DEFAULT_HOUR_TOL


class ant_metrics(MCDeclarativeBase):
    """
    Definition of ant_metrics table.

    obsid:      observation identification number, generally equal to the floor
                of the start time in gps seconds (long integer)
    ant:        Antenna number (int >= 0)
    pol:        Polarization ('x' or 'y')
    metric:     Name of metric (str)
    metric_id:  ID number within metric (int)
    mc_time:    time metric is reported to M&C in floor(gps seconds) (BigInteger)
    val:        Value of metric (double)
    """
    __tablename__ = 'ant_metrics'
    obsid = Column(BigInteger, ForeignKey('hera_obs.obsid'), primary_key=True)
    ant = Column(Integer, primary_key=True)
    pol = Column(String, primary=True)
    metric = Column(String, primary=True)
    metric_id = Column(Integer, primary=True)
    mc_time = Column(BigInteger, nullable=False)
    val = Column(Float, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['metric', 'metric_id'],
                                           ['desc_metrics.metrics',
                                            'desc_metrics.metric_id']))

    # tolerances set to 1ms
    tols = {'mc_time': DEFAULT_GPS_TOL}

    @hybrid_property
    def antpol(self):
        return (ant, pol)

    @hybrid_property
    def mmid(self):
        return (metric, metric_id)

    @classmethod
    def create(cls, obsid, ant, pol, metric, metric_id, db_time, val):
        """
        Create a new ant_metric object using Astropy to compute the LST.

        Parameters:
        ------------
        obsid: long integer
            observation identification number.
        ant: integer
            antenna number
        pol: string ('x' or 'y')
            polarization
        metric: string
            metric name
        metric_id: integer
            metric ID
        db_time: astropy time object
            astropy time object based on a timestamp from the database.
            Usually generated from MCSession.get_current_db_time()
        val: float
            value of metric
        """

        if not isinstance(obsid, (int, long)):
            raise ValueError('obsid must be an integer.')
        if not isinstance(ant, (int, long)):
            raise ValueError('antenna must be an integer.')
        if not isinstance(pol, str):
            raise ValueError('pol must be string "x" or "y".')
        pol = pol.lower()
        if pol not in ('x', 'y'):
            raise ValueError('pol must be string "x" or "y".')
        if not isinstance(metric, str):
            raise ValueError('metric must be string.')
        if not isinstance(metric_id, (int, long)):
            raise ValueError('metric_id must be an integer.')
        if not isinstance(db_time, Time):
            raise ValueError('db_time must be an astropy Time object')
        mc_time = floor(db_time.gps)
        try:
            val = float(val)
        except ValueError:
            raise ValueError('val must be castable as float.')

        return cls(obsid=obsid, ant=ant, pol=pol, metric=metric, metric_id=metric_id,
                   mc_time=mc_time, val=val)
