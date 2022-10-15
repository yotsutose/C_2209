import cv2
import numpy as np
from tqdm import tqdm

def compare_image(img: np.ndarray, previous_img: np.ndarray):
  height, width, channels = img.shape[:3]
  pre_height, pre_width, channels = previous_img.shape[:3]
  diff = img.astype(int) - previous_img.astype(int)
  diff_abs = np.abs(diff)
  # diff_abs_norm = diff_abs / diff_abs.max() * 255 # 最大化しない方がいい
  mix_img = np.full((height+1, width*2+1, 3), 1280, dtype=np.uint8)
  mix_img[0:height,0:width] = img
  mix_img[0:pre_height,width:width+pre_width] = diff_abs
  print(f"{np.sum(diff_abs)=}")
  cv2.imshow("Video", mix_img)
  return

def func1():
  cap = cv2.VideoCapture('input/input1.MP4')
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  print(f'{width=} {height=} {frame_count=}')

  previous_img = None
  for i in tqdm(range(frame_count)):
    ret, img = cap.read()
    if ret == False:
      break
    img = cv2.resize(img, dsize=None, fx=1/20, fy=1/20)
    if i != 0:
      compare_image(img, previous_img)
      if cv2.waitKey(200) & 0xFF == ord('q'): 
        break
    previous_img = img
  cap.release()
  cv2.destroyAllWindows()


def main():
  func1()

if __name__ == '__main__':
	main()
