#動画の分割
#-*- coding: utf-8 -*-

from distutils.command.config import config
import cv2
import numpy as np
import time
import glob
import imagehash
from PIL import Image

#保存する画像数
countI = 52
#countI = 0
#保存時の画像名
nameT = 'output1'
#画像の大きさ
width = 828
height = 1792

#動画を読み込み、jフレームに１回保存
def func1():
    cap = cv2.VideoCapture('./input/input1.MP4')
    print(cap.isOpened())
    if cap.isOpened == False:
        print("むり")
        exit()
        
    #動画の大きさ
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("動画幅：", width) #動画の幅
    print("動画高さ：", height)  #動画の高さ
    #動画のフレーム規格
    print("フレ数/s：", cap.get(cv2.CAP_PROP_FPS))   #動画の1秒あたりのフレーム数
    print("全フレ数：", cap.get(cv2.CAP_PROP_FRAME_COUNT))   #動画の全てのフレーム数
    print("現在フレ：", cap.get(cv2.CAP_PROP_POS_FRAMES))   #動画の現在のフレームの位置
    
    #動画を１フレームごとに読み込んでウィンドウを起動、表示
    #現在、10ずつで読み込む
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
    i = 0
    j = 0
    nameT2 = 'output_F'
    for i in range(countI+1):
    #for i in range(20):
        name = nameT + '_' + '{0:04d}.jpeg'.format(i)
        img_path = './output/' + name
        img = cv2.imread(img_path)
        cv2.imshow("Image", img)
        #cv2.waitKey()
        
        nameF = nameT2 + '_' + '{0:04d}.jpeg'.format(j)
        
        if i == 0:
            cv2.imwrite(('output_Re/' + nameF), img)
            hash = imagehash.average_hash(Image.open(img_path))
            print(hash) 
            #img_Comp = img
            img_Comp_path = img_path
            j+=1
        else:
            if d_hash(img_path, img_Comp_path) >= 16:
                cv2.imwrite(('output_Re/' + nameF), img)
                print('^'+str(j))
                j+=1
            #img_Comp = img
            img_Comp_path = img_path
            
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break



#Perceptual Hash値を使用して比較
#https://aws.amazon.com/jp/blogs/news/jpmne-automatically-compare-two-videos-to-find-common-content/
#「https://pypi.org/project/ImageHash/」
#2つの画像のハッシュ値の差分を出力
def d_hash(img,otherimg):
    hash = imagehash.phash(Image.open(img))
    other_hash = imagehash.phash(Image.open(otherimg))
    return hash-other_hash


def main():
    func2()


if __name__ == '__main__':
	main()

