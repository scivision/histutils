#!/usr/bin/env python3
"""
Computes solar irradiance and hence solar elevation angle for a year.
Updated to use AstroPy 1.0+, vectorized computation instead of PyEphem
tested in Python 3.4 and Python 2.7
Michael Hirsch
 Aug 2012 -- updated to Astropy Feb 2015
"""
import astropy.units as u
from astropy.time import Time, TimeDelta
from astropy.coordinates import get_sun, EarthLocation, AltAz
from matplotlib.pyplot import figure,show
from datetime import datetime
#
from airMass import airmass

def main(site,coord,year,plotperhour,doplot):
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
        print('*** you must specify a site or coordinates')
        return None, None

    plotperday = 24*plotperhour
    dt = TimeDelta(3600/plotperhour, format='sec')
    times = Time(year+'-01-01T00:00:00',format='isot',scale='utc') + dt * range(365*plotperday)
    dates = times[::plotperday].datetime
    hoursofday = times[:plotperday].datetime

    #yes, we need to feed times to observer and sun!
    sun = get_sun(times).transform_to(AltAz(obstime=times,location=obs))
    sunel = sun.alt.degree.reshape((plotperday,-1),order='F')

    Irr = airmass(sunel)[0]

    if doplot:
        plotIrr(dates,hoursofday,Irr,site,obs)
        plotyear(dates,hoursofday,sunel,site,obs)

        show()

    return Irr,sunel

def plotyear(dates,hoursofday,sunel,site,obs):
    fg = figure(figsize=(12,7),dpi=110)
    ax = fg.gca()
    V = (-18,-12,-6,-3,0,10,20,30,40,50,60,70,80,90)
    CS = ax.contour(dates,hoursofday,sunel,V)
    ax.clabel(CS, inline=1, fontsize=10,fmt='%0.0f')#, manual=manual_locations)
    ax.set_ylabel('UTC')
    ax.set_title(''.join(('Solar elevation angle (deg.)  ',site,': ',
                          str(obs.latitude),', ',str(obs.longitude))))
    ax.grid(True)
    fg.autofmt_xdate()

def plotIrr(dates,hoursofday,sunel,site,obs):
    fg = figure(figsize=(12,7),dpi=110)
    ax = fg.gca()
    CS = ax.contour(dates,hoursofday,sunel)
    ax.clabel(CS, inline=1, fontsize=10,fmt='%0.0f')#, manual=manual_locations)
    ax.set_ylabel('UTC')
    ax.set_title(''.join(('Sea level solar irradiance [W/m$^2$] at ',site,': ',
                          str(obs.latitude),', ',str(obs.longitude))))
    ax.grid(True)
    fg.autofmt_xdate()
    show()

def plotday(t,sunalt,site):
    ax = figure().gca()
    ax.plot(t,sunalt)
    ax.set_ylabel('Solar elevation [deg.]')
    ax.set_xlabel('UTC')
    ax.grid(True)
    ax.set_title(site + ' ' + t[0].strftime('%Y-%m-%d'))

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='plots solar elevation angle')
    p.add_argument('-s','--site',help='use a prestored site [sondrestrom, pfisr, bu, svalbard]',type=str,default='')
    p.add_argument('-c','--coord',help='specify site lat lon [degrees] ', nargs=3,type=float,default=(None, None, None))
    p.add_argument('-y','--year',help='year to plot',type=str,default=datetime.now().strftime('%Y'))
    p.add_argument('--pph',help='plot steps per hour (default 1)',type=int,default=1)
    p.add_argument('--noplot',help='disable plotting',action='store_false')
    p.add_argument('--selftest',help='debug only',action='store_true')
    p = p.parse_args()

    if p.selftest:
        from numpy import isclose
        Irr,sunel = main('pfisr',(None,None,None), '2015', 1, False)
        assert isclose(Irr[6,174],   403.17394679495857)
        assert isclose(sunel[6,174],  9.0549755440225681)
    else:
        Irr, sunel = main(p.site, p.coord, p.year, p.pph, p.noplot)
