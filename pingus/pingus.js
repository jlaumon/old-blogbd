//      pingus.js - v1.0
//      
//      Copyright 2009 Jérémy Laumon <j.laumon@lavache.com>
//      
//      This program is free software. It comes without any warranty, to
//		the extent permitted by applicable law. You can redistribute it
//		and/or modify it under the terms of the Do What The Fuck You Want
//		To Public License, Version 2, as published by Sam Hocevar. See
//		http://sam.zoy.org/wtfpl/COPYING for more details.
//		
//		Png images and sounds are from the game "Pingus" and are published
//		under the GNU GPL. More info at http://pingus.seul.org
//		jQuery, jQuery timer plugin and jQuery sound plugin are also free
//		softwares. See their own headers for more info.


//	How to rear a pinguin :
//	1. First, you need to choose where you want him to live :
//
//		Just put a <div id="mypingus"></div> where you want.
//
//	2. Then, you need to put these 4 lines in the header of your page :
//		
//		<script type="text/javascript" src="/your-pingus-folder/jquery.js"></script>
//    	<script type="text/javascript" src="/your-pingus-folder/jquery.timer.js"></script>
//    	<script type="text/javascript" src="/your-pingus-folder/jquery.sound.js"></script>
//		<script type="text/javascript" src="/your-pingus-folder/pingus.js"></script>
//
//		And don't forget to change the src fields. If you already have jQuery, note that
//		v1.2 or more recent is required. You MUST use my versions of jquery.timer and 
//		jquery.sound because I modified them.
//
//	3. Finally, bring him to life by calling the function "play" like this :
//		
//		<script type="text/javascript">
//	   	pingus.play({
//    		id: "mypingus",		// Id of the div where pingus will live
//    		limit_left: 0,		// Where pingus starts, in pixels (0 means pingus starts at the beginning of its parent div)
//    		limit_right: 100,	// Where pingus turns back, in pixels
//    		sound_enabled: true,// Enable sounds (true/false)
//    		url_media: "/your-pingus-folder/",	// url of the pingus directory (DON'T FORGET THE TRAILING SLASH)
//		});	
//		</script>
//		
//		This code has to be put just after the 4 lines described in the 2.
//		And voilà !

  
  var pingus={
 	play:function(config){
		$(document).ready(function(){
			
			var limit_left = config.limit_left;
			var limit_right = config.limit_right;
			var direction = "right";
			var margin_left = limit_left;
			var bg_position = {
				left: 0,
				top: 0
			}
			var current_state = "";
			var new_state = "walker";
			var first_run = true;
			
			$("#" + config.id).css({
				"height" : "32px",
				"width" : "32px",
				"overflow" : "hidden",
				"cursor" : "pointer"
			});
		
			$.timer({name: config.id, interval: 45}, function() {
				if (new_state) {
					if(new_state == "walker") {
						direction = "right";
						margin_left = limit_left;
						bg_position.left = 0;
						bg_position.top = 32;
						$("#" + config.id)
							.css("background-position", bg_position.left + "px " + bg_position.top + "px")
							.css({"background-image" : "url(" + config.url_media +"walker.png)"})
							.css("margin-left", limit_left);
						if (!first_run) {
							$.timers[config.id].interval = 45;
								$.stopTimer(config.id);
								$.runTimer(config.id);
							if(config.sound_enabled)
								$.sound.play(config.url_media +"yipee.wav", { track: "yipee"+config.id, unique: true, timeout: 3000 });
						}
						else
							first_run = false;
					}
					if(new_state == "bomber") {
						bg_position.left = 0;
						bg_position.top = 0;
						$("#" + config.id)
							.css("background-position", bg_position.left + "px " + bg_position.top + "px")
							.css({"background-image" : "url(" + config.url_media +"bomber.png)"});
					}
					current_state = new_state;
					new_state = "";
				}
				else {
					if (current_state == "walker" ) {
						bg_position.left = (bg_position.left-32)%256;
						switch(direction) {
							case "right":
								margin_left += 2;
								$("#" + config.id).css("margin-left", margin_left);
								if(margin_left > limit_right) {
									direction = "left";
									bg_position.top = 0;
								}
								break;
							case "left":
								margin_left -= 2;
								$("#" + config.id).css("margin-left", margin_left);
								if(margin_left < limit_left) {
									direction = "right";
									bg_position.top = 32;
								}
								break;
						}
						$("#" + config.id).css("background-position", bg_position.left + "px " + bg_position.top + "px");	
					}
					if (current_state == "bomber" ) {
						bg_position.left = (bg_position.left-32);
						if (bg_position.left == -32) {
							$.timers[config.id].interval = 1000;
							$.stopTimer(config.id);
							$.runTimer(config.id);
						}
						if (bg_position.left == -64) {
							$.timers[config.id].interval = 45;
							$.stopTimer(config.id);
							$.runTimer(config.id);
						}
						if (bg_position.left == -384)
							if(config.sound_enabled)
								$.sound.play("" + config.url_media + "plop.wav", { track: "plop"+config.id, unique: true, timeout: 3000 });
						if (bg_position.left <= -512) {
							new_state = "walker";
							$("#" + config.id)
								.css({"background-image" : "none"});
							$.timers[config.id].interval = 2000;
							$.stopTimer(config.id);
							$.runTimer(config.id);
						}
						else {
							$("#" + config.id)
								.css("background-position", bg_position.left + "px " + bg_position.top + "px");
						}
					}
				}
			});
			
			$("#" + config.id)
				.click(function() {
					if(config.sound_enabled)
						$.sound.play(config.url_media + "ohno.wav", { track: "ohno"+config.id, unique: true, timeout: 3000 });
					new_state = "bomber";
				})
		});
	}
}
		
