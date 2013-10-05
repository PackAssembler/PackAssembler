$(document).ready(function(){
    $('.linked').click(function(){
        window.location = $(this).data('href');
    });
    $('.nolink').click(function(e){
        e.stopPropagation();
    });
});