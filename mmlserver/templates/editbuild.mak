<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row"><div class="span10">
    <form class="form-horizontal" method="post" action="${request.url}" novalidate="novalidate" data-persist="garlic" data-destroy="false" id="edit-build">
        ${form.formerror(error)}
        ${form.mcselect('selMCVersion', 'Minecraft Version')}
        ${form.forgefield('txtForgeVersion', 'Forge Version', required=True)}
        ${form.horfield('txtConfig', 'Config', 'text', attr={
            'data-type': 'url'
        })}
        ${form.horsubmit(request.route_url('viewpack', packid=request.matchdict['packid']))}
    </form>
</div></div>
<%block name="style">
    ${form.formstyle()}
</%block>
<%block name="endscripts">
    ${form.formscripts('edit-build', include_garlic=True)}
</%block>