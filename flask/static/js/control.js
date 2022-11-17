function getDetailData() {
    $.ajax({
        url: "/getOverViewData",
        timeout: 3000,
        success: function (data) {
            // console.log("This is get VideoDetailData", data);
            $(".bold").eq(0).html(data.following);
            $(".bold").eq(1).html(data.follower);
            $(".bold").eq(2).html(data.likes);
            $(".bold").eq(3).html(data.play_view);
            $(".bold").eq(4).html(data.article_view);
            $(".bold").eq(5).html(data.count);

            sumScore = data.follower + data.likes*0.01 + data.play_view*0.001 + data.article_view + data.count;
            // console.log("sumScore", sumScore);
            //将sumScore转为整数
            sumScore = parseInt(sumScore);
            // console.log("sumScore", sumScore);
            //获取sumScore的每一位数
            var sumScoreArr = sumScore.toString().split("");
            //获取sumScore的长度
            var sumScoreLength = sumScoreArr.length;
            //获取sumScore的每一位数
            for (var i = 7; sumScoreLength > 0; i--) {
                $(".score").eq(i).html(sumScoreArr[sumScoreLength - 1]);
                sumScoreLength--;
            }

        },
        error: function (data) {
            console.log(data);
        }
    });
}

getDetailData();
// setInterval(getDetailData, 5000);


