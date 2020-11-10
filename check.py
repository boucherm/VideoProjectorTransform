import numpy as np
import cv2



if __name__ == '__main__':
    img = cv2.imread("img.png")

    h = img.shape[0]
    w = img.shape[1]

    with open("oHi.npy", "rb") as f:
        oHi = np.load(f)

    res = cv2.warpPerspective( img, oHi, (w,h) )

    cv2.namedWindow("res", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("res",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("res",res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("res.png", res)
