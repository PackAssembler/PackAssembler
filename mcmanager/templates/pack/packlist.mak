<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
<div class="pull-right bmargin">
    <a href="${request.route_url('addpack')}" class="action-add"><i class="icon-plus no-decoration"></i> Add Pack</a>
</div>
<table class="table table-hover table-bordered listtable">
    <thead>
        <tr><th>Pack</th><th>Owner</th></tr>
    </thead>
    <tbody>
    % for pack in packs:
        <tr class="linked" data-href="${request.route_url('viewpack', id=pack.id)}"><td>${pack.name}</td><td>${pack.owner.username}</td></tr>
    % endfor
    </tbody>
</table>
<%block name="endscripts">
    <script src="${request.static_url('mcmanager:static/js/rowlink.js')}"></script>
</%block>
