<%inherit file="base.mak"/>
<h2>${title}</h2>
<hr>
<h3>Mods</h3>
% if mods:
    <table class="table table-hover table-bordered" data-provides="rowlink">
    % for mod in mods:
        <tr><td><a href="${request.route_url('viewmod', modid=mod.id)}">${mod.name}</a></td></tr>
    % endfor
    </table>
% else:
    No mods.
% endif
<h3>Packs</h3>
% if packs:
    <table class="table table-hover table-bordered" data-provides="rowlink">
    % for pack in packs:
        <tr><td><a href="${request.route_url('viewpack', packid=pack.id)}">${pack.name}</a></td></tr>
    % endfor
    </table>
% else:
    No packs.
% endif
<h3>Servers</h3>
% if servers:
    <table class="table table-hover table-bordered" data-provides="rowlink">
    % for server in servers:
        <tr><td><a href="${request.route_url('viewserver', serverid=server.id)}">${server.name}</a></td></tr>
    % endfor
    </table>
% else:
    No servers.
% endif
<%block name="style">
    <link href="${request.static_url('mmlserver:static/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mmlserver:static/bootstrap-rowlink.min.js')}"></script>
</%block>