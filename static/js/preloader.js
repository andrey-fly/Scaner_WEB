$(window).on('load', function(e){
    setTimeout(function(){
      $('.loader').fadeOut(500, function(){
        $(this).css('display', 'none');
      });
    }, 750);
});
