import tkinter
import tkinter.filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from tqdm import tqdm # プログレスバーの導入

class Model():

    def __init__(self):

        # 動画オブジェクト参照用
        self.cap= None

        # 読み込んだフレーム
        self.frames = []

        # PIL画像オブジェクト参照用
        self.image = None

        # Tkinter画像オブジェクト参照用
        self.image_tk = None

        # 現在表示中のフレーム
        self.now = tkinter.IntVar()

        self.create_video("./input/input1.MP4")

    def create_video(self, path):
        '動画オブジェクトの生成を行う'


        # pathの動画から動画オブジェクト生成
        self.cap = cv2.VideoCapture(path)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f'{width=} {height=} {frame_count=}')

        self.frames = []
        for i in tqdm(range(frame_count)):
            ret, img = self.cap.read()
            if ret == False:
                break
            # 画像をリサイズする　20分の1に圧縮
            if i % 20 != 0:
                continue
            rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            pil_image = pil_image.resize((round(width/4), round(height/4)), resample=3)
            self.frames.append(ImageTk.PhotoImage(pil_image))

    def next_frame(self):
        next = min(self.now.get()+1, len(self.frames)-1)
        self.now.set(next)

    def previous_frame(self):
        next = max(self.now.get()-1, 0)
        self.now.set(next)


class View():

    def __init__(self, app, model):

        self.master = app
        self.model = model

        # アプリ内のウィジェットを作成
        self.create_widgets()

    def create_widgets(self):
        'アプリ内にウィジェットを作成・配置する'

        # キャンバスのサイズ
        canvas_width = 1200
        canvas_height = 900

        # キャンバスとボタンを配置するフレームの作成と配置
        self.main_frame = tkinter.Frame(
            self.master
        )
        self.main_frame.pack()

        # キャンバスを配置するフレームの作成と配置
        self.canvas_frame = tkinter.Frame(
            self.main_frame
        )
        self.canvas_frame.grid(column=1, row=1)

        # ユーザ操作用フレームの作成と配置
        self.operation_frame = tkinter.Frame(
            self.main_frame
        )
        self.operation_frame.grid(column=1, row=2)

        # キャンバスs
        self.canvases = [tkinter.Canvas(
            self.canvas_frame,
            width=canvas_width/5.5,
            height=canvas_height/2,
            bg="#EEEEEE",) for x in range(7)]
        
        for i in range(len(self.canvases)):
            self.canvases[i].pack(fill = 'x', padx=0, side = 'left')

        # # キャンバスの作成と配置
        # self.canvas = tkinter.Canvas(
        #     self.canvas_frame,
        #     width=canvas_width/4,
        #     height=canvas_height,
        #     bg="#EEEEEE",
        # )
        # self.canvas.pack(fill = 'x', padx=20, side = 'left')

        # # キャンパス2
        # self.canvas2 = tkinter.Canvas(
        #     self.canvas_frame,
        #     width=canvas_width/4,
        #     height=canvas_height,
        #     bg="#FFFFFF",
        # )
        # self.canvas2.pack(fill = 'x', padx=20, side = 'left')
        

        # ファイル読み込みボタンの作成と配置
        self.load_button = tkinter.Button(
            self.operation_frame,
            text="動画選択"
        )
        self.load_button.pack()


        # グレーON/OFFボタンの作成と配置
        self.gray_button = tkinter.Button(
            self.operation_frame,
            text="Next Frame"
        )
        self.gray_button.pack()

        # フリップ/OFFボタンの作成と配置
        self.flip_button = tkinter.Button(
            self.operation_frame,
            text="Previous Frame"
        )
        self.flip_button.pack()

        # val = tkinter.IntVar()
        self.scale_bar = ttk.Scale(
            self.operation_frame,
            variable=self.model.now,
            orient=tkinter.HORIZONTAL,
            length=600,
            from_=0 + 4,
            to=len(self.model.frames)-1 - 4,
            command=lambda e: self.draw_image())
        self.scale_bar.pack()

    def select_open_file(self, file_types):
        'オープンするファイル選択画面を表示'

        # ファイル選択ダイアログを表示
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=".",
            filetypes=file_types
        )
        return file_path

    def draw_image(self):
        '画像をキャンバスに描画'

        for i in range(len(self.canvases)):
            image = self.model.frames[self.model.now.get() - 2 + i]

            if image is None:
                continue
            # キャンバス上の画像の左上座標を決定
            sx = (self.canvases[0].winfo_width() - image.width()) // 2
            sy = (self.canvases[0].winfo_height() - image.height()) // 2

            # 画像をキャンバスの真ん中に描画
            self.canvases[i].delete('all')
            self.canvases[i].create_image(
                sx, sy,
                image=image,
                anchor=tkinter.NW,
                tag="image"
            )

class Controller():

    def __init__(self, app, model, view):
        self.master = app
        self.model = model
        self.view = view

        self.set_events()

    def set_events(self):
        '受け付けるイベントを設定する'

        # キャンバス上のマウス押し下げ開始イベント受付
        self.view.canvases[0].bind(
            "<ButtonPress-1>",
            self.button_press
        )

        # 動画選択ボタン押し下げイベント受付
        self.view.load_button['command'] = self.push_load_button

        # モノクロON/OFFボタン押し下げイベント受付
        self.view.gray_button['command'] = self.push_gray_button

        # フリップON/OFFボタン押し下げイベント受付
        self.view.flip_button['command'] = self.push_flip_button
        
    def push_load_button(self):
        '動画選択ボタンが押された時の処理'

        file_types = [
            ("MOVファイル", "*.mov"),
            ("MP4ファイル", "*.mp4"),
        ]

        # ファイル選択画面表示
        file_path = self.view.select_open_file(file_types)

        if len(file_path) != 0:

            # 動画オブジェクト生成
            self.model.create_video(file_path)

            # 最初のフレームを表示
            self.model.advance_frame()
            self.model.create_image(
                (
                    self.view.canvas.winfo_width(),
                    self.view.canvas.winfo_height()
                )
            )
            self.model.reverse_video()
            self.view.draw_image()

    def button_press(self, event):
        'マウスボタン押された時の処理'

        # 動画の再生/停止を切り替える
        if not self.playing:
            self.playing = True

            # 再生ボタンの削除
            self.view.delete_play_button()
        else:
            self.playing = False
            
            # 再生ボタンの描画
            self.view.draw_play_button()

    def push_gray_button(self):
        print("push")
        self.model.next_frame()
        self.view.draw_image()
        # print(self.model.now)

    def push_flip_button(self):
        print("push")
        self.model.previous_frame()
        self.view.draw_image()
        # print(self.model.now)


app = tkinter.Tk()

app.title("らくらくトリセツ")

model = Model()
view = View(app, model)
controller = Controller(app, model, view)

app.mainloop()