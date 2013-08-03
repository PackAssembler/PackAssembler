<%inherit file="base.mak"/>
<div class="row">
    <div class="span2" id="gravatar">Loading Gravatar</div>
    <div class="span6"><h2 style="line-height: 140px">${title}</h2></div>
    <div class="span4">
    % if perm:
        <div class="btn-group pull-right" style="margin-top: 10px">
            <a href="${request.route_url('edituser', userid=owner.id)}" class="btn btn-info">Edit Account</a>
            <a href="${request.route_url('deleteuser', userid=owner.id)}" class="btn btn-danger">Delete Account</a>
        </div>
    % endif
    </div>
</div>
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
    <link href="${request.static_url('mcmanager:static/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mcmanager:static/bootstrap-rowlink.min.js')}"></script>
    <script src="${request.static_url('mcmanager:static/gravatar/md5.js')}"></script>
    <script src="${request.static_url('mcmanager:static/gravatar/jquery.gravatar.js')}"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#gravatar').empty().append($.gravatar('${owner.email}', {rating: 'pg', secure: true, size: 150, image: 'identicon'}));
            $('#gravatar').children(':first').addClass('img-polaroid');
        });
    </script>
</%block>
