<-! $
common.linkRows!
common.linkAutoCheck \topcheck \mods
common.linkDynamicSubmit \form

$('#version-dropdown').css \display \inline-block
$('#version-dropdown > ul > li > a').click(!->
    val = $(this).html!
    mcv_hidden = $('input[name="mc_version"]')
    mcv_hidden.attr \value val
    if common.pyBool mcv_hidden.data \outdated
        $('<input />').attr \type \hidden
                       .attr \name \outdated
                       .appendTo \#search-form
    $('#search-form').submit!
)
