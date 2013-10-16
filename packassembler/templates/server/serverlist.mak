<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
<div class="pull-right bmargin">
    <a href="${request.route_url('addserver')}" class="action-add"><i class="icon-plus no-decoration"></i> Add Server</a>
</div>
<table class="table table-hover table-bordered listtable" data-provides="rowlink">
    <thead>
        <tr><th>Server</th><th>Owner</th><th>Pack</th></tr>
    </thead>
    <tbody>
    % for server in servers:
        <tr class="linked" data-href="${request.route_url('viewserver', id=server.id)}">
        <td>${server.name}</td>
        <td>${server.owner.username}</td>
        <td>${server.build.pack.name if server.build else None}</td>
    </tr>
    % endfor
    </tbody>
</table>
<small class="pull-right">${len(servers)} servers.</small>
<%block name="endscripts">
    <script src="${request.static_url('packassembler:static/js/rowlink.js')}"></script>
</%block>
