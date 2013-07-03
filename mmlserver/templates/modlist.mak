<%inherit file="base.mak"/>
<%namespace name="view" file="viewmod.mak" />
<h2>${title}</h2>
<hr>
<div class="pull-right" style="margin-bottom: 10px;">
    <a href="${request.route_url('addmod')}"><i class="icon-plus" style="text-decoration: none;"></i> Add Mod</a>
</div>
<table class="table table-hover table-bordered" data-provides="rowlink">
    <thead>
        <tr><th>Name</th><th>Owner</th><th>Target</th></tr>
    </thead>
    <tbody>
    % for mod in mods:
        <tr><td><a href="${request.route_url('viewmod', modid=mod.id)}">${mod.name}</a></td><td>${mod.owner.username}</td><td>${view.runson(mod)}</td></tr>
    % endfor
    </tbody>
</table>
<%block name="style">
    <link href="${request.static_url('mmlserver:static/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mmlserver:static/bootstrap-rowlink.min.js')}"></script>
</%block>
