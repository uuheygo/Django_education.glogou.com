$(document).ready(function(){
    console.log("dddddd");
    
   
    
    //display cosmetics tab
    $('#tabs-Cosmetics').addClass('active');
    
    //carousel*************************************************
    $('#myCarousel').carousel({
	interval: 2000
    })
    
    $('.carousel .item').each(function(){
	var next = $(this).next();
	if (!next.length) {
	    next = $(this).siblings(':first');
	    }
	    next.children(':first-child').clone().appendTo($(this));
  
	    for (var i=0;i<2;i++) {
		next=next.next();
		if (!next.length) {
		    next = $(this).siblings(':first');
		    }
    
		next.children(':first-child').clone().appendTo($(this));
	    }
	});
    //showmore and showless ******************************************************8
    var default_display = '.sub_cat'
    $(default_display).each(function(){
	$(this).children(':first-child').next().children().children().slice(0,8).show()
	});
    $('.showMore').click(function(){
	$(this).prev().children().children().css('display', 'block')
	$(this).addClass("hide")
	$(this).next().removeClass("hide")
	})
    $('.showLess').click(function(){
	console.log("showlesssss");
	
	$(this).prev().prev().children().children().css('display', 'none')
	$(this).prev().prev().children().children().slice(0,8).show()
	$(this).addClass("hide")
	$(this).prev().removeClass("hide")
    })
    //hover to show city name *****************************************************
    $('.thumbnail_city').hover(function(){
	console.log(this);
	$(this).children('.caption_city').css("display", "block");
	},function(){
	    $(this).children('.caption_city').css("display", "none");
	    })
});
 //display city_A tab **************************************

    var cur_cap = '#city_' + current;
    console.log(cur_cap);
    $(cur_cap).addClass('active');
    $('.Cap_tab').click(function(){
	sel_id=$(this).children().attr('href');
	console.log(sel_id);
	$(cur_cap).removeClass('active');
	cur_cap = sel_id;
	$(cur_cap).addClass('active');
	});