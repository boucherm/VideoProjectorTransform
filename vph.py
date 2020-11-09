# Notes to self
#
# Pygame examples:
# /usr/share/doc/python-pygame/examples
#
# doc:
# https://www.pygame.org/docs/ref/key.html

import math as m
import numpy as np
import pygame
from   pygame.locals import *
import sys
try:
  import cv2
  HAS_OPENCV = True
except:
  HAS_OPENCV = False



RADIUS  = 25
WIDTH   = 1
BLACK   = (0,0,0)
BLUE    = (0,0,255)
GREEN   = (0,255,0)
MAGENTA = (100,0,150)


def drawHandles( surf, corners ):
    # TODO give different colors to each
    for ii in range( len(corners) ):
        pygame.draw.circle( surf, BLUE, corners[ii], RADIUS )


def drawFrame( surf, corners, color ):
    for ii in range( len(corners) ):
        if ii == len(corners)-1:
            jj = 0
        else:
            jj = ii+1
        pygame.draw.line( surf, color, corners[ii], corners[jj], WIDTH )


def eucliDist( p1, p2 ):
    X1 = p1[0]
    Y1 = p1[1]
    X2 = p2[0]
    Y2 = p2[1]
    dX = X2 - X1
    dY = Y2 - Y1
    return m.sqrt( dX*dX + dY*dY )


def findClosestCorner( pos, corners ):
    min_dist = sys.float_info.max
    closest  = -1
    for ii in range( len(corners) ):
        corner = corners[ii]
        dist   = eucliDist( pos, corner )
        if dist < min_dist:
            min_dist = dist
            closest = ii
    return closest


def normalizeDet( M ):
    n_cols     = M.shape[1]
    det_M      = np.linalg.det(M)
    isNegative = False

    if ( det_M < 0 ) and ( n_cols % 2 == 0 ):
        raise ArithmeticError( "Attempting to find an even root of a negative number" )
    if ( det_M < 0 ):
        isNegative = True
        det_M = - det_M

    a = m.pow( 1./det_M, 1./n_cols )
    a = -a if isNegative else a

    return M * a


def computeHomographyMvg( xss, xds ):
    n = len(xss)
    A = np.zeros( (2*n,9) )
    for ii in range(n):
        l1 = 2*ii
        l2 = l1+1
        xs = xss[ii]
        xd = xds[ii]
        A[l1, 3] = -xs[0]
        A[l1, 4] = -xs[1]
        A[l1, 5] = -1.0

        A[l1, 6] = xd[1]*xs[0]
        A[l1, 7] = xd[1]*xs[1]
        A[l1, 8] = xd[1]*1.0

        A[l2, 0] = xs[0]
        A[l2, 1] = xs[1]
        A[l2, 2] = 1.0

        A[l2, 6] = -xd[0]*xs[0]
        A[l2, 7] = -xd[0]*xs[1]
        A[l2, 8] = -xd[0]*1.0

    u, s, vh = np.linalg.svd( A )
    H = np.reshape( vh[-1,:], (3,3) )
    H = normalizeDet( H )
    return H


def computeHomographyOcv( xss, xds ):
    src = np.array( [ [x, y] for (x,y) in xss ], dtype="float32" )
    dst = np.array( [ [x, y] for (x,y) in xds ], dtype="float32" )
    H   = cv2.getPerspectiveTransform(src, dst)
    return H


def computeHomography( xss, xds ):
    if HAS_OPENCV:
        return computeHomographyOcv( xss, xds )
    else:
        return computeHomographyMvg( xss, xds )


def testHomography( xss ):
    ## Create a "random" H as H=Hs*Ha*Hp
    # Hs
    s       = 1.3
    theta   = 0.2
    Hs      = np.eye(3)
    Hs[0,0] = s*m.cos( theta )
    Hs[0,1] = -s*m.sin( theta )
    Hs[1,0] = s*m.sin( theta )
    Hs[1,1] = s*m.cos( theta )
    Hs[0,2] = 3.0
    Hs[1,2] = 6.0
    # Ha
    Ha          = np.eye( 3 )
    K           = np.eye( 2 )
    K[0,0]      = 2
    K[0,1]      = 0.5
    K[1,1]      = 1.3
    Ha[0:2,0:2] = normalizeDet( K )
    # Hp
    Hp      = np.eye( 3 )
    Hp[2,0] = 1
    Hp[2,1] = 2
    # H
    H = normalizeDet( Hs @ Ha @ Hp )

    ## Make xds from xss and H
    xds = []
    for xs in xss:
        X = np.reshape( np.array( [xs[0],xs[1],1.0] ), (3,1) )
        Y = H @ X
        xds.append( (Y[0]/Y[2], Y[1]/Y[2] ) )

    ## Estimate H_est from xss and xds
    H_est = computeHomography( xss, xds )

    # Manual check
    print( "Check ground trust and estimated homographies are almost identical" )
    print( "H gdt: ", H )
    print( "H est: ", H_est )

    return H


def transformCorners( H, corners ):
    res = []
    for corner in corners:
        X = np.reshape( np.array( [corner[0],corner[1],1.0] ), (3,1) )
        Y = H @ X
        res.append( (Y[0]/Y[2], Y[1]/Y[2] ) )

    return res


if __name__ == '__main__':
    pygame.init()

    # Find size of display
    disp_info = pygame.display.Info()
    w = disp_info.current_w
    h = disp_info.current_h

    # Set up the drawing window
    screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )

    screen_corners = [ (0,0), (w-1,0), (w-1,h-1), (0,h-1) ]
    moved_corners  = [ (0,0), (w-1,0), (w-1,h-1), (0,h-1) ]
    iHo            = np.eye(3)

    #testHomography(corners)

    # Run until the user asks to quit
    running = True
    while running:

        # Events handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN and ( e.key == K_ESCAPE or e.key == K_q ):
                running = False
            elif e.type == pygame.KEYDOWN and ( e.key == K_RETURN ):
                iHo = computeHomography( screen_corners, moved_corners )
                print( "H:\n"\
                     + f"{iHo[0,0]:.8f},{iHo[0,1]:.8f},{iHo[0,2]:.8f},"\
                     + f"{iHo[1,0]:.8f},{iHo[1,1]:.8f},{iHo[1,2]:.8f},"\
                     + f"{iHo[2,0]:.8f},{iHo[2,1]:.8f},{iHo[2,2]:.8f}" )
                with open("iHo.npy", "wb") as f:
                    np.save(f, iHo)
            elif e.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                ii  = findClosestCorner( pos, moved_corners )
                # TODO update only if that keeps the polygon convex
                moved_corners[ii] = pos

        # Fill the background with black
        screen.fill( BLACK )

        # Draw selected borders
        drawHandles( screen, moved_corners )
        drawFrame( screen, moved_corners, GREEN )

        # Draw projected borders
        drawFrame( screen, transformCorners(iHo,screen_corners), MAGENTA )

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()
