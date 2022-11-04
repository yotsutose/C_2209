const fileInput = document.getElementById('filename');
const video = document.getElementById('video');
let videoWidth, videoHeight, videoRatio;

// FileInputのchangeイベントで呼び出す関数
const handleFileSelect = () => {
    var URL = URL || webkitURL;
    let videofile = fileInput.files[0];
    video.src = URL.createObjectURL(videofile);
    document.getElementById('filename').innerHTML = video.src;
}
// ファイル選択時にhandleFileSelectを発火
fileInput.addEventListener('change', handleFileSelect);

// opencv.jsの読み込みが終わってから動く関数
function onCvLoaded() {
    console.log('cv', cv);
    cv.onRuntimeInitialized = onReady;
}

// videoの再生時に処理を行う関数達
let streaming = false;
let index = 0;

function onReady() {
    console.log('ready');
    let src;
    let diff_src;
    let pre_src;
    let cap;
    let index = 0;
    
    video.controls = true;

    // videoタグに対して、再生・ポーズ・終了などのアクションに対して発火する関数をセットしている
    video.addEventListener('play', start);
    video.addEventListener('pause', pause);
    video.addEventListener('ended', stop);

    // 動画の再生時に発火する関数
    // processvideoを最後に呼んでいる
    function start() {
        console.log('playing...');
        streaming = true;
        videoWidth  = video.videoWidth; // video本体の大きさ取得
        videoHeight = video.videoHeight;
        videoRatio = videoHeight/videoWidth;
        video.height = videoHeight; // videoElementの大きさを決める(capのため)
        video.width = videoWidth;
        video.playbackRate = 3.0;
        src      = new cv.Mat(videoHeight, videoWidth, cv.CV_8UC4);
        diff_src = new cv.Mat(videoHeight, videoWidth, cv.CV_8UC4);
        pre_src  = new cv.Mat(videoHeight, videoWidth, cv.CV_8UC4);
        cap = new cv.VideoCapture(video);
        setTimeout(processVideo, 0);
    }

    // 動画のポーズ時に発火する関数
    function pause() {
        // video.play();
        stop();
    }

    // 動画の終了時に発火する関数
    function stop() {
        console.log('paused or ended');
        streaming = false;
    }

    // 再生されている動画から画像を切り出す関数
    function processVideo() {
        if (!streaming) {
            src.delete();
            diff_src.delete();
            return; // ストリーミング=falseなら終了
        }
        
        // 今videoで流れている画像をsrcにreadする処理
        cap.read(src);
        
        // diffをとる
        cv.absdiff(pre_src, src, diff_src);
        cv.bitwise_not(diff_src, diff_src);

        // ここでdiffから類似度を計算する
        // todo

        // 選択されたフレームをキャンバスに追加
        if(index%3==0){ // 「ここを類似度がXXXなら追加する」みたいに書き換える (今の処理は30FPSだから2秒に1回くらい選択)
            canvas_id = addCanvas(index);
            cv.imshow(canvas_id, src);
            index++;
        }

        // debug用のキャンバス表示 なくても困らない
        cv.imshow('canvasOutput', diff_src);
        cv.imshow('canvasOutput2', pre_src);
        cv.imshow('canvasOutput3', src);
        
        index++;
        pre_src = src.clone();
        setTimeout(processVideo, 0);
    }
}

// 「選択された画像の一覧画面」のところに<canvas>を追加する処理
function addCanvas(index) {

    let parentnode = document.getElementsByClassName('canvases');

    let divElement = document.createElement('div');
    parentnode[0].appendChild(divElement);
    
    let canvasElement = document.createElement('canvas');
    canvasElement.id = "canvas" + (index/3);
    canvasElement.style.width  = Math.round(videoWidth /3)+"px";
    canvasElement.style.height = Math.round(videoHeight/3)+"px";
    canvasElement.willReadFrequently = true;

    let buttonElement = document.createElement('p');
    buttonElement.value = "button"
    divElement.appendChild(buttonElement);
    divElement.appendChild(canvasElement);

    return canvasElement.id;
}

