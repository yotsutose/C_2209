const fileInput = document.getElementById('fileinput');
const video = document.getElementById('video');

// FileInputのchangeイベントで呼び出す関数
const handleFileSelect = () => {
    var URL = URL || webkitURL;
    let videofile = fileInput.files[0];
    video.src = URL.createObjectURL(videofile);
    // document.getElementById('filename').innerHTML = video.src;
}

// ファイル選択時にhandleFileSelectを発火
fileInput.addEventListener('change', handleFileSelect);


// opencv.jsの読み込みが終わってから動く関数
function onCvLoaded() {
  console.log('cv', cv); //debug用
  cv.onRuntimeInitialized = onReady;
}

// videoの再生時に処理を行う関数達
let streaming = true;
function onReady() {
  console.log('ready');
  // <!-- 828 x 1792 -->
  let src;
  let cap;
  video.controls = true;

  // videoタグに対して、再生・ポーズ・終了などのアクションに対して発火する関数をセットしている
  video.addEventListener('play', start);

  // 動画の再生時に発火する関数
  // processvideoを最後に呼んでいる
  function start() {
      if(!streaming) return;
      console.log('playing...');
      videoWidth  = video.videoWidth; // video本体の大きさ取得
      videoHeight = video.videoHeight;
      videoRatio = videoHeight/videoWidth;
      video.playbackRate = 4.0;
      console.log(videoHeight, videoWidth);// 828 1792

      cap = new cv.VideoCapture(video);
      setTimeout(processVideo, 0);
  }

  // 再生されている動画から画像を切り出す関数
  function processVideo() {
      if(!streaming) return;
      console.log("proces");
      for(var i = 1791;i<1800;i++){
        for(var j=800;j<850;j++){
          console.log(i,j);
          src = new cv.Mat(i, j, cv.CV_8UC4);
          try{
            cap.read(src);
          } catch(err){
            continue;
          }
          console.log("----------------");
          console.log(src.rows, src.cols);
        }
      }
      console.log("proces");

      console.log(src.rows, src.cols);
      // setTimeout(processVideo, 10);
  }
}
