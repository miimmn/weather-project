siData = [
  "강원특별자치도",
  "경기도",
  "경상남도",
  "경상북도",
  "광주광역시",
  "대구광역시",
  "대전광역시",
  "부산광역시",
  "서울특별시",
  "세종특별자치시",
  "울산광역시",
  "인천광역시",
  "전라남도",
  "전라북도",
  "제주특별자치도",
  "충청남도",
  "충청북도",
];

$(document).ready(function () {
  $("#Si-selectBox").dxSelectBox({
    placeholder: "시/도를 선택하세요",
    dataSource: siData,
    showClearButton: true,
  });
  $("#Gu-input").dxTextBox({
    placeholder: "..........",
    showClearButton: true,
  });

  $("#Dong-input").dxTextBox({
    placeholder: "..........",
    showClearButton: true,
  });

});



// 날씨 검색
function getWeather() {

  si = $("#Si-selectBox").dxSelectBox("instance").option("value")
  gu = $("#Gu-input").dxTextBox("instance").option("value")
  dong = $("#Dong-input").dxTextBox("instance").option("value")

  $.ajax({
    type: "GET",
    url: "/weather/getweather",
    data: { 
      "si" : si,
      "gu" : gu,
      "dong" : dong
    },
    success: function (data) {
      weatherGraph(data)
      console.log("성공... " , data);
    },
    error: function (request) {
      console.log("오류 오류 오류");
    },
  });
}


// 기온 그래프
function weatherGraph(data) {

  var si = $("#Si-selectBox").dxSelectBox("instance").option("value")
  var gu = $("#Gu-input").dxTextBox("instance").option("value")
  var dong = $("#Dong-input").dxTextBox("instance").option("value")
  
  $('#chart-t').dxChart({
    palette: 'Violet',
    dataSource: {
      store : data
    },
    commonSeriesSettings: {
      argumentField: 'fcstTime',
    },
    margin: {
      bottom: 20,
    },
    argumentAxis: {
      valueMarginsEnabled: 'false',
      discreteAxisDivisionMode: 'crossLabels',
      grid: {
        visible: true,
      },
    },
    valueAxis: [{
      name: 'temperature',
      title: {
        text: 'Temperature, °C',
        font: {
          color: '#e91e63',
        },
      },
      label: {
        font: {
          color: '#e91e63',
        },
      },
    }, {
      name: 'humidity',
      position: 'right',
      title: {
        text: 'Humididty, %',
        font: {
          color: '#03a9f4',
        },
      },
      label: {
        font: {
          color: '#03a9f4',
        },
      },
    },
    ],
    series: [
      { axis: 'temperature', valueField: 'temperature', name: '기온', type : 'line' },
      { axis: 'humidity', valueField: 'humidity', name: '습도', type : 'splinearea'},
    ],
    legend : {
      visible : false,
    },
    title: {
      text: `${si} ${gu} ${dong} 날씨`,
      subtitle: {
        text: '(당일 ~ 2일까지의 예보가 나타납니다.)',
      },
    },
    export: {
      enabled: true,
    },
    tooltip: {
      enabled: true,
    },
    
  })
}


