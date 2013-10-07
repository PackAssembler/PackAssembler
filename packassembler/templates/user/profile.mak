<%inherit file="base.mak"/>
<%namespace name="extras" file="extras.mak" />
<div class="row">
    <div class="col-lg-6">
        <div class="profilebox">
            <div class="profilebox-avatar">${extras.avatar(owner, 150)}</div>
            <div class="profilebox-info">
                <h2>${title}</h2>
                % if admin:
                    <form method="post" action="${request.route_url('edituser', id=owner.id)}">
                        <select class="longer" id="group" name="group" value="">
                            <option value="user">User</option>
                            <option value="contributor">Contributor</option>
                            <option value="moderator">Moderator</option>
                            <option value="admin">Admin</option>
                        </select>
                    </form>
                % else:
                    <%
                        g = owner.group.title()
                        colors = {'User': '', 'Contributor': 'text-success', 'Moderator': 'text-info', 'Admin': 'text-danger'}
                    %>
                    <h3 class="${colors[g]}">${g}</h3>
                % endif
            </div>
        </div>
    </div>
    <div class="col-lg-6">
    % if perm:
        <div class="btn-group pull-right tmargin">
            <a href="${request.route_url('edituser', id=owner.id)}" class="btn btn-info action-edit">Edit Account</a>
            <a href="#" id="delete" class="btn btn-danger action-delete">Delete Account</a>
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
                    % for item in items:
                        <a href="${request.route_url('view' + heading.lower()[:-1], id=item.id)}" class="list-group-item">${item.name}</a>
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

<%block name="endscripts">
    <script src="//raw.github.com/makeusabrew/bootbox/master/bootbox.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#group').val('${owner.group}');
            $('#group').change(function(){
                $(this).parent().submit();
            });
            $('#delete').click(function(){
                bootbox.confirm("Are you sure you want to delete this account?", function(result){
                    if (result)
                        window.location = "${request.route_url('deleteuser', id=owner.id)}";
                });
            });
        });
    </script>
</%block>
