// パワーポイントを作る関数
function makePPTX() {
  const allStart = performance.now();
  function Cm(n) {
      return n * 0.3937;
  }
  function Pt(n) {
      return n / 72;
  }

  //let startTime = performance.now();

  let pptx = new PptxGenJS();
  pptx.defineLayout({ name:'A4', width:11.7, height:8.3 });
  pptx.layout = 'A4';
  let slide = pptx.addSlide();

  let x = Cm(2.5);
  let y = Cm(0.5);
  let x2 = Cm(7.2);
  let y2 = Cm(4.25);
  let width = Cm(4.39);
  //let height = Cm(9.5);
  let height = width * videoRatio;
  let selectedImageData = [];
  let size = 28;

  // canvasに書かれたデータを読み取るコード
  for(let i=0; i<stateOfFrame.length; i++) {
      if(stateOfFrame[i]) {
          cvs = document.getElementById(`canvas${i}`);
          ctx = cvs.getContext('2d');
          imagedata = cvs.toDataURL("image/jpeg");
          selectedImageData.push(imagedata);
      }
  }

  //let endTime = performance.now();
  //console.log("キャンバスの取得時間:" + (endTime - startTime));
  
  for(let i = 0; i < selectedImageData.length; i++) {

      if (i % 8 === 0 && i!== 0){
          slide = pptx.addSlide();
          y = Cm(0.5);
          y2 = Cm(4.25)
      }

      //startTime = performance.now();
      
      slide.addImage({ path: "assets/black.png", w: width+Cm(0.12), h: height+Cm(0.12), x: x-Cm(0.06), y: y-Cm(0.06) });
      slide.addImage({ data: selectedImageData[i], w: width, h: height, x: x, y: y });
      slide.addText(String(i+1), {x: x-Cm(1.5), y: y, w: Pt(size*2), h: Pt(size), color: "363636", fontSize: size});

      // endTime = performance.now();
      // console.log("画像・枠線・番号の追加時間：" + (endTime - startTime));

      if (i % 4 == 3){
          x = Cm(2.5);
          y += Cm(10);
          x2 = Cm(7.2)
          y2 += Cm(10)
      } else {
          x += Cm(7);
          if (i != selectedImageData.length-1){
          slide.addImage({ path: "assets/arrow.png", w: Cm(2), h: Cm(2), x: x2, y: y2 });
          x2 += Cm(7) 
          }
      }

      // endTime = performance.now();
      // console.log("矢印込みの追加時間：" + (endTime - startTime));
  }

  //画像を２枚ずつパワポに出力
  //height = Cm(16);
  width = Cm(7.39);
  //let pre_imagedata = null;
  height = width * videoRatio;
  size = 36;
  y = Cm(2.5);

  for(let i=0;i<selectedImageData.length;i++){
      //console.log("--------２列---------");


      if (i === 0) {
          continue
      }

      slide = pptx.addSlide();

      // startTime = performance.now();
      
      x = ( 11.7/2 - width ) / 2
      slide.addImage({ path: "assets/black.png", w: width+Cm(0.12), h: height+Cm(0.12), x: x-Cm(0.06), y: y-Cm(0.06) });
      slide.addImage({ data: selectedImageData[i-1], w: width, h: height, x: x, y: y });
      slide.addText(String(i),  {x: x-Cm(2.5), y: y, w:Pt(size*2), h:Pt(size), color: "363636", fontSize: size});

      slide.addImage({ path: "assets/arrow.png", w: Cm(3.33), h: Cm(3.33), x: Cm(13.18), y: Cm(8.84) });
      
      x += (11.7/2)
      slide.addImage({ path: "assets/black.png", w: width+Cm(0.12), h: height+Cm(0.12), x: x-Cm(0.06), y: y-Cm(0.06) });
      slide.addImage({ data: selectedImageData[i], w: width, h: height, x: x, y: y });
      slide.addText(String(i+1),{x: x-Cm(2.5), y: y, w:Pt(size*2), h:Pt(size), color: "363636", fontSize: size});

      if(stamp_idSave[i-1] != undefined) {
        const path = 'assets/stamps/' + stamp_idSave[i-1] + '.png';
        const stamp_x = x + relatestamps[i-1].rX * width - 11.7/2;
        const stamp_y = y + relatestamps[i-1].rY * height;
        const stamp_width = stamp_siv_width * (width/paintImage_w);
        const stamp_height = stamp_width * (stamp_siv_height / stamp_siv_width);
        slide.addImage({ path: path, w: stamp_width, h: stamp_height, x: stamp_x, y: stamp_y });
      } 

      // endTime = performance.now();
      // console.log("画像２枚・枠線・番号・矢印の追加時間：" + (endTime - startTime));
      
  }

  // パワポを保存
  pptx.writeFile({ fileName: "らくらくトリセツ.pptx" });
  // const allEnd = performance.now();
  // console.log("全実行時間：" + (allEnd - allStart));
}
