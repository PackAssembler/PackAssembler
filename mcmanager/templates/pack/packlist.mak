<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
<div class="pull-right bmargin">
    <a href="${request.route_url('addpack')}"><i class="icon-plus no-decoration"></i> Add Pack</a>
</div>
<table class="table table-hover table-bordered" data-provides="rowlink">
    <thead>
        <tr><th>Pack</th><th>Owner</th></tr>
    </thead>
    <tbody>
    % for pack in packs:
        <tr><td><a href="${request.route_url('viewpack', id=pack.id)}">${pack.name}</a></td><td>${pack.owner.username}</td></tr>
    % endfor
    </tbody>
</table>
<%block name="style">
    <link href="${request.static_url('mcmanager:static/css/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mcmanager:static/js/bootstrap-rowlink.min.js')}"></script>
</%block>
