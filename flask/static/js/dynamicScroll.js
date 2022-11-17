//滚动
//原理：把marquee下面的子盒子都复制一遍 加入到marquee中然后动画向上滚动，滚动到一半重新开始滚动
//因为选取的是两个marquee  所以要遍历
$('.marquee').each(function (index, dom) {
    //将每个dom的所有子级都复制一遍
    var rows = $(dom).children().clone();
    //再将新的到的加入原来的
    $(dom).append(rows);
});