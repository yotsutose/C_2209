const fileInput = document.getElementById('filename');
const video = document.getElementById('video');
let videoWidth, videoHeight, videoRatio;

// FileInputのchangeイベントで呼び出す関数
const handleFileSelect = () => {
    var URL = URL || webkitURL;
    let videofile = fileInput.files[0];
    video.src = URL.createObjectURL(videofile);
    // //!! いらない
    // //console.log(document.getElementById('filename').innerHTML);
    // document.getElementById('suzu_test1').innerHTML ='LL'+ document.getElementById('filename').innerHTML;
    // document.getElementById('filename').innerHTML = video.src;
    // //検証テスト!!
    // //console.log(document.getElementById('filename').innerHTML);
    // //document.getElementById('suzu_test2').innerHTML = video.src;
    // document.getElementById('suzu_test2').innerHTML = 'LL'+ document.getElementById('filename').innerHTML;
}
// ファイル選択時にhandleFileSelectを発火
fileInput.addEventListener('change', handleFileSelect);

// opencv.jsの読み込みが終わってから動く関数
function onCvLoaded() {
    console.log('cv', cv); //debug用
    cv.onRuntimeInitialized = onReady;
}

// videoの再生時に処理を行う関数達
let streaming = false;
function onReady() {
    console.log('ready');
    let src;
    let diff_src;
    let pre_src;
    let cap;
    let index = 0;
    let pre_img_is_similar = false;
    let rate_similer = 0.92;
    
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
            pre_src.delete();
            return; // ストリーミング=falseなら終了
        }
        
        // 今videoで流れている画像をsrcにreadする処理
        cap.read(src);
        
        // diffをとる
        cv.absdiff(pre_src, src, diff_src);
        cv.bitwise_not(diff_src, diff_src);

        cv.cvtColor(diff_src, diff_src, cv.COLOR_RGBA2GRAY, 0);

        // ここでdiffから類似度を計算する
        // todo
        let channels = diff_src.channels(); //要素の次元
        let sum = 0;
        let count = 0;
        let Lcount = 0;
        for (let y = 0; y < diff_src.rows; y+=10) {
            for (let x = 0; x < diff_src.cols; x+=10) {
                for (let c = 0; c < channels; ++c) {
                    sum += diff_src.ucharPtr(y, x)[c];
                    if(diff_src.ucharPtr(y, x)[c] > 240){
                        count+=1;
                    }
                    Lcount+=1;
                }
            }
        }
        //console.log(`sum = ${sum}`);
        let similler = count/Lcount;
        //console.log(`count = ${count}`);
        console.log(`similler = ${similler}`);
        //console.log(`Lcount = ${Lcount}`);
        
        if(similler < rate_similer && pre_img_is_similar){ // 「ここを類似度がXXXなら追加する」みたいに書き換える (今の処理は30FPSだから2秒に1回くらい選択)
            //console.log('e : '+pre_img_is_similar);
            canvas_id = addCanvas(index);
            console.log(canvas_id);
            // cv.imshow(canvas_id, src);
            cv.imshow(canvas_id, pre_src);
            pre_img_is_similar = false;
            //console.log('s : '+pre_img_is_similar);
        }else if(similler >= rate_similer && !pre_img_is_similar){
            //console.log('e : '+pre_img_is_similar);
            pre_img_is_similar = true;
            //console.log('s : '+pre_img_is_similar);
        }

        // debug用のキャンバス表示 なくても困らない
        cv.imshow('canvasOutput', diff_src);
        cv.imshow('canvasOutput2', pre_src);
        cv.imshow('canvasOutput3', src);
        
        index++;
        pre_src = src.clone();
        setTimeout(processVideo, 0);
        // setTimeout(function () {
        //     processVideo();
        // }, 0);
    }
}

// 「選択された画像の一覧画面」のところに<canvas>を追加する処理
function addCanvas(index) {

    let parentnode = document.getElementsByClassName('canvases');

    let divElement = document.createElement('div');
    parentnode[0].appendChild(divElement);
    
    let canvasElement = document.createElement('canvas');
    canvasElement.id = "canvas" + index;
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

let cvslist = [];
function movePage(){
    console.log('move page');
    let canvas_class = document.getElementsByClassName("canvases");
    let canvas_list = canvas_class[0].getElementsByTagName("canvas");
    var myArray = Array.prototype.slice.call(canvas_list);
    console.log(myArray);
    // let index = 0;
    // for(const canV in myArray){
    //     console.log(canV);
    //     cvslist[index] = canV;
    //     index +=1;
    // }
    for(let i=0; i<myArray.length; i++){
        myArray[i] = myArray[i].getContext('2d');
    }
    cvslist = myArray;
    console.log(cvslist);

    if (window.sessionStorage) { 
        // 使用できる 
        console.log("333");
        sessionStorage["canvasList"] = cvslist;
    }
    else{ 
        // 使用できない 
    }

    window.location.replace('index.html');
}