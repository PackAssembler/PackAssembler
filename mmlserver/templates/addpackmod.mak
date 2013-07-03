<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row"><div class="span10">
    <form class="form-horizontal" method="post" action="${request.url}" novalidate="novalidate" id="add-pack-mod">
        ${form.formerror(error)}
        ${form.horfield('txtModID', 'Mod ID', 'text', attr={
            'data-regexp': '^[0-9a-f]{24}$',
            'autofocus': 'autofocus',
            'required': 'required'
        })}
        ${form.horsubmit(request.route_url('viewpack', packid=request.matchdict['packid']))}
    </form>
</div></div>
<%block name="style">
    ${form.formstyle()}
</%block>
<%block name="endscripts">
    ${form.formscripts('add-pack-mod')}
</%block>