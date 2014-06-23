<-! $
common.linkRows!
common.linkDynamicSubmit \form
common.connectDelete \mod

$ '.details' .click (e) !->
  e.preventDefault!
  $ '#details-modal-content' .load ($ @ .attr 'href')
  $ '#details-modal' .modal!

$ '#flag' .click (e) !->
  e.preventDefault!
  $flag = $ @
  $.get ($ @ .attr 'href'), ((data) ->
    if data.success
      $flag.toggleClass 'btn-default'
      $flag.toggleClass 'btn-danger'
      if data.outdated then $flag.children!.last!.html 'Unf' else $flag.children!.last!.html 'F'
    else
      window.location = $flag.attr 'href'), 'json'
