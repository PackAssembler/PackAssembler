common =
    linkRows: !->
        do
            e <-! $ \.linked .mousedown _
            if e.which == 1
                window.location = $ this .data 'href'
            else
                w = window .open ($ this .data 'href'), '_blank'
                w.focus!
        $ \.nolink .mousedown ((e) !-> e.stopPropagation!)

    linkAutoCheck: (elemId, fieldName) !->
        $ "##{elemId}" .change (!-> $ "input[name='#{fieldName}']" .prop 'checked' @checked)

    linkStaticUrl: (packid) !->
        <-! $ '[data-id]' .click _
        window.location = "/packs/#{$ @ .data \id}/addbase?bases=#{packid}"

    linkDynamicSubmit: (selector) !->
        <-! $ '[data-id]' .click _
        form = $ selector
        form .attr \action "/packs/" + ($ @ .data \id) + "/addmod"
        form .submit!

    connectDelete: (doc) !->
        e <-! $('#delete').click
        e.preventDefault!
        url = $ @ .attr 'href'
        result <-! bootbox.confirm "Are you sure you want to delete this #{doc}?"
        if result
            window.location = url

    pyBool: (.toLowerCase! == "true")
