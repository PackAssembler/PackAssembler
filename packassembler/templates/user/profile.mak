<%inherit file="base.mak"/>
<%namespace name="extras" file="extras.mak" />
<%namespace name="g" module="packassembler.template_helpers.general" />
<div class="row">
    <div class="col-lg-6">
        <div class="profilebox">
            <div class="profilebox-avatar">${extras.avatar(owner, 150)}</div>
            <div class="profilebox-info">
                <h2>${title}</h2>
                % if owner.last_login:
                    <p>Last Login: ${owner.last_login.strftime('%e %b %Y %I:%m:%S %p')}</p>
                % endif
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
                    ${extras.show_group('h3', owner)}
                % endif
            </div>
        </div>
    </div>
    <div class="col-lg-6">
        <div class="btn-group pull-right tmargin">
            <a href="${request.route_url('emailuser', id=owner.id)}" class="btn btn-default">Send Message</a>
            % if perm:
                <a href="${request.route_url('edituser', id=owner.id)}" class="btn btn-info">Edit Account</a>
                <a href="#" id="delete" class="btn btn-danger">Delete Account</a>
            % endif
        </div>
    </div>
</div>

<hr>
<div class="row">
    <% lg = owner.group == 'user' %>
    % if not lg:
        ${showlist('Mods', mods, lg)}
    % endif
    ${showlist('Packs', packs, lg)}
    ${showlist('Servers', servers, lg)}
</div>

<%def name="showlist(heading, items, lg)">
    <div class="col-lg-${'6' if lg else '4'}">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h4>${heading}</h4>
            </div>
            % if items:
                <div class="list-group">
                    % for item in items:
                        <a href="${request.route_url('view' + heading.lower()[:-1], id=item.id)}"
                           class="list-group-item ${g.show_if('list-group-item-danger', item.__class__.__name__ == 'Mod' and item.outdated)}">${item.name}</a>
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
    <script src="//rawgithub.com/makeusabrew/bootbox/master/bootbox.js"></script>
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
