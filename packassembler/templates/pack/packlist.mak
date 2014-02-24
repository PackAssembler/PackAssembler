<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
<div class="pull-right bmargin">
    <a href="${request.route_url('addpack')}" class="action-add"><i class="fa fa-plus no-decoration"></i> Add Pack</a>
</div>
<table class="table table-hover table-bordered listtable">
    <thead>
        <tr><th>Pack</th><th>Owner</th><th>Base</th></tr>
    </thead>
    <tbody>
    % for pack in packs:
        <tr class="linked" data-href="${request.route_url('viewpack', id=pack.id)}">
            <td>${pack.name}</td>
            <td>${pack.owner.username}</td>
            <td>${"Yes" if pack.base else "No"}</td>
        </tr>
    % endfor
    </tbody>
</table>
<small class="pull-right">${len(packs)} packs.</small>
<%block name="endscripts">
    <script src="${request.static_url('packassembler:static/js/bundled/wrapper.js')}"></script>
    <script type="text/javascript">$(document).ready(function(){common.linkRows();});</script>
</%block>
