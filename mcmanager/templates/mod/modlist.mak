<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
<div class="pull-right bmargin">
    <a href="${request.route_url('addmod')}"><i class="icon-plus no-decoration"></i> Add Mod</a>
</div>
<table class="table table-hover table-bordered" data-provides="rowlink">
    <thead>
        <tr><th>Name</th><th>Author</th><th>Owner</th></tr>
    </thead>
    <tbody>
    % for mod in mods:
        <tr class="${'danger' if mod.outdated else ''}"><td><a href="${request.route_url('viewmod', id=mod.id)}">${mod.name}</a></td><td>${mod.author}<td>${mod.owner.username}</td></tr>
    % endfor
    </tbody>
</table>
<small class="pull-right">${len(mods.filter(outdated=True))} flagged mods.</small>
<%block name="style">
    <link href="${request.static_url('mcmanager:static/css/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mcmanager:static/js/bootstrap-rowlink.min.js')}"></script>
</%block>
