#キーボードの検出
#-*- coding: utf-8 -*-
#https://algorithm.joho.info/programming/python/opencv-template-matching-ssd-py/

from itertools import count
from unicodedata import name
import cv2
from cv2 import waitKey
import numpy as np

count = 5

def keyMatching():
    
    for i in range(count):
        print(i)
        # 入力画像とテンプレート画像をで取得
        name = 'output' + str(i) + '.jpeg'
        img = cv2.imread('./keytest/'+ name)
        temp = cv2.imread('./input/keyboard2.jpeg')

        # グレースケール変換
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)

        # テンプレート画像の高さ・幅
        h, w = temp.shape
        print(temp.shape)

        # テンプレートマッチング（OpenCVで実装）
        match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
        min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
        pt = max_pt
        print('min>> ' + str(min_value))
        print('max>> ' + str(max_value))

        # テンプレートマッチングの結果を出力
        nameM = 'Match' + str(i) + '.jpeg'
        cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 200), 3)
        cv2.imwrite('./keytest_O/'+ nameM, img)


def keyMatching2():
    
    temp = cv2.imread('./input/keyboard3.jpeg')
    # テンプレート画像の高さ・幅
    h, w = temp.shape[:2]

    for i in range(count):
        print(i)
        # 入力画像とテンプレート画像をで取得
        name = 'output' + str(i) + '.jpeg'
        img = cv2.imread('./keytest/'+ name)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        print(img.shape)
        
        for j in range(10):
            #cv2.imshow('',img)
            #cv2.waitKey()
            print('phase' + str(j))
            re = j/10
            size = (int(w*(1+re)), int(h*(1+re)))
            print(size)
            if size[0] > img.shape[1]:
                break
            
            temp_resize = cv2.resize(temp, size)
            #cv2.imshow('',temp_resize)
            #cv2.waitKey()
            print('re')
            print(temp_resize.shape)
            
            # グレースケール変換
            temp_g = cv2.cvtColor(temp_resize, cv2.COLOR_RGB2GRAY)

            # テンプレートマッチング（OpenCVで実装）
            match = cv2.matchTemplate(gray, temp_g, cv2.TM_CCOEFF_NORMED)
            min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
            pt = max_pt
            print('min>> ' + str(min_value))
            print('max>> ' + str(max_value))

            if max_value > 0.8:
                # テンプレートマッチングの結果を出力
                nameM = 'Match' + str(i) + '.jpeg'
                cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 200), 3)
                cv2.imwrite('./keytest_O/'+ nameM, img)
                break


def keyMatching3():
    
    temp = cv2.imread('./input/keyboard.jpeg')
    # テンプレート画像の高さ・幅
    h, w = temp.shape[:2]
    print(temp.shape)

    for i in range(count):
        print(i)
        # 入力画像とテンプレート画像をで取得
        name = 'output' + str(i) + '.jpeg'
        img = cv2.imread('./keytest/'+ name)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        print(img.shape)
        
        temp_resize = temp
        
        print('Iw:'+str(img.shape[1]) + ' Tw:' + str(temp.shape[1]))
        if img.shape[1] > temp.shape[1]:
            re = img.shape[1] / temp.shape[1]
            size = (img.shape[1], int(h*re))
            print(size)
            if size[0] > img.shape[1]:
                break
            
            temp_resize = cv2.resize(temp, size)
            cv2.imshow('',temp_resize)
            cv2.waitKey()
            print('re')
            print(temp_resize.shape)
        
            
        # グレースケール変換
        temp_g = cv2.cvtColor(temp_resize, cv2.COLOR_RGB2GRAY)

        # テンプレートマッチング（OpenCVで実装）
        match = cv2.matchTemplate(gray, temp_g, cv2.TM_CCOEFF_NORMED)
        min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
        pt = max_pt
        print('min>> ' + str(min_value))
        print('max>> ' + str(max_value))

        if max_value > 0.9:
            # テンプレートマッチングの結果を出力
            nameM = 'Match' + str(i) + '.jpeg'
            cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 200), 3)
            cv2.imwrite('./keytest_O/'+ nameM, img)


def main():
    print('main')
    keyMatching2()


if __name__ == '__main__':
	main()
