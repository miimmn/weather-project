
const siData = [
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
      searchEnabled: true,
      width: 200,
    });
    $("#Gu-input").dxTextBox({
      placeholder: "..........",
      showClearButton: true,
      width: 150,
    });
  
    $("#Dong-input").dxTextBox({
      placeholder: "..........",
      showClearButton: true,
      width: 150,
    });
  });
  
  
  // 날씨 검색
  function getWeather() {
  
    var si = $("#Si-selectBox").dxSelectBox("instance").option("value");
    var gu = $("#Gu-input").dxTextBox("instance").option("value");
    var dong = $("#Dong-input").dxTextBox("instance").option("value");
  
    $.ajax({
      type: "GET",
      url: "/weather/getweather",
      data: { 
        "si" : si,
        "gu" : gu,
        "dong" : dong
      },
      success: function (data) {
        weatherGraph(data, si, gu, dong);
        console.log("성공... " , data);
      },
      error: function (xhr, status) {
        if(xhr.status == 400) {
          alert("주소값이 유효하지 않습니다. 다시 입력해 주세요.");
        }
      },
    });
  }
  
  
  // 예보 그래프 그리기
  function weatherGraph(data, si, gu, dong) {

    var startValue = data[0]['fcstTime'];
    var endValue = data[20]['fcstTime'];
  
    $('#chart-t').dxChart({
      palette: ['#EF9A9A','#727272'],
      dataSource: {
        store : data,
      },
      commonSeriesSettings: {
        argumentField: 'fcstTime',
      },
      margin: {
        bottom: 20,
      },
      customizePoint: function(pointInfo) {
        // 특정 그래프에만 이미지 적용
        if (pointInfo.series.type === "line") {
            return {
                image: { url: '/icon/'+pointInfo.data.status+'.png', width: 25, height: 25 },
                visible: true
            };
        } else {
            return {};
        }
      },
      scrollBar: {
        visible: true,
      },
      zoomAndPan: {
        argumentAxis: 'both',
      },
      argumentAxis: {
        valueMarginsEnabled: 'false',
        discreteAxisDivisionMode: 'crossLabels',
        grid: {
          visible: true,
        },
        label: {
          customizeText: function (arg) {
              var origin = arg.value.substr(5,2);
              if(origin == '00') {
                return arg.value.substr(2,2) + '일 ' + origin+'시';
              }
              return origin+'시';
          }
        },
        visualRange: {
          startValue: startValue, 
          endValue: endValue,
        },
      },
      valueAxis: [{
        name: 'temperature',
        title: {
          text: 'Temperature, °C',
          font: {
            color: '#000000',
          },
        },
        label: {
          font: {
            color: '#000000',
          },
        },
         
      }, {
        name: 'humidity',
        position: 'right',
        title: {
          text: 'Humididty, %',
          font: {
            color: '#ef5350',
          },
          
        },
        label: {
          font: {
            color: '#000000',
          },
        },
      },
      ],
      series: [
        { 
          axis: 'humidity',
          valueField: 'humidity', 
          name: '습도', 
          type : 'splinearea',
        },
        { 
          axis: 'temperature', 
          valueField: 'temperature', 
          name: '기온', 
          type : 'line',
        },
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
  
  // 로그아웃
  function logout() {
    $.ajax({
      type: "POST",
      url: "/user/logout",
      success : function() {
        window.location.href = '/user/loginview';
      },
    });
  }
  
  // 검색 기록 페이지
  function getSearchHistory() {
    $.ajax({
      type: "GET",
      url: "/history",
      success : function() {
        window.location.href = '/history';
      },
    });
  }