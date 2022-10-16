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
    i = 0
    j = 0
    cut = 100
    cut_W = 50
    nameT2 = 'output_F'
    for i in range(countI+1):
    #for i in range(20):
        name = nameT + '_' + '{0:04d}.jpeg'.format(i)
        #print(name)
        path = './output/' + name
        img = cv2.imread(path)
        cv2.imshow("Image", img)
        #cv2.waitKey()
        
        j_zero = str(j).zfill(4)
        nameF = nameT2 + '_' + j_zero + '.jpeg'
        
        if i == 0:
            cv2.imwrite(('output_F/' + nameF), img)
            img_Comp = img 
            j+=1
        else:
            #画像の大きさが同じかを判定
            #print(img.shape == img_Comp.shape)
            img_E = img[0+cut :height-cut , 0+cut_W :width-cut_W]
            img_Comp_E = img_Comp[0+cut :height-cut , 0+cut_W :width-cut_W ]
            img_gauss1 = cv2.GaussianBlur(img_E, (5, 5), 5)
            img_gauss2 = cv2.GaussianBlur(img_Comp_E, (5, 5), 5)
            
            #img_E_G = cv2.hconcat([img_E, img_gauss1])
            #img_Comp_E_G = cv2.hconcat([img_Comp_E, img_gauss2])
            if not np.array_equal(img_gauss1, img_gauss2):
                #bool = func3(img_E, img_Comp_E, i)
                bool = func3(img_gauss1, img_gauss2, i)
                print(str(i)+':'+str(bool))
                if bool:
                    cv2.imwrite(('output_F/' + nameF), img)
                    print('^'+str(j))
                    #img_Comp = img
                    j+=1
                img_Comp = img
                
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break


def func3(img, img_Comp, j):
    im_diff = img.astype(int) - img_Comp.astype(int)
    #print(im_diff.max())
    #print(im_diff.min())
    
    im_diff_abs = np.abs(im_diff)
    #print(im_diff_abs.max())
    #print(im_diff_abs.min())
    im_diff_abs_norm = im_diff_abs / im_diff_abs.max() * 255
    cv2.imwrite('./testF/diff_abs' + str(j) + '.png', im_diff_abs_norm)
    return func4(im_diff_abs_norm)


def func4(img):
    count_img_pixel = 0
    for i in range(0, height-200, 5):
        for j in range(0, width-100, 5):
            pixelValue = img[i, j]
            if np.all(pixelValue == 0):
                count_img_pixel += 1
                    
    result_4 = count_img_pixel / (1792 * 828 / 25)
    print('黒:'+str(result_4))
    if result_4 < 0.5:
    #if result_4 < 0.7:  #一つの動画に焦点を合わせすぎてしまうのも。。。
        return True
    else:
        return False


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