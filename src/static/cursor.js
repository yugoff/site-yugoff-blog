			
	//Page cursors
	
	$(window).mousemove(function(e) { 	  
		$(".cursor").css({
			left: e.pageX,
			top: e.pageY
		})	  
	})
	$(".cursor-link")
	.on("mouseenter", function() {	 
	$('.cursor').addClass("active")	  
	})
	.on("mouseleave", function() {	  
	$('.cursor').removeClass("active")	  
	})		



	