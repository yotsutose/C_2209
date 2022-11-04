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
let img_num = 0;

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
            img_num += 1;
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
    canvasElement.id = "canvas" + (index/3);       // 値が整数になるように、とりあえず調節 60を３に
    canvasElement.style.width  = Math.round(videoWidth /3)+"px";
    canvasElement.style.height = Math.round(videoHeight/3)+"px";
    // canvasElement.style.border = "4px solid"    // pdfに枠線が付くか確認
    canvasElement.willReadFrequently = true;

    let buttonElement = document.createElement('p');
    buttonElement.value = "button"
    divElement.appendChild(buttonElement);
    divElement.appendChild(canvasElement);

    return canvasElement.id;
}

// パワーポイントを作る関数
function makePPTX() {
    // 1. パワポの作成、設定
    let pptx = new PptxGenJS();
    pptx.defineLayout({ name:'A4', width:11.7, height:8.3 });
    pptx.layout = 'A4';

    // 2. スライドの追加
    let slide = pptx.addSlide();

    // 3. こんな感じでスライドにオブジェクトを追加できる
    slide.addText("Hello World from PptxGenJS...", {
        x: 1.5,
        y: 1.5,
        color: "363636",
        fill: { color: "F1F1F1" },
        align: pptx.AlignH.center,
    });

    // canvasに書かれたデータを読み取るコード
    cvs = document.getElementById('canvasOutput2');
    ctx = cvs.getContext('2d');
    imagedata = cvs.toDataURL("image/jpeg");
    // 3, 画像データをパワポに追加するメソッドを使う
    slide.addImage({ data: imagedata, w: 2, h: 4, x: 2, y: 1 });

    // 4. パワポを保存する
    pptx.writeFile({ fileName: "らくらくトリセツ.pptx" });
}

// PDFを作る関数
function makePDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({orientation: "landscape"}); // 向きを指定する

    // doc.text("Hello world!", 10, 10);

    // １枚目の初期位置
    let x = 25;
    let y = 5;
    let width = 43.9;
    let height = 95;
    let size = 27;

    // canvasに書かれたデータを読み取るコード
    for(let i=0; i<img_num; i++) {
        cvs = document.getElementById(`canvas${i}`);
        ctx = cvs.getContext('2d');
        imagedata = cvs.toDataURL("image/jpeg");
        
        if (i % 8 === 0 && i !== 0){
            // ページを増やす
            doc.addPage({orientation: "landscape"});
            y = 5;
        }

        doc.addImage(imagedata, 'JPEG', x, y, width, height);

        // 画像番号の追加
        doc.setFontSize(size);
        doc.text(String(i+1), x-13, y+10);

        if (i % 4 === 3){
            x = 25;
            y += 100;
        } else {
            x += 70;
        }
    }

    // 画像を２枚ずつ連番で出力
    height = 160;
    width = 73.9;

    let pre_path = null;
    let path = null;
    size = 35;
    y = 25;

    for(let i =0; i<img_num; i++) {
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
        doc.addPage({orientation: "landscape"});
        //pre_pathの画像を←に配置
        x = ( 297/2 - width ) / 2;
        doc.addImage(imagedata, 'JPEG', x, y, width, height);
        doc.text(String(i), x-15, y+10);
        pre_path = path
        //pathの画像を→に配置
        x += 297/2
        doc.addImage(imagedata, 'JPEG', x, y, width, height);

        //テキストを追加
        // 画像番号の追加
        doc.setFontSize(size);
        doc.text(String(i+1), x-15, y+10);
    }

    
    // doc.addImage('images/arrow_big.jpg', 'JPEG', 100, 100, 80, 160);

    // cvs = document.getElementById('canvasOutput2');
    // ctx = cvs.getContext('2d');
    // imagedata = cvs.toDataURL("image/jpeg");
    
    // addImage(imageData, format, x, y, width, height, alias, compression, rotation)
    // https://artskydj.github.io/jsPDF/docs/module-addImage.html
    // doc.addImage(imagedata, 'JPEG', 30, 30, 80, 160);


    doc.save("らくらくトリセツ.pdf");
}