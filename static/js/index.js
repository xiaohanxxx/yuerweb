$(function(){
	$('.headerNav-ul ul li').hover(function(){
		$(this).find('.xialabox').show();
	},function(){
		$(this).find('.xialabox').hide();
	})
    $('.bannerwz').hover(function(){
		$(this).css("background-color","#e2afd6");
		$(this).find('.hidebox').show();
	},function(){
		$(this).css("background-color","");
		$(this).find('.hidebox').hide();
	})
   $('.titleanswer').click(function(){
		var _this = $(this);
		if(_this.find('abbr').hasClass('hides')){
			_this.find('abbr').removeClass('hides');
			_this.find('p').hide();
		}else{
			_this.find('abbr').addClass('hides');
			_this.find('p').show(300);
		}
	})
    $('.fristmama').hover(function(){
        var _this = $(this);
    	_this.hide();
		_this.next('.tuxiangbig').show();
	},function(){
		_this.next('.tuxiangbig').hide();
    	_this.show();
	})


   $('#blurfs').blur(function(){
   	  $(this).prev().find('ol').hide();
   })
   $('#blurfs').click(function(){
   	  $(this).prev().find('ol').show();
   	  $(this).prev().find('ul').addClass('hites');
   })
})


