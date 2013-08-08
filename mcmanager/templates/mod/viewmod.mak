<%inherit file="base.mak"/>
<div class="row">
    <div class="span8">
        <h2>${title}</h2>
        <div class="btn-group">
            <a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">
                Add to Pack
                <span class="icon-caret-down"></span></a>
            <ul class="dropdown-menu">
                % if packs:
                    % for pack in packs:
                    <li><a href="${request.route_url('addpackmod', id=pack.id)}?btnSubmit&txtModID=${mod.id}">${pack.name}</a></li>
                    % endfor
                % else:
                    <li><a href="#">You have no packs!</a></li>
                % endif
                <li class="divider"></li>
                <li><a href="${request.route_url('addpack')}">Add Pack</a></li>
            </ul>
        </div>
        ## VERY BAD IDEA! Find a better way to do this. Hardcoding username -> not good.
        % if mod.owner.username == 'Orphan':
            % if user is not None and 'group:user' not in user.groups:
                <br class="bmargin"><a href="${request.route_url('adoptmod', id=mod.id)}" class="btn">Adopt</a>
            % else:
                <%block name="userlink"><h4><a href="${request.route_url('profile', id=mod.owner.id)}">${mod.owner.username}</a></h4></%block>
            % endif
        % else:
            % if perm:
                <br class="bmargin"><a href="${request.route_url('disownmod', id=mod.id)}" class="btn">Disown</a>
            % else:
                ${userlink()}
            % endif
        % endif
    </div>
    <div class="span4">
    % if perm:
        <div class="btn-group pull-right tmargin">
            <a href="${request.route_url('editmod', id=mod.id)}" class="btn btn-info">Edit Mod</a>
            <a id="delete" class="btn btn-danger">Delete Mod</a>
        </div>
    % endif
    </div>
</div>
<hr>
<h3>Mod Information</h3>
<table class="table table-hover table-bordered">
    <tr><td>Author</td><td><a href="${request.route_url('modlist')}?txtSearch=${mod.author}&btnSubmit=">${mod.author}</a></td></tr>
    <tr><td>Added</td><td>${mod.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td></tr>
    <tr><td>Mod ID</td><td>${mod.id}</td></tr>
    <tr><td>Installs to</td><td>${mod.install}</td></tr>
    <tr><td>Runs on</td><td>
    <%def name="runson(mod)">
        % if mod.target == "both":
            Server and Client
        % elif mod.target == "server":
            Server
        % elif mod.target == "client":
            Client
        % endif
    </%def>
    ${runson(mod)}
    </td></tr>
    <tr><td>Homepage</td><td>
    % if mod.url == None:
        None
    % else:
        <a href="${mod.url}">${mod.url}</a>
    % endif
    </td></tr>
    <%
        try:
            p = '<br />'.join(mod.permission.splitlines())
        except AttributeError:
            p = 'None'
    %>
    <tr><td>Permission</td><td>${p | n}</td></tr>
</table>
<h3>Versions</h3>
<div class="row bmargin relative-position">
    <div class="span8">
        <a href="${request.route_url('flagmod', id=mod.id)}" class="btn${' btn-danger' if not mod.outdated else ''}">
            <i class="icon-flag"></i> ${'Unf' if mod.outdated else 'F'}lag as Outdated
        </a>
    </div>
    % if perm:
    <div class="span4 force-bottom">
        <div class="pull-right">
            <a href="${request.route_url('addversion', id=mod.id)}"><i class="icon-plus no-decoration"></i> Add Version</a>
        </div>
    </div>
    % endif
</div>
<table class="table table-hover table-bordered">
    <thead>
        <tr><th>Version</th><th>MC Min</th><th>MC Max</th><th>Uploaded</th><th>Action</th></tr>
    </thead>
    <tbody>
    % for version in mod.versions[::-1]:
        <tr>
            <td>${version.version}</td>
            <td>${version.mc_min}</td>
            <td>${version.mc_max}</td>
            <td>${version.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td>
            <td>
                <div class="btn-group">
                    <a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">
                        Action
                        <span class="icon-caret-down"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="${request.route_url('downloadversion', id=version.id)}"><i class="icon-fixed-width icon-download"></i> Download</a></li>
                        % if perm:
                            <li><a href="${request.route_url('deleteversion', id=version.id)}"><i class="icon-fixed-width icon-trash"></i> Delete</a></li>
                            <li><a href="${request.route_url('editversion', id=version.id)}"><i class="icon-fixed-width icon-pencil"></i> Edit</a></li>
                        % endif
                    </ul>
                </div>
            </td>
        </tr>
    % endfor
    </tbody>
</table>
<%block name="endscripts">
    <script src="//github.com/makeusabrew/bootbox/releases/v3.3.0/1141/bootbox.min.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#delete').click(function(){
                bootbox.confirm("Are you sure you want to delete this mod?", function(result){
                    if (result)
                        window.location = "${request.route_url('deletemod', id=mod.id)}";
                });
            });
        });
    </script>
</%block>