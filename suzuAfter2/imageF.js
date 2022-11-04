//A4 = 2,894 x 4,093px

var canvasL = document.getElementById('canvas');
var c = canvasL.getContext('2d');
var canStamp = document.getElementById('stamp');
var cS = canStamp.getContext('2d');

// Image オブジェクトを生成
var img = new Image();
var img_S = new Image();
img.src = 'image/backWhite.png'; //解像度72
//img.src = 'image/a4_white.png'; //解像度300
img_S.src = 'image/redT.png';
let w =0;
let h = 0;

//スタンプの指先の座標
let asset_w = 113;
let asset_h = 31;

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
    concatCanvas("#canvas", "#stamp", canvasX, canvasY);
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

// async function concatCanvas(base, asset, cX, cY){
//     let baseC = document.querySelector(base);
//     let ctx = baseC.getContext("2d");
//     let base_data = ctx.getImageData(0, 0, baseC.width, baseC.height);

//     const assetC = document.querySelector(asset);
//     const ctxAS = assetC.getContext("2d");
//     let asset_data = ctxAS.getImageData(0, 0, assetC.width, assetC.height);

//     let k=0;
//     let l =0;
//     for (var y = cY;y < base_data.height;y++) {
//         for (var x = cX;x < base_data.width;x++) {

//             var index = (x + y * base_data.width) * 4;
//             var index_asset = (k + l * base_data.width) * 4;

//             base_data.data[index] = asset_data.data[index_asset];
//             base_data.data[index+1] = asset_data.data[index_asset];
//             base_data.data[index + 2] =asset_data.data[index_asset];

//             l +=1;
//         }
//         k +=1;
//     }
// }


// async function concatCanvas(base, asset, cX, cY){
//     const canvas = document.querySelector(base); //ここは変えない方が良い
//     const ctx = canvas.getContext("2d");

//     for(let i=0; i<asset.length; i++){
//         //const image1 = await getImagefromCanvas(asset[i]);
//         ctx.drawImage(img_S, cX, cY, canvas.width, canvas.height);
//     }
    
// }

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