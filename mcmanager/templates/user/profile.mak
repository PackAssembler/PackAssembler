<%inherit file="base.mak"/>
<div class="row">
    <div class="col-lg-6">
        <div class="profilebox">
            <div class="profilebox-avatar" id="gravatar">Loading Gravatar</div>
            <div class="profilebox-info">
                <h2>${title}</h2>
                % if admin:
                    <form method="post" action="${request.route_url('edituser', id=owner.id)}">
                        <select class="longer" id="group" name="group" value="">
                            <option value="user">User</option>
                            <option value="trusted">Trusted</option>
                            <option value="moderator">Moderator</option>
                            <option value="admin">Admin</option>
                        </select>
                    </form>
                % else:
                    <%
                        g = owner.groups[0].split(':')[1].title()
                        colors = {'User': '', 'Trusted': 'text-success', 'Moderator': 'text-info', 'Admin': 'text-danger'}
                    %>
                    <h3 class="${colors[g]}">${g}</h3>
                % endif
            </div>
        </div>
    </div>
    <div class="col-lg-6">
    % if perm:
        <div class="btn-group pull-right tmargin">
            <a href="${request.route_url('edituser', id=owner.id)}" class="btn btn-info">Edit Account</a>
            <a href="${request.route_url('deleteuser', id=owner.id)}" class="btn btn-danger">Delete Account</a>
        </div>
    % endif
    </div>
</div>

<hr>
<div class="row">
    ${showlist('Mods', mods)}
    ${showlist('Packs', packs)}
    ${showlist('Servers', servers)}
</div>
<%def name="showlist(heading, items)">
    <div class="col-lg-4">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h4>${heading}</h4>
            </div>
            % if items:
                <div class="list-group">
                    % for mod in mods:
                        <a href="${request.route_url('viewmod', id=mod.id)}" class="list-group-item">${mod.name}</a>
                    % endfor
                </div>
            % else:
                <div class="panel-body">
                    No ${heading.lower()}.
                </div>
            % endif
        </div>
    </div>
</%def>
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
            $('#group').val('${owner.groups[0].split(':')[1]}');
            $('#group').change(function(){
                $(this).parent().submit();
            });
        });
    </script>
</%block>
