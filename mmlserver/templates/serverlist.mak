<%inherit file="base.mak"/>
<h2>${title}</h2>
<hr>
<div class="pull-right" style="margin-bottom: 10px;">
    <a href="${request.route_url('addserver')}"><i class="icon-plus" style="text-decoration: none;"></i> Add Server</a>
</div>
<table class="table table-hover table-bordered" data-provides="rowlink">
    <thead>
        <tr><th>Server</th><th>Owner</th><th>Pack</th></tr>
    </thead>
    <tbody>
    % for server in servers:
        <tr><td><a href="${request.route_url('viewserver', serverid=server.id)}">${server.name}</a></td><td>${server.owner.username}</td><td>${server.build.pack.name}</td></tr>
    % endfor
    </tbody>
</table>
<%block name="style">
    <link href="${request.static_url('mmlserver:static/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mmlserver:static/bootstrap-rowlink.min.js')}"></script>
</%block>