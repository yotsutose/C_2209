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

        # mode 0:プレビュー、1:編集
        self.mode = tkinter.IntVar()
        self.mode.set(0)

        # 読み込んだフレームの選択状態 1:選択、0:未選択
        # 最初から2は消しておくかもしれない
        # 0と1しかない予定
        self.frame_state = []

        # PIL画像オブジェクト参照用
        self.image = None

        # Tkinter画像オブジェクト参照用
        self.image_tk = None

        # 現在表示中のフレーム
        self.now = tkinter.IntVar()
        self.nows = []
        for x in range(7):
            self.nows.append(tkinter.IntVar())
            self.nows[x].set(-1)

        self.now.trace_add("write", self.set_nows)

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
            if i % 30 != 0:
                continue
            rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            pil_image = pil_image.resize((round(width/4), round(height/4)), resample=3)
            self.frames.append(ImageTk.PhotoImage(pil_image))
        self.frame_state = []
        for x in range(len(self.frames)):
            self.frame_state.append(tkinter.IntVar())
        # セットする
        self.now.set(3)

    def set_nows(self, a, b, c):
        for x in range(7):
            self.nows[x].set(-1)
        if self.mode.get() == 0: # プレビュー
            now = self.now.get()
            idx = 1
            for i in range(now, len(self.frames), 1):
                if self.frame_state[i].get() == 1:
                    self.nows[idx].set(i)
                    idx += 1
                if idx > 5:
                    break
        else:
            # 0用
            for i in range(self.now.get()-3, -1, -1):
                if self.frame_state[i].get() == 1:
                    self.nows[0].set(i)
                    break
            # 12345用
            for i in range(5):
                state_ = self.now.get() + i - 2
                if state_ < 0 or len(self.frames) <= state_:
                    continue
                self.nows[i+1].set(state_)
            # 6用
            for i in range(self.now.get()+3, len(self.frames), 1):
                if self.frame_state[i].get() == 1:
                    self.nows[6].set(i)
                    break

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

        # callbackを用意
        # for x in range(7):
        #     self.model.nows[x].trace_add("write", lambda name, index, mode: self.make_draw_image(self, x))

        self.model.nows[0].trace_add("write", lambda name, index, mode: self.draw_image(self, 0))
        self.model.nows[1].trace_add("write", lambda name, index, mode: self.draw_image(self, 1))
        self.model.nows[2].trace_add("write", lambda name, index, mode: self.draw_image(self, 2))
        self.model.nows[3].trace_add("write", lambda name, index, mode: self.draw_image(self, 3))
        self.model.nows[4].trace_add("write", lambda name, index, mode: self.draw_image(self, 4))
        self.model.nows[5].trace_add("write", lambda name, index, mode: self.draw_image(self, 5))
        self.model.nows[6].trace_add("write", lambda name, index, mode: self.draw_image(self, 6))

        # アプリ内のウィジェットを作成
        self.create_widgets()

    def create_widgets(self):
        'アプリ内にウィジェットを作成・配置する'

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # キャンバスとボタンとタイトル配置するフレームの作成と配置
        self.main_frame = tkinter.Frame(
            self.master,
            bg="#FCFFEE"
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        # self.main_frame.pack()
        self.main_frame.tkraise()

        # 上の表示を配置するフレームの作成と配置
        self.head_frame = tkinter.Frame(
            self.main_frame,
            height=200,
            width=700,
            bg="#FCFFEE"
        )
        self.head_frame.grid(column=1, row=1)

        # キャンバスを配置するフレームの作成と配置
        self.canvas_frame = tkinter.Frame(
            self.main_frame,
            bg="#FCFFEE"
        )
        self.canvas_frame.grid(column=1, row=2)

        # ユーザ操作用フレームの作成と配置
        self.operation_frame = tkinter.Frame(
            self.main_frame,
            bg="#FCFFEE"
        )
        self.operation_frame.grid(column=1, row=3)

        # 下の表示を配置するフレームの作成と配置
        self.head_frame = tkinter.Frame(
            self.main_frame,
            height=50,
            width=700,
            bg="#FCFFEE"
        )
        self.head_frame.grid(column=1, row=4)

        # キャンバスのフレーム
        self.canvas_paneles = [tkinter.Frame(
            self.canvas_frame,
            bg="#FCFFEE",) for x in range(7)]
        [self.canvas_paneles[x].grid(column=x, row=1) for x in range(7)]

        # キャンバスごとのフレーム番号表示
        self.frame_index = [tkinter.Label(
            self.canvas_paneles[x],
            bg="#FCFFEE",
            font=("MSゴシック", "30", "bold"),
            textvariable=self.model.nows[x]) for x in range(7)]
        [self.frame_index[x].grid(row=0, column=0, sticky="nsew") for x in range(7)]

        # キャンバスごとのフレーム表示
        self.frame = [tkinter.Canvas(
            self.canvas_paneles[x],
            width=220,
            height=480,
            highlightbackground='#FCFFEE',
            bg='#FCFFEE'
            ) for x in range(7)]
        [self.frame[x].grid(row=1, column=0, sticky="nsew") for x in range(7)]

        # キャンバスのボタンのためのフレーム
        self.button_frame = [tkinter.Frame(
            self.canvas_paneles[x],
            highlightbackground='#FCFFEE',
            bg='#FCFFEE'
            ) for x in range(7)]
        [self.button_frame[x].grid_rowconfigure(0, weight=1) for x in range(7)]
        [self.button_frame[x].grid_columnconfigure(0, weight=1) for x in range(7)]
        [self.button_frame[x].grid(row=2, column=0, sticky="nsew") for x in range(7)]
        
        # [self.frame[x].pack() for x in range(7)]

        # キャンパスごとのボタン表示
        self.state_button = [tkinter.Button(
            self.button_frame[x],
            text="追加",
            highlightbackground='blue'
            ) for x in range(7)]
        [self.state_button[x].grid(row=0, column=0) for x in range(7)]
        

        # キャンパスごとのボタン表示
        self.state_button2 = [tkinter.Button(
            self.button_frame[x],
            text="削除",
            highlightbackground='red'
            ) for x in range(7)]
        [self.state_button2[x].grid(row=0, column=0) for x in range(7)]

        [self.state_button[x].tkraise() for x in range(7)]
        # [self.state_button2[x].tkraise() for x in range(7)]

        # 練習用のフレーム
        self.my_frame = tkinter.Frame(
            self.master,
            bg="#FCFFEE"
        )
        self.my_frame.grid(row=0, column=0, sticky="nsew")
        self.my_frame.tkraise()
        self.main_frame.tkraise()

        # ファイル読み込みボタンの作成と配置
        self.load_button = tkinter.Button(
            self.operation_frame,
            text="動画選択",
            highlightbackground='#FCFFEE'
        )
        self.load_button.pack()

        style = ttk.Style()
        style.configure(
            "Horizontal.TScale",
            background="cyan"
        )
        self.scale_bar = ttk.Scale(
            self.operation_frame,
            style="TScale",
            variable=self.model.now,
            orient="horizontal",
            length=600,
            from_=0,
            to=len(self.model.frames)-1,
            # command=lambda e: self.draw_image()
        )

        # self.scale_bar = tkinter.Scale(
        #     self.operation_frame,
        #     variable=self.model.now,
        #     orient=tkinter.HORIZONTAL,
        #     bg='#FCFFEE',
        #     troughcolor='#FCFFEE',
        #     length=600,
        #     from_=0,
        #     sliderlength=15,
        #     to=len(self.model.frames)-1,
        #     # command=lambda e: self.draw_image()
        # )
        self.scale_bar.pack()

        # グレーON/OFFボタンの作成と配置
        self.gray_button = tkinter.Button(
            self.operation_frame,
            text="Next Frame",
            highlightbackground='#FCFFEE'
        )
        self.gray_button.pack(fill = 'x', padx=20, side = 'right')

        # フリップ/OFFボタンの作成と配置
        self.flip_button = tkinter.Button(
            self.operation_frame,
            text="Previouss Frame",
            highlightbackground='#FCFFEE'
        )
        self.flip_button.pack(fill = 'x', padx=20, side = 'left')

        # modeのON/OFFボタンの作成と配置
        mode_button_image_ = Image.open('./input/IMG_0240.png')
        mode_button_image = ImageTk.PhotoImage(mode_button_image_)
        # mode_button_image = tkinter.PhotoImage(file='./input/IMG_0240.png')
        self.mode_button = tkinter.Button(
            self.operation_frame,
            text="change mode",
            image=mode_button_image,
            highlightbackground='#FCFFEE'
        )
        self.mode_button.image = mode_button_image
        self.mode_button.pack()

    def select_open_file(self, file_types):
        'オープンするファイル選択画面を表示'

        # ファイル選択ダイアログを表示
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=".",
            filetypes=file_types
        )
        return file_path

    # def make_draw_image(self, name, index):
    #     return lambda: self.draw_image(self, "", index)

    def draw_image(self, name, index):
        i = index
        alli = self.model.nows[index].get()
        'buttonの切り替え'
        state_ = self.model.frame_state[alli].get()
        if state_ == 1: # 選択されているので、削除ボタンを表示
            self.state_button2[i].tkraise()
        else: # 選択されていないので、追加ボタンを表示
            self.state_button[i].tkraise()
        
        '画像をキャンバスに描画'
        self.frame[i].delete('all')
        if alli < 0 or len(self.model.frames) <= alli:
            return
        image = self.model.frames[alli]
        self.frame[i].create_image(
            0, 0,
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

        # 動画選択ボタン押し下げイベント受付
        self.view.load_button['command'] = self.push_load_button

        # モノクロON/OFFボタン押し下げイベント受付
        self.view.gray_button['command'] = self.push_gray_button

        # フリップON/OFFボタン押し下げイベント受付
        self.view.flip_button['command'] = self.push_flip_button

        # modeON/OFFボタン押し下げイベント受付
        self.view.mode_button['command'] = self.push_mode_button

        for x in range(7):
            self.view.state_button[x]['command'] = self.make_push_state_button(x)    
        
        for x in range(7):
            self.view.state_button2[x]['command'] = self.make_push_state_button(x)    
        
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

    def push_gray_button(self):
        self.model.next_frame()

    def push_flip_button(self):
        self.model.previous_frame()

    # ここではボタン押したら、今の数字のやつのstate切り替えと、再び表示がしたい、真ん中に真ん中を入れたらおけ
    def make_push_state_button(self, x):
        return lambda: self.push_state_button(x)

    def push_state_button(self, x):
        index = self.model.nows[x].get()
        if index < 0 or len(self.model.frames) <= index:
            return
        self.model.frame_state[index].set((self.model.frame_state[index].get()+1)%2)
        # print([self.model.frame_state[x].get() for x in range(len(self.model.frame_state))])
        # 全体の更新
        self.model.now.set(self.model.now.get())

    def push_mode_button(self):
        self.model.mode.set((self.model.mode.get()+1)%2)
        self.model.set_nows("", "", "")


app = tkinter.Tk()

app.title("らくらくトリセツ")

model = Model()
view = View(app, model)
controller = Controller(app, model, view)

app.mainloop()