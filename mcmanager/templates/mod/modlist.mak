<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
<div class="pull-right" style="margin-bottom: 10px;">
    <a href="${request.route_url('addmod')}"><i class="icon-plus" style="text-decoration: none;"></i> Add Mod</a>
</div>
<table class="table table-hover table-bordered" data-provides="rowlink">
    <thead>
        <tr><th>Name</th><th>Author</th><th>Owner</th></tr>
    </thead>
    <tbody>
    % for mod in mods:
        <tr><td><a href="${request.route_url('viewmod', id=mod.id)}">${mod.name}</a></td><td>${mod.author}<td>${mod.owner.username}</td></tr>
    % endfor
    </tbody>
</table>
<%block name="style">
    <link href="${request.static_url('mcmanager:static/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mcmanager:static/bootstrap-rowlink.min.js')}"></script>
</%block>
