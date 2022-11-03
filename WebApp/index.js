const fileInput = document.getElementById('filename');
const video = document.getElementById('video');
let videoWidth, videoHeight, videoRatio;
let stateOfFrame = [];
let prewviewMode = true;


// FileInputのchangeイベントで呼び出す関数
const handleFileSelect = () => {
    var URL = URL || webkitURL;
    let videofile = fileInput.files[0];
    video.src = URL.createObjectURL(videofile);
    // document.getElementById('filename').innerHTML = video.src;
    $.scrollify.next();
}

// ファイル選択時にhandleFileSelectを発火
fileInput.addEventListener('change', handleFileSelect);

// 編集モードとプレビューモードの切り替え
function modeChange() {
    prewviewMode = !prewviewMode;
    for(var i = 0;i < stateOfFrame.length; i++){
        if(prewviewMode){ // プレビューに変わったので
            if(stateOfFrame[i]) document.getElementById("allDiv" + (i)).hidden = false;
            else document.getElementById("allDiv" + (i)).hidden = true;
        }
        else{ // 編集モードに入ったので全てを表示
            document.getElementById("allDiv" + (i)).hidden = false;
        }
    }
}

// フレームの選択/非選択の切り替え
function stateChange(i){
    stateOfFrame[i] = !stateOfFrame[i];
    const allDivi = document.getElementById("allDiv" + (i));
    if(prewviewMode) allDivi.hidden = true;
    allDivi.style.backgroundColor = stateOfFrame[i]? '#00FF00': '#FF0000';
}

// opencv.jsの読み込みが終わってから動く関数
function onCvLoaded() {
    console.log('cv', cv); //debug用
    cv.onRuntimeInitialized = onReady;
}

// videoの再生時に処理を行う関数達
let streaming = true;
function onReady() {
    console.log('ready');
    let src, diff_src, pre_src;
    let cap;
    let pre_img_is_similar = false;
    let index = 0;
    const rate_similer = 0.95;
    
    video.controls = true;

    // videoタグに対して、再生・ポーズ・終了などのアクションに対して発火する関数をセットしている
    video.addEventListener('play', start);
    video.addEventListener('pause', pause);
    video.addEventListener('ended', stop);

    // 動画の再生時に発火する関数
    // processvideoを最後に呼んでいる
    function start() {
        if(!streaming) return;
        console.log('playing...');
        videoWidth  = video.videoWidth; // video本体の大きさ取得
        videoHeight = video.videoHeight;
        videoRatio = videoHeight/videoWidth;
        video.height = videoHeight; // videoElementの大きさを決める(capのため)
        video.width = videoWidth;
        video.playbackRate = 4.0;
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
        if(!streaming) return;
        
        // 今videoで流れている画像をsrcにreadする処理
        // アイデア:ここの処理をsrc1とsrc2に交互に読み込めばコピーが起こらない
        cap.read(src);
        
        // diffをとる
        cv.absdiff(pre_src, src, diff_src);
        cv.bitwise_not(diff_src, diff_src);
        cv.cvtColor(diff_src, diff_src, cv.COLOR_RGBA2GRAY, 0);

        let channels = diff_src.channels(); //要素の次元
        let count = 0;
        let Lcount = 0;
        for (let y = 0; y < diff_src.rows; y+=10) {
            for (let x = 0; x < diff_src.cols; x+=10) {
                for (let c = 0; c < channels; ++c) {
                    if(diff_src.ucharPtr(y, x)[c] > 240){
                        count+=1;
                    }
                    Lcount+=1;
                }
            }
        }
        let similler = count/Lcount;
        if(similler < rate_similer && pre_img_is_similar){ // アニメーション始まり
            canvas_id = addCanvas(index, true);
            cv.imshow(canvas_id, pre_src);
            stateOfFrame.push(true);
            index++;
            pre_img_is_similar = false;
        }else if(similler >= rate_similer && !pre_img_is_similar){ // アニメーション終わり
            canvas_id = addCanvas(index, false);
            cv.imshow(canvas_id, src);
            stateOfFrame.push(false);
            index++;
            pre_img_is_similar = true;
        }
        
        pre_src = src.clone(); // 30フレームx10秒くらいやると落ちる, 6フレームx50秒くらいまで耐えられる
        setTimeout(processVideo, 0);
    }
}

// 「選択された画像の一覧画面」のところに<canvas>を追加する処理
function addCanvas(i, isSelected) {
    // <div>
    //   <div><button></button></div>
    //   <canvas></canvas>
    // <div>

    let parentnode = document.getElementsByClassName('canvases');

    // 一番外側のdiv要素
    let allDivElement = document.createElement('div');
    allDivElement.id = "allDiv" + (i);
    allDivElement.hidden = !isSelected; // 選択状態なら隠さない
    allDivElement.style.backgroundColor = isSelected? '#00FF00': '#FF0000';
    // ボタンのためのdiv
    let buttonDivElement = document.createElement('div');
    // ボタン
    let buttonElement = document.createElement('button');
    buttonElement.textContent = "選択/非選択"
    buttonElement.onclick = () => stateChange(i);
    // キャンバス
    let canvasElement = document.createElement('canvas');
    canvasElement.id = "canvas" + (i);
    canvasElement.style.width  = Math.round(videoWidth /4)+"px";
    canvasElement.style.height = Math.round(videoHeight/4)+"px";
    canvasElement.willReadFrequently = true;

    buttonDivElement.appendChild(buttonElement);
    allDivElement.appendChild(buttonDivElement);
    allDivElement.appendChild(canvasElement);
    parentnode[0].appendChild(allDivElement);

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