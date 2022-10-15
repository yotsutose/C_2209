import cv2
import numpy as np

def func1():
  cap = cv2.VideoCapture('input/input1.MP4')
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  print(f'{width=} {height=} {frame_count=}')
  while(cap.isOpened()):
    ret, img = cap.read()
    if ret == False:
      break
    # img = cv2.resize(img, dsize=None, fx=0.1, fy=0.1)
    # img = cv2.resize(img, dsize=None, fx=10, fy=10)
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  cap.release()
  cv2.destroyAllWindows()


def main():
    func1()

if __name__ == '__main__':
	main()
