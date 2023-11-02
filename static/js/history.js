$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/history/getSearchHistory",
        success: function (data) {
            showSearchHistory(data);
        },
    });
});


// // 서버로부터 받아온 검색 기록 보여주기
function showSearchHistory(data) {
    console.log("dsfsdf", data);
    // var keys = Object.keys(data);
    // var values = Object.keys(data).map(key => data[key]);
    // var values = Object.values(data);


    const listWidget = $('#simpleList').dxList({
        dataSource: data,
        itemTemplate: function(itemData) {
            return itemData.address;
        },
        height: 400,
        width : 1000,
        allowItemDeleting: false,
        itemDeleteMode: 'toggle',

        // 삭제 처리............
        onItemDeleting: function(e) {
            $.ajax({
                type: "DELETE",
                url: "/history/deleteSearchHistory/" + e.itemData.id,
                success: function (data) {
                    alert("삭제되었습니다.");
                },
            });
          }
      }).dxList('instance');
    
      $('#allowDeletion').dxCheckBox({
        value: false,
        text: 'Allow deletion',
        onValueChanged(data) {
          listWidget.option('allowItemDeleting', data.value);
        },
      });
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