// パワーポイントを作る関数
function makePPTX() {
    function Cm(n) {
    return n * 0.3937;
}
    function Pt(n) {
        return n / 72;
    }
    // 1. パワポの作成、設定
    let pptx = new PptxGenJS();
    pptx.defineLayout({ name:'A4', width:11.7, height:8.3 });
    pptx.layout = 'A4';

    // 2. スライドの追加
    let slide = pptx.addSlide();

    // 3. こんな感じでスライドにオブジェクトを追加できる
    let x = Cm(2.5);
    let y = Cm(0.5);
    let width = Cm(4.39);
    let height = Cm(9.5);
    let size = 28;
    for(let i = 0; i < index; i++) {
         // canvasに書かれたデータを読み取るコード
        cvs = document.getElementById(`canvas${i}`);
        ctx = cvs.getContext('2d');
        imagedata = cvs.toDataURL("image/jpeg");
        if (i % 8 === 0 && i !== 0){
            slide = pptx.addSlide();
            y = Cm(0.5);
        }
        //画像追加
        slide.addImage({ data: imagedata, w: width, h: height, x: x, y: y });
        //テキスト追加
        slide.addText(String(i+1), 
        {x: x-Cm(1.5),
        y: y,
        w: Pt(size*2),
        h: Pt(size),
        color: "363636",
        fontSize: size,
        //align: pptx.AlignH.center
    });
        x += Cm(7);

        if (i % 4 == 3){
            x = Cm(2.5);
            y += Cm(10);
        }
    }
    //画像を２枚ずつパワポに出力
    height = Cm(16);
    width = Cm(7.39);

    //連番で2枚ずつのスライドを作る疑似コード
    let pre_path = null;
    let path = null;
    size = 36;
    y = Cm(2.5);
    for(let i =0;i<index;i++){
        // canvasに書かれたデータを読み取るコード
        cvs = document.getElementById(`canvas${i}`);
        ctx = cvs.getContext('2d');
        imagedata = cvs.toDataURL("image/jpeg");
        path = imagedata;
        if (i==0) {
            pre_path = path
            continue
        }
        //スライドを増やす
        slide = pptx.addSlide(); 
        //pre_pathの画像を←に配置
        x = ( Cm(11.7)/2/0.3937 - width ) / 2
        slide.addImage({ data: pre_path, w: width, h: height, x: x, y: y });
        //put_text(pic_left-Cm(1.5), pic_top, str(i), 36)
        slide.addText(String(i), 
        {x: x-Cm(1.5),
        y: y,
        w:Pt(size*2),
        h:Pt(size),
        color: "363636",
        fontSize: size,
        //align: pptx.AlignH.center
    });
        pre_path = path
        //pathの画像を→に配置
        x += ((Cm(11.7)/0.3937)/2)
        slide.addImage({ data: path, w: width, h: height, x: x, y: y });
        //矢印を追加
        // ratio = 0.45
        // pic_left2 = slide_width/2 - pic_width*ratio/2
        // pic_top2 = slide_height/2 - pic_width*ratio/2
        // put_arrow(pic_left2, pic_top2, pic_width*ratio)
        //手の写真を追加
        // put_sign(SIGN_DIR, sign_names)
        //テキストを追加
        slide.addText(String(i+1), 
        {x: x-Cm(1),
        y: y,
        w:Pt(size),
        h:Pt(size),
        color: "363636",
        fontSize: size,
        align: pptx.AlignH.right
    });
        // put_text(pic_left-Cm(1.5), pic_top, str(i+1), 36)
        // pre_path = path
    }
    // 4. パワポを保存する
    pptx.writeFile({ fileName: "らくらくトリセツ.pptx" });
}

// PDFを作る関数
function makePDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({orientation: "landscape"}); // 向きを指定する

    doc.text("Hello world!", 10, 10);

    // canvasに書かれたデータを読み取るコード
    cvs = document.getElementById('canvasOutput2');
    ctx = cvs.getContext('2d');
    imagedata = cvs.toDataURL("image/jpeg");
    
    // addImage(imageData, format, x, y, width, height, alias, compression, rotation)
    // https://artskydj.github.io/jsPDF/docs/module-addImage.html
    doc.addImage(imagedata, 'JPEG', 30, 30, 80, 160);

    doc.addPage({orientation: "landscape"});

    doc.save("らくらくトリセツ.pdf");
}