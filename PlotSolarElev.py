#!/usr/bin/env python3
"""
Computes solar irradiance and hence solar elevation angle for a year.
Updated to use AstroPy 1.0+, vectorized computation instead of PyEphem

If you'd like to incorporate a better spectral model like Lowtran or Hitran let me know.

Michael Hirsch
 Aug 2012 -- updated to Astropy Feb 2015
"""
from __future__ import absolute_import,division
import astropy.units as u
from astropy.coordinates import get_sun, EarthLocation, AltAz
from astropy.time import Time
from datetime import datetime
from warnings import warn
from dateutil.rrule import HOURLY,rrule
#
try:
    from .airMass import airmass
except:
    from airMass import airmass


def compsolar(site,coord,year,plotperhour,doplot):
    if isinstance(year,datetime):
        year=year.year
#%%
    site = site.lower()
    if len(site) == 0 and coord[0] is not None:
        obs = EarthLocation(lat=coord[0]*u.deg, lon=coord[1]*u.deg, height=coord[2]*u.m)
    elif site == "sondrestrom":
        obs = EarthLocation(lat=66.98*u.deg, lon=-50.94*u.deg, height=180*u.m)
    elif site=="pfisr":
        obs = EarthLocation(lat=65.12*u.deg, lon=-147.49*u.deg, height=210*u.m)
    elif site=="bu":
        obs = EarthLocation(lat=42.4*u.deg, lon=-71.1*u.deg, height=5*u.m)
    elif site=="svalbard":
        obs = EarthLocation(lat=78.23*u.deg, lon=15.4*u.deg, height=450*u.m)
    else:
        warn('you must specify a site or coordinates')
        return None, None

    plotperday = 24*plotperhour
    #don't fool around with Pandas or Numpy, since Numpy datetime64 doesn't work with Matplotlib
    times = list(rrule(HOURLY,
                       dtstart=datetime(year,1,1,0,0,0),
                       until=datetime(year,12,31,23,59,59)))

    dates = times[::plotperday]
    hoursofday = times[:plotperday]

    #yes, we need to feed times to observer and sun!
    sun = get_sun(Time(times)).transform_to(AltAz(obstime=times,location=obs))
    sunel = sun.alt.degree.reshape((plotperday,-1),order='F')

    Irr = airmass(sunel,times)[0]

    if doplot:
        lbl=MonthLocator(range(1,13),bymonthday=15,interval=1)
        fmt=DateFormatter("%b")
        plotIrr(dates,hoursofday,Irr,site,obs,lbl,fmt)
        plotyear(dates,hoursofday,sunel,site,obs,lbl,fmt)

        show()

    return Irr,sunel

def plotyear(dates,hoursofday,sunel,site,obs,lbl,fmt):
    fg = figure(figsize=(12,7),dpi=100)
    ax = fg.gca()
    V = (-18,-12,-6,-3,0,10,20,30,40,50,60,70,80,90)
    CS = ax.contour(dates,hoursofday,sunel,V)
    ax.clabel(CS, inline=1, fontsize=10,fmt='%0.0f')#, manual=manual_locations)
    ax.set_ylabel('UTC')
    ax.set_title(''.join(('Solar elevation angle (deg.)  ',site,': ',
                          str(obs.latitude),', ',str(obs.longitude))))
    ax.grid(True)
#    fg.autofmt_xdate()
    ax.xaxis.set_major_locator(lbl)
    ax.xaxis.set_major_formatter(fmt)

def plotIrr(dates,hoursofday,sunel,site,obs,lbl,fmt):
    fg = figure(figsize=(12,7),dpi=100)
    ax = fg.gca()
    CS = ax.contour(dates,hoursofday,sunel)
    ax.clabel(CS, inline=1, fontsize=10,fmt='%0.0f')#, manual=manual_locations)
    ax.set_ylabel('UTC')
    ax.set_title(''.join(('Sea level solar irradiance [W/m$^2$] at ',site,': ',
                          str(obs.latitude),', ',str(obs.longitude))))
    ax.grid(True)
#    fg.autofmt_xdate()
    ax.xaxis.set_major_locator(lbl)
    ax.xaxis.set_major_formatter(fmt)

def plotday(t,sunalt,site):
    ax = figure().gca()
    ax.plot(t,sunalt)
    ax.set_ylabel('Solar elevation [deg.]')
    ax.set_xlabel('UTC')
    ax.grid(True)
    ax.set_title(site + ' ' + t[0].strftime('%Y-%m-%d'))

if __name__ == '__main__':
    from matplotlib.dates import MonthLocator,DateFormatter
    from matplotlib.pyplot import figure,show

    from argparse import ArgumentParser
    p = ArgumentParser(description='plots solar elevation angle')
    pg = p.add_mutually_exclusive_group(required=True)
    pg.add_argument('-s','--site',help='use a prestored site [sondrestrom, pfisr, bu, svalbard]',type=str,default='')
    pg.add_argument('-c','--coord',help='specify site lat lon [degrees] ', nargs=3,type=float)
    p.add_argument('--pph', help='plot steps per hour (default 1)',type=int,default=1)
    p.add_argument('--noplot',help='disable plotting',action='store_false')
    p = p.parse_args()

    doplot = p.noplot

    Irr, sunel = compsolar(p.site, p.coord, 2013, p.pph, doplot)