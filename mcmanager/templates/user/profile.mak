<%inherit file="base.mak"/>
<div class="row">
    <div class="span6">
        <div class="profilebox">
            <div class="profilebox-avatar" id="gravatar">Loading Gravatar</div>
            <div class="profilebox-info">
                <h2>${title}</h2>
                % if admin:
                    <form method="post" action="${request.route_url('edituser', id=owner.id)}">
                        <select class="longer" id="selGroup" name="selGroup" value="">
                            <option value="user">User</option>
                            <option value="trusted">Trusted</option>
                            <option value="moderator">Moderator</option>
                            <option value="admin">Admin</option>
                        </select>
                    </form>
                % else:
                    <%
                        g = owner.groups[0].split(':')[1].title()
                        colors = {'User': '', 'Trusted': 'text-success', 'Moderator': 'text-info', 'Admin': 'text-error'}
                    %>
                    <h3 class="${colors[g]}">${g}</h3>
                % endif
            </div>
        </div>
    </div>
    <div class="span6">
    % if perm:
        <div class="btn-group pull-right tmargin">
            <a href="${request.route_url('edituser', id=owner.id)}" class="btn btn-info">Edit Account</a>
            <a href="${request.route_url('deleteuser', id=owner.id)}" class="btn btn-danger">Delete Account</a>
        </div>
    % endif
    </div>
</div>

<hr>
<h3>Mods</h3>
% if mods:
    <table class="table table-hover table-bordered" data-provides="rowlink">
    % for mod in mods:
        <tr class="${'error' if mod.outdated else ''}"><td><a href="${request.route_url('viewmod', id=mod.id)}">${mod.name}</a></td></tr>
    % endfor
    </table>
% else:
    No mods.
% endif
<h3>Packs</h3>
% if packs:
    <table class="table table-hover table-bordered" data-provides="rowlink">
    % for pack in packs:
        <tr><td><a href="${request.route_url('viewpack', id=pack.id)}">${pack.name}</a></td></tr>
    % endfor
    </table>
% else:
    No packs.
% endif
<h3>Servers</h3>
% if servers:
    <table class="table table-hover table-bordered" data-provides="rowlink">
    % for server in servers:
        <tr><td><a href="${request.route_url('viewserver', id=server.id)}">${server.name}</a></td></tr>
    % endfor
    </table>
% else:
    No servers.
% endif
<%block name="style">
    <link href="${request.static_url('mcmanager:static/css/bootstrap-rowlink.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mcmanager:static/js/bootstrap-rowlink.min.js')}"></script>
    <script src="${request.static_url('mcmanager:static/js/gravatar/md5.js')}"></script>
    <script src="${request.static_url('mcmanager:static/js/gravatar/jquery.gravatar.js')}"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#gravatar').empty().append($.gravatar('${owner.email}', {rating: 'pg', secure: true, size: 150, image: 'identicon'}));
            $('#gravatar').children(':first').addClass('img-polaroid');
            $('#selGroup').val('${owner.groups[0].split(':')[1]}');
            $('#selGroup').change(function(){
                $(this).parent().submit();
            });
        });
    </script>
</%block>
