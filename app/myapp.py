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
            if i % 20 != 0:
                continue
            rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            # widthとheightは画像とcanvasのサイズ見て考える
            # 元の画像は800x1800くらい
            pil_image = pil_image.resize((width//4, height//4), resample=3)
            self.frames.append(ImageTk.PhotoImage(pil_image))
        self.frame_state = []
        for x in range(len(self.frames)):
            self.frame_state.append(tkinter.IntVar())
        for x in range(4):
            self.frame_state[x].set(1)
        # セットする
        self.now.set(2)

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

        # メインフレーム(編集とプレビュー画面)
        self.main_frame = tkinter.Frame(
            self.master,
            bg="#FCFFEE"
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.create_main_frame()

        # ホームフレーム(ホーム画面)
        self.home_frame = tkinter.Frame(
            self.master,
            bg="#FCFFEE"
        )
        self.home_frame.grid(row=0, column=0, sticky="nsew")
        self.home_frame.grid_rowconfigure(0, weight=4)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.create_home_frame()

        # エンドフレーム(終了画面)
        self.end_frame = tkinter.Frame(
            self.master,
            bg="#FCFFEE"
        )
        self.end_frame.grid(row=0, column=0, sticky="nsew")
        self.end_frame.grid_rowconfigure(0, weight=1)
        self.end_frame.grid_columnconfigure(0, weight=1)
        self.create_end_frame()

        # tkraise()
        self.home_frame.tkraise()
        # self.main_frame.tkraise()
        # self.end_frame.tkraise()


    def create_main_frame(self):
        # 画像の読み込み
        edit_top_image_ = Image.open('./app/image/編集モード.png')
        self.edit_top_image = ImageTk.PhotoImage(edit_top_image_)

        preview_top_image_ = Image.open('./app/image/プレビューモード.png')
        self.preview_top_image = ImageTk.PhotoImage(preview_top_image_)

        add_button_image_ = Image.open('./app/image/未選択_四角.png')
        self.add_button_image = ImageTk.PhotoImage(add_button_image_)

        delete_button_image_ = Image.open('./app/image/選択_四角.png')
        self.delete_button_image = ImageTk.PhotoImage(delete_button_image_)

        next_frame_button_image_ = Image.open('./app/image/次へ.png')
        self.next_frame_button_image = ImageTk.PhotoImage(next_frame_button_image_)
        
        prev_frame_button_image_ = Image.open('./app/image/前へ.png')
        self.prev_frame_button_image = ImageTk.PhotoImage(prev_frame_button_image_)
        
        mode_button_image_ = Image.open('./app/image/編集.png')
        mode_button_image = ImageTk.PhotoImage(mode_button_image_)
        
        mode_button_image2_ = Image.open('./app/image/完了ボタン.png')
        mode_button_image2 = ImageTk.PhotoImage(mode_button_image2_)

        to_home_button_image_ = Image.open('./app/image/ホームへ.png')
        self.to_home_button_image = ImageTk.PhotoImage(to_home_button_image_)

        making_pptx_button_image_ = Image.open('./app/image/実行ボタン.png')
        self.making_pptx_button_image = ImageTk.PhotoImage(making_pptx_button_image_)

        # 編集モード/プレビューモードのフレーム
        self.head_canvas = tkinter.Canvas(
            self.main_frame,
            height=150,
            width=500,
            highlightbackground='#FCFFEE',
            bg="#FCFFEE"
        )
        self.head_canvas.create_image(
            30, 30,
            image=self.preview_top_image,
            anchor=tkinter.NW,
            tag="image",
        )
        self.head_canvas.grid(column=1, row=1)

        # キャンバス7枚のフレーム
        self.canvas_frame = tkinter.Frame(
            self.main_frame,
            bg="#FCFFEE"
        )
        self.canvas_frame.grid(column=1, row=2)

        # オペレーションフレーム
        self.operation_frame = tkinter.Frame(
            self.main_frame,
            bg="#FCFFEE"
        )
        self.operation_frame.grid(column=1, row=3)

        # フッターのフレーム
        self.foot_frame = tkinter.Frame(
            self.main_frame,
            height=20,
            width=700,
            bg="#FCFFEE"
        )
        self.foot_frame.grid(column=1, row=4)

        # パネルごとのフレーム in canvas_panels
        self.canvas_paneles = [tkinter.Frame(
            self.canvas_frame,
            bg="#FCFFEE",) for x in range(7)]
        [self.canvas_paneles[x].grid(column=x, row=1) for x in range(7)]

        # フレーム番号表示 in canvas_panels
        self.frame_index = [tkinter.Label(
            self.canvas_paneles[x],
            bg="#FCFFEE",
            font=("MSゴシック", "30", "bold"),
            textvariable=self.model.nows[x]) for x in range(7)]
        [self.frame_index[x].grid(row=0, column=0, sticky="nsew") for x in range(7)]

        # フレーム表示 in canvas_panels
        self.frame = [tkinter.Canvas(
            self.canvas_paneles[x],
            width=200, # ここは要調整
            height=450,
            highlightbackground='#FCFFEE',
            bg='#FCFFEE'
            ) for x in range(7)]
        [self.frame[x].grid(row=1, column=0, sticky="nsew") for x in range(7)]

        # ボタンのためのフレーム
        self.button_frame = [tkinter.Frame(
            self.canvas_paneles[x],
            highlightbackground='#FCFFEE',
            bg='#FCFFEE'
            ) for x in range(7)]
        [self.button_frame[x].grid_rowconfigure(0, weight=1) for x in range(7)]
        [self.button_frame[x].grid_columnconfigure(0, weight=1) for x in range(7)]
        [self.button_frame[x].grid(row=2, column=0, sticky="nsew") for x in range(7)]

        # 追加ボタン表示
        self.state_button = [tkinter.Button(
            self.button_frame[x],
            image = self.add_button_image,
            ) for x in range(7)]
        [self.state_button[x].grid(row=0, column=0) for x in range(7)]

        # 削除ボタン表示
        self.state_button2 = [tkinter.Button(
            self.button_frame[x],
            image = self.delete_button_image,
            ) for x in range(7)]
        [self.state_button2[x].grid(row=0, column=0) for x in range(7)]

        [self.state_button[x].tkraise() for x in range(7)]

        # シークバーの表示
        style = ttk.Style()
        style.configure(
            "Horizontal.TScale",
        )
        self.scale_bar = ttk.Scale(
            self.operation_frame,
            style="TScale",
            variable=self.model.now,
            orient="horizontal",
            length=500,
            from_=0,
            to=len(self.model.frames)-1,
            # command=lambda e: self.draw_image()
        )
        self.scale_bar.pack(pady=25)

        # pptx実行ボタン
        self.making_pptx_button = tkinter.Button(
            self.operation_frame,
            image = self.making_pptx_button_image,
        )
        self.making_pptx_button.pack(fill = 'x', padx=20, side = 'right')

        # ホームへのボタン
        self.to_home_button = tkinter.Button(
            self.operation_frame,
            image = self.to_home_button_image,
        )
        self.to_home_button.pack(fill = 'x', padx=20, side = 'left')

        # next_frameへのボタン
        self.next_frame_button = tkinter.Button(
            self.operation_frame,
            image = self.next_frame_button_image,
        )
        self.next_frame_button.pack(fill = 'x', padx=20, side = 'right')

        # prev_frameへのボタン
        self.prev_frame_button = tkinter.Button(
            self.operation_frame,
            image = self.prev_frame_button_image,
        )
        self.prev_frame_button.pack(fill = 'x', padx=20, side = 'left')

        # modeチェンジのためのフレーム
        self.mode_change_frame = tkinter.Frame(
            self.operation_frame,
            highlightbackground='#FCFFEE',
            bg='#FCFFEE')
        self.mode_change_frame.grid_rowconfigure(0, weight=1)
        self.mode_change_frame.grid_columnconfigure(0, weight=1)
        self.mode_change_frame.pack()

        # プレビューから編集モードに行くための編集ボタン
        self.mode_button = tkinter.Button(
            self.mode_change_frame,
            image=mode_button_image,
            bg='#FCFFEE',
            highlightbackground='#FCFFEE'
        )
        self.mode_button.image = mode_button_image
        self.mode_button.grid(row=0, column=0, sticky="nsew")
        

        # 編集モードからプレビューに行くための完了ボタン
        self.mode_button2 = tkinter.Button(
            self.mode_change_frame,
            image=mode_button_image2,
            bg='#FCFFEE',
            highlightbackground='#FCFFEE'
        )
        self.mode_button2.image = mode_button_image2
        self.mode_button2.grid(row=0, column=0, sticky="nsew")
        self.mode_button.tkraise()
        return
    
    def create_home_frame(self):
        # 画像の読み込み
        title_logo_image_ = Image.open('./app/image/bigtitle.png')
        self.title_logo_image = ImageTk.PhotoImage(title_logo_image_)

        input_button_image_ = Image.open('./app/image/動画選択.png')
        self.input_button_image = ImageTk.PhotoImage(input_button_image_)

        using_button_image_ = Image.open('./app/image/使い方.png')
        self.using_button_image = ImageTk.PhotoImage(using_button_image_)

        done_button_image_ = Image.open('./app/image/実行ボタン.png')
        self.done_button_image = ImageTk.PhotoImage(done_button_image_)

        # 下の余白のためのフレーム
        self.home_head_frame = tkinter.Frame(
            self.home_frame,
            height=50,
            width=500,
            bg="#FCFFEE"
        )
        self.home_head_frame.grid(column=0, row=0)

        # タイトルロゴを配置するフレーム
        self.home_title_canvas = tkinter.Canvas(
            self.home_frame,
            height=280,
            width=850,
            highlightbackground='#FCFFEE',
            bg="#FCFFEE"
        )
        self.home_title_canvas.create_image(
            30, 80,
            image=self.title_logo_image,
            anchor=tkinter.NW,
            tag="image",
        )
        self.home_title_canvas.grid(column=0, row=1, pady=10)

        # ファイル読み込みを配置するフレーム
        self.home_input_frame = tkinter.Frame(
            self.home_frame,
            height=200,
            width=500,
            highlightbackground='#FCFFEE',
            bg="#FCFFEE"
        )
        self.home_input_frame.grid(column=0, row=2, pady=10)

        # ユーザ操作用フレームの作成と配置
        self.home_operation_frame = tkinter.Frame(
            self.home_frame,
            height=150,
            width=500,
            bg="#FCFFEE"
        )
        self.home_operation_frame.grid(column=0, row=3, pady=10)

        # 下の余白のためのフレーム
        self.home_foot_frame = tkinter.Frame(
            self.home_frame,
            height=150,
            width=500,
            bg="#FCFFEE"
        )
        self.home_foot_frame.grid(column=0, row=4)

        # ファイル読み込みの作成と配置
        self.input_button = tkinter.Button(
            self.home_input_frame,
            image = self.input_button_image,
            highlightbackground='#FCFFEE'
        )
        self.input_button.pack()

        # 使い方の作成と配置
        self.using_button = tkinter.Button(
            self.home_operation_frame,
            image = self.using_button_image,
            highlightbackground='#FCFFEE'
        )
        self.using_button.pack(fill = 'x', padx=25, side = 'left')

        # 実行の作成と配置
        self.done_button = tkinter.Button(
            self.home_operation_frame,
            image = self.done_button_image,
            highlightbackground='#FCFFEE'
        )
        self.done_button.pack(fill = 'x', padx=25, side = 'right')
        return

    def create_end_frame(self):
        # 画像の読み込み
        complete_image_ = Image.open('./app/image/完了.png')
        self.complete_image = ImageTk.PhotoImage(complete_image_)

        # キャンバスの配置
        self.complete_canvas = tkinter.Canvas(
            self.end_frame,
            height=500,
            width=700,
            highlightbackground='#FCFFEE',
            bg="#FCFFEE"
        )
        self.complete_canvas.create_image(
            30, 30,
            image=self.complete_image,
            anchor=tkinter.NW,
            tag="image",
        )
        self.complete_canvas.grid(column=0, row=0)
        # 画像の配置


        return

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
        self.model.mode.set(0)
        self.model.now.set(2)


    def set_events(self):
        '受け付けるイベントを設定する'

        # 動画選択ボタン押し下げイベント受付
        self.view.input_button['command'] = self.push_load_button

        # モノクロON/OFFボタン押し下げイベント受付
        self.view.next_frame_button['command'] = self.push_next_frame_button

        # フリップON/OFFボタン押し下げイベント受付
        self.view.prev_frame_button['command'] = self.push_prev_frame_button

        # 編集とプレビューの切り替えイベント受付
        self.view.mode_button['command'] = self.push_mode_button
        self.view.mode_button2['command'] = self.push_mode_button

        for x in range(7):
            self.view.state_button[x]['command'] = self.make_push_state_button(x)    
        
        for x in range(7):
            self.view.state_button2[x]['command'] = self.make_push_state_button(x)    

        # ホームからプレビューへの画面遷移
        self.view.done_button['command'] = self.push_done_button

        # プレビューからホームへの画面遷移
        self.view.to_home_button['command'] = self.push_to_home_button

        # プレビューからエンドへの画面遷移
        self.view.making_pptx_button['command'] = self.push_making_pptx_button

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

    def push_next_frame_button(self):
        self.model.next_frame()

    def push_prev_frame_button(self):
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
        if self.model.mode.get() == 0: # プレビュー
            self.view.head_canvas.delete('all')
            self.view.head_canvas.create_image(
                30, 30,
                image=self.view.preview_top_image,
                anchor=tkinter.NW,
                tag="image",
            )
            self.view.mode_button.tkraise()
        else: # 編集モード
            self.view.head_canvas.delete('all')
            self.view.head_canvas.create_image(
                30, 31,
                image=self.view.edit_top_image,
                anchor=tkinter.NW,
                tag="image",
            )
            self.view.mode_button2.tkraise()

        # ここに編集モードとプレビューモードのviewの変更をかく
        self.model.set_nows("", "", "")

    def push_done_button(self):
        self.view.main_frame.tkraise()

    def push_to_home_button(self):
        self.view.home_frame.tkraise()

    def push_making_pptx_button(self):
        self.view.end_frame.tkraise()
        self.making_pptx()

    def making_pptx(self):
        print("今からパワポを作ります")
        # ここにパワポを作る操作をかく
        # 画像　　 self.model.frames = []
        # 選択状況 self.model.frame_state = []
        
        ## 保存を行う処理

        ## pptxを保存する処理


        return

app = tkinter.Tk()

app.title("らくらくトリセツ")

model = Model()
view = View(app, model)
controller = Controller(app, model, view)

app.mainloop()