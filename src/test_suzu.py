#動画の分割
#-*- coding: utf-8 -*-

from operator import truediv
import cv2, os
import numpy as np
import time
import glob
import imagehash
from PIL import Image

import matplotlib.pylab as plt # グラフの出力用

# グラフ出力用のlistをグローバル変数で用意しておく
xdata=[]
ydata=[]

#保存する画像数
countI = 201
#保存時の画像名
nameT = 'output1'
#画像の大きさ
width = 750
height = 1334

#動画名
name_MoV = 'input2.MP4'

#動画を読み込み、jフレームに１回保存
def func1():
    cap = cv2.VideoCapture('./input/' + name_MoV)
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
    #exit()


def func5():
    first_img = True
    j=0
    for i in range(countI-1):
        name1 = nameT + '_' + '{0:04d}.jpeg'.format(i)
        path = './output/' + name1
        image1 = cv2.imread(path)

        name2 = nameT + '_' + '{0:04d}.jpeg'.format(i+1)
        path = './output/' + name2
        image2 = cv2.imread(path)

        height = image1.shape[0]
        width = image1.shape[1]

        img_size = (int(width), int(height))

        # 比較するために、同じサイズにリサイズしておく
        image1 = cv2.resize(image1, img_size)
        image2 = cv2.resize(image2, img_size)

        #画素数が一致している割合を計算
        degree_of_similarity = np.count_nonzero(image1 == image2) / image2.size
        print(name1 + " 類似度：" + str(degree_of_similarity))
        
        y = degree_of_similarity
        ydata.append(y)

        #類似度が0.8より大きくなった瞬間の画像を保存
        if(degree_of_similarity > 0.8 and first_img):
            name3 = nameT + '_' + '{0:04d}.jpeg'.format(j)
            cv2.imwrite(('output_func5_2/' + name3), image1)
            j+=1
            first_img = False
        elif(degree_of_similarity <= 0.8):
            first_img = True
        
    print('読み込み完了')


def func6():
    i = 0
    j = 0
    nameT2 = 'output_F2'
    countI = 20
    for i in range(countI+1):
    #for i in range(20):
        name = nameT + '_' + '{0:04d}.jpeg'.format(i)
        img_path = './output_func5_2/' + name
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

def d_hash(img,otherimg):
    hash = imagehash.phash(Image.open(img))
    other_hash = imagehash.phash(Image.open(otherimg))
    return hash-other_hash


def func7():
    first_img = True
    j=0
    countI = 20
    for i in range(countI-1):
        name1 = nameT + '_' + '{0:04d}.jpeg'.format(i)
        path = './output_func5_2/' + name1
        image1 = cv2.imread(path)

        name2 = nameT + '_' + '{0:04d}.jpeg'.format(i+1)
        path = './output_func5_2/' + name2
        image2 = cv2.imread(path)

        height = image1.shape[0]
        width = image1.shape[1]

        img_size = (int(width), int(height))

        # 比較するために、同じサイズにリサイズしておく
        image1 = cv2.resize(image1, img_size)
        image2 = cv2.resize(image2, img_size)

        #画素数が一致している割合を計算
        degree_of_similarity = np.count_nonzero(image1 == image2) / image2.size
        print(name1 + ' : '+ name2 + " 類似度：" + str(degree_of_similarity))

        #類似度が0.8より大きくなった瞬間の画像を保存
        if(degree_of_similarity < 0.8):
            name3 = nameT + '_' + '{0:04d}.jpeg'.format(j)
            #cv2.imwrite(('output_func5_2/' + name3), image1)
            cv2.imwrite(('OO/' + name3), image2)
            print('^^')
            j+=1
            #first_img = False


def funcPlot():
    # 最後に一度だけ出力を行う
    xdata=np.arange(len(ydata)) # xdataにydataの長さの分連番データの作成
    fig, ax = plt.subplots() # グラフ出力の設定
    fig.suptitle("diff.abs.sum") # グラフ出力の設定
    plt.scatter(xdata, ydata, marker='.', lw=0) # 今回は散布図で出力　折線グラフとかも調べたらできるよ
    plt.show() # 出力

def main():
    func5()
    funcPlot()


if __name__ == '__main__':
	main()

