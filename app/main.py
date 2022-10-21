import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk
import cv2
import time


class Model():

    def __init__(self):

        # 動画オブジェクト参照用
        self.video = None

        # 画像処理の設定
        self.gray = False
        self.flip= False

        # 読み込んだフレーム
        self.frames = None

        # PIL画像オブジェクト参照用
        self.image = None

        # Tkinter画像オブジェクト参照用
        self.image_tk = None


    def create_video(self, path):
        '動画オブジェクトの生成を行う'

        # pathの動画から動画オブジェクト生成
        self.video = cv2.VideoCapture(path)

    def advance_frame(self):
        'フレームを読み込んで１フレーム進める'

        if not self.video:
            return

        # フレームの読み込み
        ret, self.frame = self.video.read()
        
        return ret

    def reverse_video(self):
        '動画を先頭に戻す'

        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def create_image(self, size):
        'フレームの画像を作成'

        t1 = time.time()

        # フレームを読み込み
        frame = self.frame
        if frame is None:
            print("None")

        # 設定に応じて画像処理
        if self.gray:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.flip:
            frame = cv2.flip(frame, 1)

        # PIL イメージに変換
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        
        # 指定サイズに合わせて画像をリサイズ

        # 拡大率を計算
        ratio_x = size[0] / pil_image.width
        ratio_y = size[1] / pil_image.height

        if ratio_x < ratio_y:
            ratio = ratio_x
        else:
            ratio = ratio_y

        # リサイズ
        self.image = pil_image.resize(
            (
                int(ratio * pil_image.width),
                int(ratio * pil_image.height)
            )
        )
        t2 = time.time()

        print(f"経過時間：{t2-t1}")

    def get_image(self):
        'Tkinter画像オブジェクトを取得する'

        if self.image is not None:
            # Tkinter画像オブジェクトに変換
            self.image_tk = ImageTk.PhotoImage(self.image)
        return self.image_tk

    def get_fps(self):
        '動画のFPSを取得する'

        if self.video is None:
            return None

        return self.video.get(cv2.CAP_PROP_FPS)

    def set_gray(self):
        self.gray = not self.gray

    def set_flip(self):
        self.flip = not self.flip

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
        self.operation_frame.grid(column=2, row=1)


        # キャンバスの作成と配置
        self.canvas = tkinter.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="#EEEEEE",
        )
        self.canvas.pack()

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
        self.gray_button.pack()

        # フリップ/OFFボタンの作成と配置
        self.flip_button = tkinter.Button(
            self.operation_frame,
            text="Previous Frame"
        )
        self.flip_button.pack()


    def draw_image(self):
        '画像をキャンバスに描画'

        image = self.model.get_image()

        if image is not None:
            # キャンバス上の画像の左上座標を決定
            sx = (self.canvas.winfo_width() - image.width()) // 2
            sy = (self.canvas.winfo_height() - image.height()) // 2

            # キャンバスに描画済みの画像を削除
            objs = self.canvas.find_withtag("image")
            for obj in objs:
                self.canvas.delete(obj)

            # 画像をキャンバスの真ん中に描画
            self.canvas.create_image(
                sx, sy,
                image=image,
                anchor=tkinter.NW,
                tag="image"
            )

    def select_open_file(self, file_types):
        'オープンするファイル選択画面を表示'

        # ファイル選択ダイアログを表示
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=".",
            filetypes=file_types
        )
        return file_path

    def draw_play_button(self):
        '再生ボタンを描画'

        # キャンバスのサイズ取得
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # 円の直径を決定
        if width > height:
            diameter = height
        else:
            diameter = width

        # 端からの距離を計算
        distance = diameter / 10

        # 円の線の太さを計算
        thickness = distance

        # 円の描画位置を決定
        sx = (width - diameter) // 2 + distance
        sy = (height - diameter) // 2 + distance
        ex = width - (width - diameter) // 2 - distance
        ey = height - (height - diameter) // 2 - distance

        # 丸を描画
        self.canvas.create_oval(
            sx, sy,
            ex, ey,
            outline="white",
            width=thickness,
            tag="oval"
        )

        # 頂点座標を計算
        x1 = sx + distance * 3
        y1 = sy + distance * 2
        x2 = sx + distance * 3
        y2 = ey - distance * 2
        x3 = ex - distance * 2
        y3 = height // 2

        # 三角を描画
        self.canvas.create_polygon(
            x1, y1,
            x2, y2,
            x3, y3,
            fill="white",
            tag="triangle"
        )

    def delete_play_button(self):
        self.canvas.delete("oval")
        self.canvas.delete("triangle")

class Controller():

    def __init__(self, app, model, view):
        self.master = app
        self.model = model
        self.view = view


        # 動画再生中かどうかの管理
        self.playing = False

        # フレーム進行する間隔
        self.frame_timer = 0

        # 描画する間隔
        self.draw_timer = 50

        self.set_events()

    def set_events(self):
        '受け付けるイベントを設定する'

        # キャンバス上のマウス押し下げ開始イベント受付
        self.view.canvas.bind(
            "<ButtonPress-1>",
            self.button_press
        )

        # 動画選択ボタン押し下げイベント受付
        self.view.load_button['command'] = self.push_load_button

        # モノクロON/OFFボタン押し下げイベント受付
        self.view.gray_button['command'] = self.push_gray_button

        # フリップON/OFFボタン押し下げイベント受付
        self.view.flip_button['command'] = self.push_flip_button

    def draw(self):
        '一定間隔で画像等を描画'

        # 再度タイマー設定
        self.master.after(self.draw_timer, self.draw)

        # 動画再生中の場合
        if self.playing:
            # フレームの画像を作成
            self.model.create_image(
                (
                    self.view.canvas.winfo_width(),
                    self.view.canvas.winfo_height()
                )
            )

            # 動画１フレーム分をキャンバスに描画
            self.view.draw_image()

    def frame(self):
        '一定間隔でフレームを進める'

        # 再度タイマー設定
        self.master.after(self.frame_timer, self.frame)

        # 動画再生中の場合
        if self.playing:
            # 動画を１フレーム進める
            ret = self.model.advance_frame()

            # フレームが進められない場合
            if not ret:
                # フレームを最初に戻す
                self.model.reverse_video()
                self.model.advance_frame()
            
        
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

            # 再生ボタンの表示
            self.view.delete_play_button()
            self.view.draw_play_button()

            # FPSに合わせてフレームを進める間隔を決定
            fps = self.model.get_fps()
            self.frame_timer = int(1 / fps * 1000 + 0.5)

            # フレーム進行用のタイマースタート
            self.master.after(self.frame_timer, self.frame)

            # 画像の描画用のタイマーセット
            self.master.after(self.draw_timer, self.draw)

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
        self.model.set_gray()

    def push_flip_button(self):
        self.model.set_flip()



app = tkinter.Tk()

app.title("動画再生アプリ")

model = Model()
view = View(app, model)
controller = Controller(app, model, view)

app.mainloop()