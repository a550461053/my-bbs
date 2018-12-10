$(document).ready(function(){
    $('.sideBar ul li').click(function(){
        $(this).addClass('active').siblings().removeClass('active');
        $('.content > div').eq($(this).index()).addClass('selected').siblings().removeClass('selected');
    });
});



