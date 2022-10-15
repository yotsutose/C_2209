#動画の分割
#-*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import glob

#保存する画像数
countI = 52
#保存時の画像名
nameT = 'output1'

#動画を読み込み、jフレームに１回保存
def func1():
    cap = cv2.VideoCapture('./input/input1.MP4')
    print(cap.isOpened())
    if cap.isOpened == False:
        print("むり")
        exit()
        
    #動画の大きさ
    print("動画幅：", cap.get(cv2.CAP_PROP_FRAME_WIDTH)) #動画の幅
    print("動画高さ：", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  #動画の高さ
    #動画のフレーム規格
    print("フレ数/s：", cap.get(cv2.CAP_PROP_FPS))   #動画の1秒あたりのフレーム数
    print("全フレ数：", cap.get(cv2.CAP_PROP_FRAME_COUNT))   #動画の全てのフレーム数
    print("現在フレ：", cap.get(cv2.CAP_PROP_POS_FRAMES))   #動画の現在のフレームの位置
    
    #動画を１フレームごとに読み込んでウィンドウを起動、表示
    #現在、全読してるけど、iで読み込むやつ制限する必要あるかも（フレ数やばいから）
    i=0
    j=0
    
    # 時間計測開始
    time_sta = time.time()
    while(cap.isOpened()):
        ret, img = cap.read()

        if ret == True:
            cv2.imshow("Video", img)

            if i%10 == 0:
                j_zero = str(j).zfill(4)
                nameI = nameT + '_' + j_zero + '.jpeg'
                print(nameI)
                #画像の保存
                #cv2.imwrite(('output/' + nameI), img)
                j+=1
            
            #"q"を押すと終了
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
        
        else:
            break

        if i == cap.get(cv2.CAP_PROP_FRAME_COUNT)-5:
            countI = j-1
            print(countI)
            break

        i+=1

    cap.release()
    cv2.destroyAllWindows()

    # 時間計測終了
    time_end = time.time()
    # 経過時間（秒）
    tim = time_end- time_sta

    print("動画処理実行時間：",tim)
    exit()


def func2():
    print('aa')
    #files = glob.glob('./output/*.jpeg')
    for i in range(countI):
        name = nameT + '_' + '{0:04d}.jpeg'.format(i)
        print(name)
        img = cv2.imread('./output/' + name)
        cv2.imshow("Image", img)
        cv2.waitKey()


def main():
    func2()


if __name__ == '__main__':
	main()



"""
    for frame in files:
        img = cv2.imread(frame)
        cv2.imshow("Image", img)
        #"q"を押すと終了
        cv2.waitKey()
"""