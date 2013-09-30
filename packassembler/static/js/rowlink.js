function loc(url, newtab){
    if (newtab){
        var win = window.open(url, '_blank');
        win.focus();
    }
    else{
        window.location = url;
    }
}

$(document).ready(function(){
    $('.linked-tab').click(function(){
        loc($(this).data('href'), true);
    });
    $('.linked').click(function(){
        loc($(this).data('href'), false);
    });
    $('.nolink').click(function(e){
        e.stopPropagation();
    });
});