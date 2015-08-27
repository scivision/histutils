#!/usr/bin/env python3
"""
Plays video contained in HDF5 file, especially from rawDMCreader program.
"""
from __future__ import division,absolute_import
import h5py
from os.path import expanduser,splitext
from scipy.misc import bytescale
from numpy import dstack
#
#from histutils.sixteen2eight import sixteen2eight
from histutils.rawDMCreader import doPlayMovie

def playh5movie(h5fn,imgh5,outfn):
    h5fn = expanduser(h5fn)

    with h5py.File(h5fn,'r',libver='latest') as f:
        data = f[imgh5]
        try:
            ut1_unix = f['/ut1_unix']
        except:
            ut1_unix = None

        if outfn:
            hdf2video(data,h5fn,imgh5,outfn)
        else:
            doPlayMovie(data,0.1,ut1_unix=ut1_unix)

def hdf2video(data,h5fn,imgh5,outfn):
    import cv2
    try:
        from cv2.cv import FOURCC as fourcc #Windows needs from cv2.cv
    except Exception:
        from cv2 import VideoWriter_fourcc as fourcc

    stem = splitext(outfn)[0]
    outfn = stem + '.ogv'
    cc4 = fourcc(*'THEO')
    # we use isColor=True because some codecs have trouble with grayscale
    hv = cv2.VideoWriter(outfn,cc4, fps=36, frameSize=data.shape[1:], isColor=True) #right now we're only using grayscale
    if not hv.isOpened():
        raise TypeError('trouble starting video file')

    for d in data:
        #RAM usage explodes if scaling all at once on GB class file
    #for d in bytescale(data,1000,4000):
    #for d in sixteen2eight(data,(1000,4000)):
        hv.write(gray2rgb(bytescale(d,1000,4000)))

    hv.release()

def gray2rgb(gray):
    return dstack((gray,)*3)

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='play hdf5 video')
    p.add_argument('h5fn',help='hdf5 .h5 file with video data')
    p.add_argument('-p','--imgh5',help='path / variable inside hdf5 file to image stack (default=rawimg)',default='rawimg')
    p.add_argument('-o','--output',help='output new video file instead of playing back')
    p = p.parse_args()

    playh5movie(p.h5fn,p.imgh5,p.output)
