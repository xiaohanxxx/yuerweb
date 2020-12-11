 (function () {
    window.Toolfun = {
        clearClass: function (className, items) {
            for (var i = 0; i < items.length; i++) {
                if (items.eq(i).hasClass(className)) {
                    items.eq(i).removeClass(className);
                }
            }
        },
        diguiClass: function (datalis, comment) {
            var resData = [];
            for (var a in comment) {
                comment[a].child = [];
                var hChild = [];
                for (var b in datalis) {
                    if (comment[a].id == datalis[b].parent) {
                        hChild.push(datalis[b]);
                    }
                }
                if (hChild) {
                    comment[a].child = Toolfun.diguiClass(datalis, hChild);
                }
                resData.push(comment[a])
            }
            return comment = resData;
        },
        snimgzsClass: function (data) {//data为数组
            for (var i = 0; i < data.length; i++) {
                if (data[i].content.indexOf('<img') != '-1') {
                    var snimg = JSON.stringify(data[i].content.match(/src=".*\.(jpg|png)"/g)).match(/\/media\/.*\.(jpg|png)/);
                    if(snimg){
                        data[i].snimg = snimg[0];
                    }else{
                        data[i].snimg = '/media/luntan/moren.jpg';
                    }
                } else {
                    data[i].snimg = '/media/luntan/moren.jpg';
                }
            }
        },
        iszhezClass:function(){
            $('.mainzz').height(document.body.scrollHeight);
            $('.mainzz').fadeIn();
        },
        qxzheClass:function(){
            $('.mainzz').fadeOut();
        },
        getlunboClass:function(type,data){
            var imgdata = [];
            $.ajax({
                url:root_Domain+'/webmanage/banner',
                type:'post',
                data:{
                    'bannertype':type,
                },success:function(ajax){
                    imgdata = ajax.data;
                    data = imgdata;
                    console.log(data,111,typeof(ajax.data) )
                },error:function(error){
                    console.log(error);
                }
            })
        }
    }
})();