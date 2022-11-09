// PDFを作る関数
function makePDF() {
  const allStart = performance.now();

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({orientation: "landscape"}); // 向きを指定する

  // 初期位置
  let x = 25;     // スマホ画像用
  let y = 5;
  let x2 = 72;    // 矢印画像用
  let y2 = 42.5;
  let width = 43.9;
  // let height = 95;
  let height = width * videoRatio;
  let selectedImageData = [];

  // フォントサイズの指定
  doc.setFontSize(27);

  // let startTime = performance.now();
  // canvasに書かれたデータを読み取るコード
  for(let i=0; i<stateOfFrame.length; i++) {
      if(stateOfFrame[i]) {
          cvs = document.getElementById(`canvas${i}`);
          ctx = cvs.getContext('2d');
          imagedata = cvs.toDataURL("image/jpeg");
          selectedImageData.push(imagedata);
      }
  }
  // let endTime = performance.now();
  // console.log("キャンバスの取得時間:" + (endTime - startTime));

  for(let i=0; i<selectedImageData.length; i++) {
      // console.log("--------４列---------");
      
      if (i % 8 === 0 && i !== 0){
          // ページを増やす
          doc.addPage({orientation: "landscape"});
          y = 5;
          y2 = 42.5;
      }

      // startTime = performance.now();

      doc.addImage('assets/black.png', 'PNG', x-0.6, y-0.6, width+1.2, height+1.2);  // 画像の枠線用の黒画像を先に貼る
      doc.addImage(selectedImageData[i], 'JPEG', x, y, width, height);
      doc.text(String(i+1), x-13, y+10);  // 画像番号

      // endTime = performance.now();
      // console.log("画像・枠線・番号の追加時間：" + (endTime - startTime));

      if (i % 4 === 3){
          x = 25;
          y += 100;
          x2 = 72;
          y2 += 100;
      } else {
          x += 70;
          if(i != selectedImageData.length-1){
              doc.addImage('assets/arrow.png', 'PNG', x2, y2, 20, 20);
              x2 += 70 
          }
      }

      // endTime = performance.now();
      // console.log("矢印込みの追加時間：" + (endTime - startTime));

  }

  // 画像を２枚ずつ連番で出力
  // height = 160;
  width = 73.9;
  height = width * videoRatio;
  y = 25;

  // フォントサイズの指定
  doc.setFontSize(35);  

  for(let i =0; i<selectedImageData.length; i++) {
      // console.log("--------２列---------");

      if (i === 0) {
          continue
      }

      //ページを増やす
      doc.addPage({orientation: "landscape"});

      // startTime = performance.now();

      // 左の画像
      x = ( 297/2 - width ) / 2;
      doc.addImage('assets/black.png', 'PNG', x-0.8, y-0.8, width+1.6, height+1.6);  // 画像の枠線用の黒画像を先に貼る
      doc.addImage(selectedImageData[i-1], 'JPEG', x, y, width, height);
      doc.text(String(i), x-15, y+10);

      doc.addImage('assets/arrow.png', 131.8, 88.4, 33.3, 33.3); 

      // 右の画像
      x += 297/2
      doc.addImage('assets/black.png', 'PNG', x-0.8, y-0.8, width+1.6, height+1.6);  // 画像の枠線用の黒画像を先に貼る
      doc.addImage(selectedImageData[i], 'JPEG', x, y, width, height);
      doc.text(String(i+1), x-15, y+10);

      // endTime = performance.now();
      // console.log("画像２枚・枠線・番号・矢印の追加時間：" + (endTime - startTime)); 

      // スタンプの画像
      if(stamp_idSave[i-1] != undefined) {
        const path = 'assets/stamps/' + stamp_idSave[i-1] + '.png';
        const stamp_x = x + relatestamps[i-1].rX * width - 297/2;
        const stamp_y = y + relatestamps[i-1].rY * height;
        const stamp_width = stamp_siv_width * (width/paintImage_w);
        const stamp_height = stamp_width * (stamp_siv_height / stamp_siv_width);
        doc.addImage(path, 'PNG', stamp_x, stamp_y, stamp_width, stamp_height);
      }  
  }
      
  // addImage(imageData, format, x, y, width, height, alias, compression, rotation)
  // https://artskydj.github.io/jsPDF/docs/module-addImage.html
  // doc.addImage(imagedata, 'JPEG', 30, 30, 80, 160);

  doc.save("らくらくトリセツ.pdf");

  const allEnd = performance.now();
  console.log("全実行時間：" + (allEnd - allStart));
}
