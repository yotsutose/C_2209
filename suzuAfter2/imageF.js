//A4 = 2,894 x 4,093px

var canvasL = document.getElementById('canvas');
var c = canvasL.getContext('2d');
// var canStamp = document.getElementById('stamp');
// var cS = canStamp.getContext('2d');

// Image オブジェクトを生成
var img = new Image();
var img_S = new Image();
img.src = 'image/backWhite.png'; //解像度72
//img.src = 'image/a4_white.png'; //解像度300
let images = [];
let srcs = [
    'image/stm/redT1.png',
    'image/stm/redT2.png',
    'image/stm/redT3.png',
    'image/stm/redT4.png',
    'image/stm/redT5.png',
    'image/stm/redT6.png',
];

//押すスタンプのid
let stamp_id_S = "stamp1";

//スタンプ画像の読み込み
for(let i=0; i<srcs.length;i++){
    images[i] = new Image();
    images[i].src = srcs[i];

    images[i].onload = function(){

        console.log('dddd');
        let stamp_id = addCanvas(i+1);
        console.log(stamp_id);
        let stamp_C = document.getElementById(stamp_id);
        let ctS = stamp_C.getContext('2d');

        let ws = images[i].width;
        let hs = images[i].height;
        console.log('ws'+ws);
        console.log('hs'+hs);

        stamp_C.width = ws/2;
        stamp_C.height = hs/2;
        images[i].width /= 2;
        images[i].height /= 2;
        console.log('w__'+images[i].width);
        console.log('h__'+hs);
        ctS.drawImage(images[i], 0, 0, ws/2, hs/2);

        stamp_C.addEventListener("click", point=>{
            console.log(stamp_id);
            stamp_id_S = stamp_id;

            const rect = point.target.getBoundingClientRect();
    
            // ブラウザ上での座標を求める
            const   viewX = point.clientX - rect.left,
                    viewY = point.clientY - rect.top;
    
            // 表示サイズとキャンバスの実サイズの比率を求める
            const   scaleWidth =  canvasL.clientWidth / canvasL.width,
                    scaleHeight =  canvasL.clientHeight / canvasL.height;
    
            // ブラウザ上でのクリック座標をキャンバス上に変換
            const   canvasX = Math.floor( viewX / scaleWidth ),
                    canvasY = Math.floor( viewY / scaleHeight );
    
            console.log( canvasX,canvasY );
        });
    }
}

// img_S.src = 'image/redT.png';
let w =0;
let h = 0;
let stamp_siv_width = 200;
let stamp_siv_height = 150;

//スタンプの指先の座標
let asset_w = 132;
let asset_h = 52;

// 画像読み込み終了してから描画
img.onload = function(){
    w = img.width;
    h = img.height;
    console.log(w);
    console.log(h);
    canvasL.width = w;
    canvasL.height = h;
    c.drawImage(img, 0, 0, w, h);
}

img_S.onload = function(){
    let ws = img_S.width;
    let hs = img_S.height;
    console.log('ws'+ws);
    console.log('hs'+hs);

    canStamp.width = ws/2;
    canStamp.height = hs/2;
    img_S.width /= 2;
    img_S.height /= 2;
    console.log('w__'+img_S.width);
    console.log('h__'+hs);
    cS.drawImage(img_S, 0, 0, ws/2, hs/2);
}

canvasL.addEventListener("click", point=>{
    const rect = point.target.getBoundingClientRect();

    // ブラウザ上での座標を求める
    const   viewX = point.clientX - rect.left,
            viewY = point.clientY - rect.top;

    // 表示サイズとキャンバスの実サイズの比率を求める
    const   scaleWidth =  canvasL.clientWidth / canvasL.width,
            scaleHeight =  canvasL.clientHeight / canvasL.height;

    // ブラウザ上でのクリック座標をキャンバス上に変換
    const   canvasX = Math.floor( viewX / scaleWidth ),
            canvasY = Math.floor( viewY / scaleHeight );

    console.log( canvasX,canvasY );
    
    c.drawImage(img, 0, 0, w, h); //リセット
    let asset_id = '#'+stamp_id_S;
    concatCanvas("#canvas", asset_id, canvasX, canvasY);
    //concatCanvas("#canvas", "#stamp");
});


canStamp.addEventListener("click", point=>{
    const rect = point.target.getBoundingClientRect();

    // ブラウザ上での座標を求める
    const   viewX = point.clientX - rect.left,
            viewY = point.clientY - rect.top;

    // 表示サイズとキャンバスの実サイズの比率を求める
    const   scaleWidth =  canvasL.clientWidth / canvasL.width,
            scaleHeight =  canvasL.clientHeight / canvasL.height;

    // ブラウザ上でのクリック座標をキャンバス上に変換
    const   canvasX = Math.floor( viewX / scaleWidth ),
            canvasY = Math.floor( viewY / scaleHeight );

    console.log( canvasX,canvasY );
});

async function concatCanvas(base, asset, cX, cY){
    const canvas = document.querySelector(base); //ここは変えない方が良い
    const ctx = canvas.getContext("2d");

    const image1 = await getImagefromCanvas(asset);
    ctx.drawImage(image1, cX-(asset_w), cY-(asset_h), image1.width, image1.height);

}

function getImagefromCanvas(id){
    return new Promise((resolve, reject) => {
        const image = new Image();
        const ctx = document.querySelector(id).getContext("2d");
        image.onload = () => resolve(image);
        image.onerror = (e) => reject(e);
        image.src = ctx.canvas.toDataURL();
    });
}

function reset(){
    console.log('reset');
    c.drawImage(img, 0, 0, w, h); //リセット
}


// 「選択された画像の一覧画面」のところに<canvas>を追加する処理
function addCanvas(index) {

    let parentnode = document.getElementsByClassName('stamps');

    let divElement = document.createElement('div');
    parentnode[0].appendChild(divElement);
    
    let canvasElement = document.createElement('canvas');
    canvasElement.id = "stamp" + (index);
    canvasElement.style.width  = stamp_siv_width+"px";
    canvasElement.style.height = stamp_siv_height+"px";
    canvasElement.style.border = "1px solid";
    //canvasElement.style.float = "left";
    canvasElement.willReadFrequently = true;

    divElement.appendChild(canvasElement);

    return canvasElement.id;
}