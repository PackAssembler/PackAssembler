<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
<%namespace name="extras" file="extras.mak" />
${listcommon.head()}
<hr>
${extras.flash()}
<div class="pull-right bmargin">
    <a href="${request.route_url('addserver')}"><i class="fa fa-plus no-decoration"></i> Add Server</a>
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
    <script src="${request.static_url('packassembler:static/js/bundled/wrapper.js')}"></script>
    <script type="text/javascript">$(document).ready(function(){common.linkRows();});</script>
</%block>
