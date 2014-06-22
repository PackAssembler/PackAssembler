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
                        <select class="longer" id="group" name="group">
                        % for group_name in ['user', 'contributor', 'moderator', 'admin']:
                            <option value="${group_name}" ${g.show_if('selected', owner.group == group_name)}>${group_name.capitalize()}</option>
                        % endfor
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
                <a href="${request.route_url('deleteuser', id=owner.id)}" id="delete" class="btn btn-danger">Delete Account</a>
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
    <script src="${request.static_url('packassembler:static/dist/js/lib/bootbox.min.js')}"></script>
    <script src="${request.static_url('packassembler:static/dist/js/profile.js')}"></script>
</%block>
