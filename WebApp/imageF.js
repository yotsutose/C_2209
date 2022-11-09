//A4 = 2,894 x 4,093px

var canvasL = document.getElementById('canvasBack');
var c = canvasL.getContext('2d');
let canvases_L = document.getElementsByClassName("canvases_List");

//押したスタンプの座標
let relatestamps = [];
let stamp_idSave = [];

// Image オブジェクトを生成
var img = new Image();
let images = [];
let srcs = [
    'assets/stamps/stamp1.png',
    'assets/stamps/stamp2.png',
    'assets/stamps/stamp3.png',
    'assets/stamps/stamp4.png',
    'assets/stamps/stamp5.png',
    'assets/stamps/stamp6.png',
];

//押すスタンプのid
let stamp_id_S = "stamp1";
//スタンプの大きさ
let stamp_siv_width = 200;
let stamp_siv_height = 150;

//台紙画像のサイズ変数
let w =0;
let h = 0;

//スタンプの指先の座標
let asset_w = stamp_siv_width/2;
let asset_h = stamp_siv_height/2;


window.onload = ()=>{
    console.log("windowload!");

    let loadcount = 0;
    //スタンプ画像の読み込み
    for(let i=0; i<srcs.length;i++){
        images[i] = new Image();
        images[i].src = srcs[i];

        images[i].onload = function(){
            loadcount +=1;
            let stamp_id = addCanvas_Re('stamps', "stampdiv", "stamp", i+1, stamp_siv_width/2, stamp_siv_height/2, "stampClass");
            let stamp_C = document.getElementById(stamp_id);
            let ctS = stamp_C.getContext('2d');

            let ws = images[i].width;
            let hs = images[i].height;

            stamp_C.width = ws/2;
            stamp_C.height = hs/2;
            images[i].width /= 2;
            images[i].height /= 2;
            ctS.drawImage(images[i], 0, 0, ws/2, hs/2);

            stamp_C.addEventListener("click", point=>{
                console.log(stamp_id);
                let pre_stamp_id = stamp_id_S;
                stamp_id_S = stamp_id;

                //使用するスタンプの強調
                let preStamp = document.getElementById(pre_stamp_id);
                let currentStamp = document.getElementById(stamp_id_S);
                preStamp.style.border = "1px solid";
                currentStamp.style.border = "5px solid";

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

            if(loadcount == srcs.length){
                mySort();
            }
        }

    }

    function mySort() {
        // (1) ノードリストを取得
        var myUL = document.getElementsByClassName("stamps");
        var myNodeList = myUL[0].getElementsByTagName("canvas");
    
        // (2) 配列を得る
        var myArray = Array.prototype.slice.call(myNodeList);
        // (3) 配列をソート
        function compareText (a,b) {
            if ( a.id > b.id)
                return 1;
            else if (a.id < b.id)
                return -1;
            return 0;
        }
        myArray.sort(compareText);
        // (4) 新しい順番を DOM ツリーに反映
        //とりあえず一度全消ししてから、追加しとく
        while(myUL[0].firstChild){
            myUL[0].removeChild(myUL[0].firstChild);
        }
        for (var i=0; i<myArray.length; i++) {
            myUL[0].appendChild(myArray[i]);
        }
    
        //ついでに初期スタンプを強調しておく
        let currentStamp = document.getElementById(stamp_id_S);
        currentStamp.style.border = "5px solid";
    }

    //台紙画像の読み込み
    img.src = 'assets/backWhite.png'; //解像度72
    // 画像読み込み終了してから描画
    img.onload = function(){
        w = img.width;
        h = img.height;
        // console.log(w);
        // console.log(h);
        canvasL.width = w;
        canvasL.height = h;
        c.drawImage(img, 0, 0, w, h);
        //addCanvasList();
    }

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
    concatCanvas("#canvasBack", asset_id, canvasX, canvasY, 1);
    //concatCanvas("#canvas", "#stamp");
});

//スタンプ用
async function concatCanvas(base, asset, cX, cY, mag){
    const canvasM = document.querySelector(base); //ここは変えない方が良い
    //console.log(canvasM);
    const ctx = canvasM.getContext("2d");

    const image1 = await getImagefromCanvas(asset);
    ctx.drawImage(image1, cX-(asset_w), cY-(asset_h), image1.width/mag, image1.height/mag);

}


//スタンプ台紙用
let paintImage_w = 0;
let paintImage_h = 0;
async function concatCanvas_M(base, asset, cX, cY, mag){
    const canvasM = document.querySelector(base); //ここは変えない方が良い
    //console.log(canvasM);
    const ctx = canvasM.getContext("2d");

    const image1 = await getImagefromCanvas(asset);
    ctx.drawImage(image1, cX, cY, image1.width/mag, image1.height/mag);

    paintImage_w = image1.width/mag;
    paintImage_h = image1.height/mag;
}

function getImagefromCanvas(id){
    return new Promise((resolve, reject) => {
        const image = new Image();
        const cnv = document.querySelector(id);
        const ctx = cnv.getContext("2d");
        image.onload = () => {
            resolve(image);
        }
        image.onerror = (e) => reject(e);
        image.src = ctx.canvas.toDataURL();
    });
}

function reset(){
    c.drawImage(img, 0, 0, w, h); //リセット
}


// 「選択された画像の一覧画面」のところに<canvas>を追加する処理
function addCanvas_Re( parentname, divname, name, index, width_, height_, class_name) {

    let parentnode = document.getElementsByClassName(parentname);

    let divElement = document.createElement('div');
    divElement.className = divname;
    parentnode[0].appendChild(divElement);
    
    let canvasElement = document.createElement('canvas');
    // canvasElement.id = "stamp" + (index);
    canvasElement.id = name + (index);
    // canvasElement.style.width  = stamp_siv_width/2+"px";
    // canvasElement.style.height = stamp_siv_height/2+"px";
    canvasElement.style.width  = width_+"px";
    canvasElement.style.height = height_+"px";
    canvasElement.style.border = "1px solid";
    canvasElement.className = class_name;
    //canvasElement.style.float = "left";
    canvasElement.willReadFrequently = true;

    divElement.appendChild(canvasElement);

    return canvasElement.id;
}

let button_move = document.getElementById("moveB");
button_move.addEventListener("click", addCanvasList);



// 「選択された画像の一覧画面」のところに<canvas>を追加する処理
function addsaveImage( index, width_, height_) {

    let parentnode = document.getElementsByClassName("savaImages");

    let divElement = document.createElement('div');
    divElement.className = "sadiv";
    parentnode[0].appendChild(divElement);
    
    let imgElement = document.createElement('img');
    imgElement.id = 'saveI_' + (index);
    imgElement.style.width  = width_+"px";
    imgElement.style.height = height_+"px";
    imgElement.hidden = true;
    imgElement.willReadFrequently = true;

    divElement.appendChild(imgElement);

    return imgElement.id;
}


let width_prepdf = 100;
let height_prepdf = 80;

async function addCanvasList(){
    let index_length = document.getElementsByClassName("canvases");
    var CNodeList = index_length[0].getElementsByTagName("canvas");

    let CNodeList2 = [];
    let j=0;
    for(let i=0; i<CNodeList.length-1; i++){
        if(!stateOfFrame[i]) {
            console.log("!!");
            continue;
        }
        CNodeList2[j] = CNodeList[i];
        j+=1;
    }

    for(let i=0; i<CNodeList2.length-1; i++){
        let id = addCanvas_Re("canvases_List", "divdiv", "canvasN", i, w, h, "area");
        let base_id = '#'+id;
        let canvasP = document.getElementById(id);
        let ctcc = canvasP.getContext('2d');
        canvasP.width = w;
        canvasP.height = h;
        ctcc.drawImage(img, 0, 0, w, h);

        let page_id = '#' + CNodeList2[i].id;
        concatCanvas_M(base_id, page_id, width_prepdf, height_prepdf ,4);
        let pageN_id = '#' + CNodeList2[i+1].id;
        concatCanvas_M(base_id, pageN_id, width_prepdf+400, height_prepdf ,4);

        let flag = true;
        let image_id = "";
        let ff="";
        canvasP.addEventListener("click", point=>{
            console.log(id);
            if(flag == true){
                image_id = addsaveImage(i, w, h);
                ff = document.getElementById(image_id);
                ff.src = canvasP.toDataURL("image/jpeg");
                ff.onload = ()=>{
                    console.log("NN");
                }
                flag = false;
            }

            const rect = point.target.getBoundingClientRect();
        
            // ブラウザ上での座標を求める
            const   viewX = point.clientX - rect.left,
                    viewY = point.clientY - rect.top;
        
            // 表示サイズとキャンバスの実サイズの比率を求める
            const   scaleWidth =  canvasP.clientWidth / canvasP.width,
                    scaleHeight =  canvasP.clientHeight / canvasP.height;
        
            // ブラウザ上でのクリック座標をキャンバス上に変換
            const   canvasX = Math.floor( viewX / scaleWidth ),
                    canvasY = Math.floor( viewY / scaleHeight );
        
            console.log( "tap" );
            console.log( canvasX,canvasY );

            relatestamps[i] = {rX:(canvasX-width_prepdf-stamp_siv_width/2)/paintImage_w 
            ,rY:(canvasY-height_prepdf-stamp_siv_height/2)/paintImage_h};
            console.log(i+':'+base_id+':'+relatestamps[i].rX);

            stamp_idSave[i] = stamp_id_S;

            console.log(relatestamps);
            console.log(stamp_idSave);

            //ctcc.drawImage(imageB_E, 0, 0, w, h); //リセット
            ctcc.drawImage(ff, 0, 0, w, h); //リセット
            //ctcc = save[i];
            // let base_id = '#'+id;
            let asset_id = '#'+stamp_id_S;
            concatCanvas(base_id, asset_id, canvasX, canvasY, 1);
        });
        
    }
}
