$(function(){
    $('#js-sponsor').click(function (){
            var $this =$(this);
            $this.next().slideToggle();
        }
    );

     $('#js-sidebar-btn').on('click', function (e) {
        var $musk = $('#sidebar-musk');
        var $sideBar = $('.widget');

        if ($musk.length === 0) {
            // Musk does not exist, create it.
            $musk = $('<div></div>')
                .addClass('musk')
                .attr('id', 'sidebar-musk')
                .css('z-index', 1)
                .appendTo('body')
                .click(function () {
                    $(this).fadeOut(500);
                    $sideBar.animate({'left': '-60%'}, 500);
                });
        }
        $sideBar.animate({'left': 0}, 500);
        $musk.fadeIn(500);
        return false;
    });

     $(window).scroll(function(){
        var top=$(window).scrollTop();
        var navbar = $(".navbar-style");

        if(top==0){
            navbar.removeClass("navbar-down");
        } else {
           navbar.addClass("navbar-down");
        }

        if( top>100 ) {
            $("#scrolltop").fadeIn();
        }else{
            $("#scrolltop").fadeOut();
        }
     });
     $("#scrolltop").click(function(){
        $("html,body").animate({scrollTop:0});
     });
});
