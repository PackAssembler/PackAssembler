<%inherit file="base.mak"/>
<h2>${title}</h2>
<hr>
<div class="pull-right" style="margin-bottom: 10px;">
    <a href="${request.route_url('addpack')}"><i class="icon-plus" style="text-decoration: none;"></i> Add Pack</a>
</div>
<table class="table table-hover table-bordered" data-provides="rowlink">
    <thead>
        <tr><th>Pack</th><th>Owner</th></tr>
    </thead>
    <tbody>
    % for pack in packs:
        <tr><td><a href="${request.route_url('viewpack', packid=pack.id)}">${pack.name}</a></td><td>${pack.owner.username}</td></tr>
    % endfor
    </tbody>
</table>
<%block name="style">
    <link href="${request.static_url('mmlserver:static/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mmlserver:static/bootstrap-rowlink.min.js')}"></script>
</%block>