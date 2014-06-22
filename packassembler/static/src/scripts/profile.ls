<-! $
$('#group').change !->
    $ @ .parent!submit!
$('#delete').click !->
    url = $ @ .data 'url'
    result <-! bootbox.confirm "Are you sure you want to delete this account?"
    if result
        window.location = url
