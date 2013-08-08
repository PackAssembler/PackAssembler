<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
<div class="pull-right bmargin">
    <a href="${request.route_url('addserver')}"><i class="icon-plus no-decoration"></i> Add Server</a>
</div>
<table class="table table-hover table-bordered" data-provides="rowlink">
    <thead>
        <tr><th>Server</th><th>Owner</th><th>Pack</th></tr>
    </thead>
    <tbody>
    % for server in servers:
        <tr><td><a href="${request.route_url('viewserver', id=server.id)}">${server.name}</a></td><td>${server.owner.username}</td><td>${server.build.pack.name}</td></tr>
    % endfor
    </tbody>
</table>
<%block name="style">
    <link href="${request.static_url('mcmanager:static/css/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mcmanager:static/js/bootstrap-rowlink.min.js')}"></script>
</%block>
