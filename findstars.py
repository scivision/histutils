#!/usr/bin/env python3
#from scipy.ndimage.filters import maximum_filter
from skimage.feature import peak_local_max
from astropy.io import fits
from skimage.draw import circle
from matplotlib.pyplot import figure, show
from matplotlib.colors import LogNorm
from os.path import expanduser
'''
Michael Hirsch 2014
Finds stars in FITS images (just ask and I'll add other formats)
GPLv3+

References:
http://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array
http://scikit-image.org/docs/dev/auto_examples/plot_peak_local_max.html?highlight=local%20maxima
'''

def getfitsimg(fn,clim=None):
    fn = expanduser(fn)
    try:
        with fits.open(fn,mode='readonly') as hdul:
            if hdul[0].header['NAXIS']==2: #gray image
                img = hdul[0].data
                print('loaded',img.dtype,'image data.')
            else:
                print('did not find image data in ' + fn + ' this may be a bug.')
    except OSError:
        print('could not find ' + fn)
        return None

    return img

def getstars(img,fn,mindist,relintthres):
    coord = peak_local_max(img,
                           min_distance=mindist, threshold_rel=relintthres,
                           exclude_border=False,indices=True)
    fg = figure()
    ax = fg.gca()
    hi = ax.imshow(img, cmap='jet',norm=LogNorm())
    fg.colorbar(hi).set_label('data numbers')

    ax.autoscale(False)
    '''
    x=col=coord[:,1]
    y=row=coord[:,0]
    '''
    ax.plot(coord[:, 1], coord[:, 0], 'r*',markersize=8)
#    ax.axis('off')
    ax.set_title(fn)
    return coord

def getstarsums(img,pks,crad):
    sums = []
    for p in pks: #iterate down rows
        c = circle(p[0], p[1], radius=crad, shape=img.shape)
        sums.append(img[c].sum())
    return sums

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('imgs',help='list of images you want to load',nargs='+',type=str)
    p.add_argument('-c','--crad',help='circle summation radius',type=int,default=4)
    p.add_argument('-m','--mindist',help='minimum distance to neighor peak (pixels)',type=int,default=80)
    p.add_argument('-r','--relintthres',help='minimum intensity relative to peak intensity',type=float,default=0.25)
    a = p.parse_args()
    fl = a.imgs
    crad = a.crad

    for f in fl:
        img = getfitsimg(f)
        if img is None: continue

        peaks = getstars(img,f,a.mindist,a.relintthres)

        sums = getstarsums(img,peaks,crad)
        print('rows',peaks[:,0])
        print('sums radius',crad,sums)
    show()