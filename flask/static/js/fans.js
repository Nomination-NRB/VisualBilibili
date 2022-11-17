function getFans() {
    $.ajax({
        url: "/getFansData",
        timeout: 3000,
        success: function (data) {
            // console.log("This is FansData", data.fans[0]);
            // $(".row .col").eq(0).html(data.fans[0][0]);
            // $(".row .col").eq(1).html(data.fans[0][1]);
            // $(".row .col").eq(2).html(data.fans[0][2]);
            // 根据data.fans的长度，动态生成html
            var html = "";
            for (var i = 0; i < data.fans.length; i++) {
                html += "<div class='row'>";
                html += "<span class='col'>" + data.fans[i][0] + "</span>";
                html += "<span class='col'>" + data.fans[i][1] + "</span>";
                html += "<span class='col'>" + data.fans[i][2] + "</span>";
                html += "</div>";
                $(".marquee").html(html);
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}

getFans();
// setInterval(getDetailData, 5000);
