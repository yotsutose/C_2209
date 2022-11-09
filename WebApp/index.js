const fileInput = document.getElementById('filename');
const video = document.getElementById('video');
let videoWidth, videoHeight, videoRatio;
let stateOfFrame = [];
let prewviewMode = true;
let index = 0;



// FileInputのchangeイベントで呼び出す関数
const handleFileSelect = () => {
    var URL = URL || webkitURL;
    let videofile = fileInput.files[0];
    video.src = URL.createObjectURL(videofile);
    // document.getElementById('filename').innerHTML = video.src;
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
    // モードの切り替え
    let mode = document.getElementsByClassName('mode');
    let modeChange = document.getElementsByClassName('modeChange');
    let modeChange2 = document.getElementsByClassName('modeChange2');
    [mode[0].hidden, mode[1].hidden] = [mode[1].hidden, mode[0].hidden];
    [modeChange[0].hidden, modeChange[1].hidden] = [modeChange[1].hidden, modeChange[0].hidden];
    modeChange2[0].hidden = !modeChange2[0].hidden;
}

// ページ遷移を行う
function nextPage() {
    $.scrollify.next();
}

function playV() {
    bool_stamp = true;
    video.play();
}

// フレームの選択/非選択の切り替え
function stateChange(i){
    stateOfFrame[i] = !stateOfFrame[i];
    const allDivi = document.getElementById("allDiv" + (i));
    if(prewviewMode) allDivi.hidden = true;
    const buttonElement = allDivi.childNodes[1].childNodes[0].childNodes;
    [buttonElement[0].hidden, buttonElement[1].hidden] = [buttonElement[1].hidden, buttonElement[0].hidden];
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

// <canvases>の中に<canvas>と<button>を追加する処理
function addCanvas(i, isSelected) {

    let parentnode = document.getElementsByClassName('canvases');

    // 一番外側のdiv要素
    let allDivElement = document.createElement('div');
    allDivElement.id = "allDiv" + (i);
    allDivElement.hidden = !isSelected; // 選択状態なら隠さない
    // ボタンのためのdiv
    let buttonDivElement = document.createElement('div');
    buttonDivElement.style="text-align:center";
    // ボタン
    let buttonElement = document.createElement('button');
    buttonElement.onclick = () => stateChange(i);
    buttonElement.className="buttonDiv";
    // 選択ボタン
    let checkboxElement = document.createElement('img');
    checkboxElement.src="assets/選択box.png";
    checkboxElement.hidden = !isSelected;
    // 未選択ボタン
    let noncheckboxElement = document.createElement('img');
    noncheckboxElement.src="assets/未選択box.png";
    noncheckboxElement.hidden = isSelected;

    // キャンバス
    let canvasElement = document.createElement('canvas');
    canvasElement.id = "canvas" + (i);
    canvasElement.style.width  = Math.round(videoWidth /4)+"px";
    canvasElement.style.height = Math.round(videoHeight/4)+"px";
    canvasElement.willReadFrequently = true;

    buttonElement.appendChild(checkboxElement);
    buttonElement.appendChild(noncheckboxElement);
    buttonDivElement.appendChild(buttonElement);
    allDivElement.appendChild(canvasElement);
    allDivElement.appendChild(buttonDivElement);
    parentnode[0].appendChild(allDivElement);

    return canvasElement.id;
}
