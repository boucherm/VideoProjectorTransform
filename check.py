import numpy as np
import cv2



if __name__ == '__main__':
    img = cv2.imread("img.png")

    h = img.shape[0]
    w = img.shape[1]

    #iHo = np.reshape( np.array( [0.95286768,-0.04116499,80.54139615,-0.03062313,0.96119319,78.36460165,-0.00004066,-0.00001609,1.08839725], dtype="float32"), (3,3) )
    with open("iHo.npy", "rb") as f:
        iHo = np.load(f)
    H = iHo

    #--- The transform estimated in vph.py works well when used by this very script.
    #--- Yet when given to xrandr, the output is different ( hence not what I want ).
    #--- The next commented lines are some attempts at finding the reason for this discrepancy
    #--- ( i.e. by replicating the output produced by xrandr )

    #- Is this a change of basis ?
    #P = np.array( [ [0, 1, 0], [1, 0, 0], [0, 0, 1] ], dtype="float32" );
    #P = np.array( [ [-1, 0, 0], [0, -1, 0], [0, 0, 1] ], dtype="float32" );
    #P = np.array( [ [1, 0, 0], [0, -1, 0], [0, 0, 1] ], dtype="float32" );
    #P = np.array( [ [-1, 0, 0], [0, -1, 0], [0, 0, 1] ], dtype="float32" );
    #H = P@iHo@P

    #- Is this a change of origin ?
    #T = np.array( [ [1, 0, 0], [0, 1, 0], [0, 0, 1] ], dtype="float32" );
    #T = np.array( [ [1, 0, -2560], [0, 1, 0], [0, 0, 1] ], dtype="float32" );
    #T = np.array( [ [1, 0, +2560], [0, 1, 0], [0, 0, 1] ], dtype="float32" );
    #T = np.array( [ [1, 0, 0], [0, 1, -1440], [0, 0, 1] ], dtype="float32" );
    #T = np.array( [ [1, 0, 0], [0, 1, +1440], [0, 0, 1] ], dtype="float32" );
    #T = np.array( [ [1, 0, -2560], [0, 1, -1440], [0, 0, 1] ], dtype="float32" );
    #T = np.array( [ [1, 0, -2560], [0, 1, +1440], [0, 0, 1] ], dtype="float32" );
    #T = np.array( [ [1, 0, +2560], [0, 1, -1440], [0, 0, 1] ], dtype="float32" );
    #T = np.array( [ [1, 0, +2560], [0, 1, +1440], [0, 0, 1] ], dtype="float32" );
    #H = iHo @ T

    #- Is this simply the inverse ?
    #H = np.linalg.inv( iHo )

    res = cv2.warpPerspective( img, H, (w,h) )

    cv2.namedWindow("res", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("res",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("res",res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("res.png", res)
