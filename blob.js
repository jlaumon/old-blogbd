//      blob.js - v1.0
//      
//      Copyright 2009 Jérémy Laumon <j.laumon@lavache.com>
//      
//      This program is free software. It comes without any warranty, to
//      the extent permitted by applicable law. You can redistribute it
//      and/or modify it under the terms of the Do What The Fuck You Want
//      To Public License, Version 2, as published by Sam Hocevar. See
//      http://sam.zoy.org/wtfpl/COPYING for more details.

// TODO
// - add a custom event triggered for each state change
// - add a second (optional) argument to change_state() which is a 
//   callback function to call at the end of the state
// - remove id_timer_death and all this crap and use a callback function
//   with change_state() instead


var blob = {
    
    /*** Vars ***/
    id : '#blob',
    interval : 70,
    width : 128,
    height : 128,
    id_timer_anim : 0,
    id_timer_toggle : 0,
    current_state : '',
    current_index : 0,
    speed : 150,
    alive : true,
    disabled : false,
    
    
    position : {
        left : 0,
        top : 0
    },
    
    home : {
        left : 0,
        top : 0
    },
    
    bubble : {
        id : '#bubble',
        top : '#bubble .bubble_top',
        middle : '#bubble .bubble_middle',
        persistence : 10000,
        msg_ids : [],
        msg_timers : [],
        position : {
            bottom : 0,
            right : 0
        },
        display_only_last_msg : false,
        last_msg : '',
        update_pos : function() {
            
            blob.bubble.position.bottom = $(blob.id).parent().height() - parseInt($(blob.id).css('top'));
            blob.bubble.position.right = $(blob.id).parent().width() - parseInt($(blob.id).css('left')) - $(blob.id).parent().width()/2 - $(blob.id).width()/4 ;

            $(blob.bubble.id).css({'right':blob.bubble.position.right,'bottom':blob.bubble.position.bottom});
        }
    },
    
    
    states : {
        no_blob : {},
        idle : {
            sprite : 'blob_normal.png',
            size : 1,
            duration : [1]
        },
        frown : {
            sprite : 'blob_frown.png',
            size : 13,
            duration : [1,1,1,1,1,1,10,1,10,1,1,1,1],
            next_state : 'idle'
        },
        hands_up : {
            sprite : 'blob_hands_up.png',
            size : 1,
            duration : [1]
        },
        move_right : {
            sprite : 'blob_move_right.png',
            size : 20,
            duration : [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,]
        },
        move_left : {
            sprite : 'blob_move_left.png',
            size : 20,
            duration : [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,]
        },
        transition_left : {
            sprite : 'blob_transition_left.png',
            size : 2,
            duration : [0.5,0.5],
            next_state : 'idle'
        },
        transition_right : {
            sprite : 'blob_transition_right.png',
            size : 2,
            duration : [0.5,0.5],
            next_state : 'idle'
        },
        death : {
            sprite : 'blob_death.png',
            size : 22,
            duration : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            next_state : 'no_blob'
        },
        raise : {
            sprite : 'blob_raise.png',
            size : 14,
            duration : [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            next_state : 'idle'
        }
        
    },
    
    loop : function(){
        if(blob.states[blob.current_state].sprite){
            $(blob.id).css({
                'background-image' : 'url("/'+blob.states[blob.current_state].sprite+'")',
                'background-position' : ''+(-blob.current_index*blob.width)+'px 0px'
            });
        
            if (!blob.states[blob.current_state].next_state){
                blob.id_timer_anim = setTimeout(blob.loop,blob.interval*blob.states[blob.current_state].duration[blob.current_index]);
                blob.current_index = (blob.current_index+1)%blob.states[blob.current_state].size;
            }
            else {
                if (blob.current_index!=blob.states[blob.current_state].size){
                    blob.id_timer_anim = setTimeout(blob.loop,blob.interval*blob.states[blob.current_state].duration[blob.current_index]);
                    blob.current_index = blob.current_index+1;
                }
                else {
                    blob.change_state(blob.states[blob.current_state].next_state);
                }
            }
        }
    },
    
    play : function(){
        $(function(){
            var blob_css_default = {
                'background-color':'transparent',
                'background-image':'url("/blob_normal.png")',
                'background-repeat':'no-repeat',
                'background-attachment':'scroll',
                'background-position':'0px 0px',
                'position':'absolute',
                'cursor':'move',
                'display':'block',
                'opacity':0.8,
                'height':blob.height,
                'width':blob.width,
                'left': $(blob.id).parent().width()/2 - blob.width/2,
                'top': -blob.height,
                'z-index': 100
            }
            $(blob.id).css(blob_css_default);
            
            var bubble_css_default = {
                'position' : 'fixed',
                'bottom' : $(blob.id).parent().height()+blob.height,
                'z-index' : 90,
                'display':'none'
            }
            $(blob.bubble.id).css(bubble_css_default);
            
            var draggable_options = {
                addClasses: false,
                //~ containment: [0, 0, $(window).width(), $(window).height()],
                cursor: 'move',
                opacity: 0.6,
                start: function(event, ui) { blob.change_state('hands_up'); },
                stop: function(event, ui) { blob.change_state('idle'); blob.bubble.update_pos(); }
            }
            $(blob.id).draggable(draggable_options);
            
            
            blob.position = $(blob.id).position();
            blob.home = $(blob.id).position();
            blob.bubble.position.bottom = parseInt($(blob.bubble.id).css('bottom'));
            blob.bubble.position.right = parseInt($(blob.bubble.id).css('right'));
            
            blob.change_state('raise');
        });
    },
    
    change_state : function(state){
        //console.log('Nouvel etat : '+state);
        
        clearTimeout(blob.id_timer_anim);
        blob.current_state=state;
        blob.current_index=0;
        
        /* updates the position var */
        blob.position = $(blob.id).position();
        
        /* stops the current animation */
        $(blob.id).queue('fx',[]);
        $(blob.id).stop();
        
        blob.loop();
    },
    
    move : function(x,y){
        var diff_x = blob.position.left-x;
        var diff_y = blob.position.top-y;
        var distance = Math.sqrt(Math.pow(diff_x,2)+Math.pow(diff_y,2));
        var dir;
        //console.log('Distance a parcourir: '+distance);
        if(diff_x!=0&&diff_y!=0){
            $(blob.bubble.id).fadeOut(200, function(){
                for(var i=0; i< blob.bubble.msg_ids.length;i++){
                $('#'+blob.bubble.msg_ids[i]).remove();
                }
                for(var i=0; i< blob.bubble.msg_timers.length;i++){
                    clearTimeout(blob.bubble.msg_timers[i]);
                }
                blob.bubble.msg_timers = [];
                blob.bubble.msg_ids = [];
            });
            
            if(diff_x>0){
                blob.change_state('move_left');
                dir = 'left';
            }
            else{
                blob.change_state('move_right');
                dir = 'right';
            }
            $(blob.id).animate({'left':x,'top':y}, (distance/blob.speed)*1000, 'linear', function(){
                blob.change_state('transition_'+dir);
                blob.bubble.update_pos();
                callback();
            });
            //~ console.log($(blob.bubble.id).css('bottom'));
            //~ console.log($(blob.bubble.id).css('right'));
            
            //~ $(blob.bubble.id).queue('fx', function(){
                //~ var bubble_bottom = $(blob.id).parent().height() - y;
                //~ var bubble_right = $(blob.id).parent().width() - x - $(blob.id).parent().width()/2 - $(blob.id).width()/4 ;
                //~ $(this).dequeue();
            //~ });
        }
    },
    
    death : function(){
        if(blob.alive){
            $(blob.id).draggable('disable');
            blob.change_state('death');
            blob.alive=false;
            blob.id_timer_death = setTimeout(function(){$(blob.id).hide();},blob.interval*(blob.states['death'].size+10));
        }
    },
    
    raise : function(){
        if(!blob.alive){
            clearTimeout(blob.id_timer_death);
            $(blob.id).show();
            $(blob.id).css({'top':blob.home.top,'left':blob.home.left});
            blob.change_state('raise');
            $(blob.id).draggable('enable');
            blob.alive=true;
        }
    },
    
    go_home : function(){
        if(!blob.alive){
            blob.raise();
        }
        else{
            blob.move(blob.home.left,blob.home.top);
        }
    },
    
    say : function(s){
        if(blob.alive){
            var rand = Math.random();
            if (rand > 0.6)
                blob.change_state('frown');
            var date = new Date();
            var msg_id = ""+date.getSeconds()+date.getMilliseconds();
            $(blob.bubble.middle).append('<div style="display:none" id='+msg_id+'>'+s+'</div>');
            
            if(blob.bubble.msg_ids.length == 0){
                $(blob.bubble.id).show();
                $('#'+msg_id).slideDown(100);
            }
            else{
                $('#'+msg_id).show();
                $(blob.bubble.id).fadeIn(200);
            }
            blob.bubble.msg_ids.push(msg_id);
            
            if(blob.bubble.display_only_last_msg){
                if(blob.bubble.last_msg_id!=undefined){
                    $(blob.bubble.last_msg_id).slideUp(100, function(){
                        $(this).remove();
                    });
                }
                blob.bubble.last_msg_id = '#'+msg_id;
            }
            else{
                blob.bubble.msg_timers.push(setTimeout(function(){ 
                    if(blob.bubble.msg_ids.length == 1){
                        $(blob.bubble.id).fadeOut(200, function(){
                            $('#'+msg_id).remove();
                        });
                        blob.bubble.msg_ids.reverse();
                        blob.bubble.msg_ids.pop();
                        blob.bubble.msg_ids.reverse();
                    }
                    else{
                        $('#'+msg_id).slideUp(100, function(){
                            $(this).remove();
                            blob.bubble.msg_ids.reverse();
                            blob.bubble.msg_ids.pop();
                            blob.bubble.msg_ids.reverse();
                        }); 
                    }
                    blob.bubble.msg_timers.reverse();
                    blob.bubble.msg_timers.pop();
                    blob.bubble.msg_timers.reverse();
                    //~ console.log(blob.bubble.msg_ids);
                    //~ console.log(blob.bubble.msg_timers);
                },blob.bubble.persistence));
            }
            //~ console.log(blob.bubble.msg_ids);
            //~ console.log(blob.bubble.msg_timers);
        }
    },
    
    send : function(question) {
        if (question!=''&&blob.alive){
            $.post('/blobia/', {'question':question}, function(answer){
                blob.say('<p>'+answer+'</p>');
            }, 'text');
        }
    }
    
}
