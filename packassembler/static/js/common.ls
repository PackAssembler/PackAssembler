linkRows = !->
    do
        e <-! $ \.linked .mousedown _
        if e.which == 1
            window.location = $ this .data 'href'
        else
            w = window .open ($ this .data 'href'), '_blank'
            w.focus!
    $ \.nolink .mousedown ((e) !-> e.stopPropagation!)

linkAutoCheck = (elemId, fieldName) !->
    $ "##{elemId}" .change (!-> $ "input[name='#{fieldName}']" .prop 'checked' @checked)


linkDynamicSubmit = (selector) !->
    <-! $ '[data-id]' .click _
    form = $ selector
    form .attr \action "/packs/#{$ @ .data \id}/addmod"
    form .submit!

module.exports =
    linkRows: linkRows,
    linkAutoCheck: linkAutoCheck,
    linkDynamicSubmit: linkDynamicSubmit
