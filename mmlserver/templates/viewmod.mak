<%inherit file="base.mak"/>
<div class="row">
    <div class="span8">
        <h2>${title}</h2>
        <h4 class="muted">${mod.owner.username}</h4>
    </div>
    <div class="span4">
    % if perm:
        <div class="btn-group pull-right" style="margin-top: 10px">
            <a href="${request.route_url('editmod', modid=mod.id)}" class="btn btn-info">Edit Mod</a>
            <a href="${request.route_url('deletemod', modid=mod.id)}" class="btn btn-danger">Delete Mod</a>
        </div>
    % endif
    </div>
</div>
<hr>
<h3>Mod Information</h3>
<table class="table table-hover table-bordered">
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
    <tr><td>Permission</td><td>${mod.permission}</td></tr>
</table>
<h3>Versions</h3>
% if perm:
    <div class="pull-right" style="margin-bottom: 10px;">
        <a href="${request.route_url('addversion', modid=mod.id)}"><i class="icon-plus" style="text-decoration: none;"></i> Add Version</a>
    </div>
% endif
<table class="table table-hover table-bordered">
    <thead>
        <tr><th>Version</th><th>MC Min</th><th>MC Max</th><th>Uploaded</th><th>Action</th></tr>
    % for version in mod.versions:
        <tr>
            <td>${version.version}</td>
            <td>${version.mc_min}</td>
            <td>${version.mc_max}</td>
            <td>${version.upload_date.strftime('%e %b %Y %I:%m:%S %p')}</td>
            <td>
                <div class="btn-group">
                    <a class="btn btn-primary" href="#">Action</a>
                    <a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">
                        <span class="icon-caret-down"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="${request.route_url('downloadversion', versionid=version.id)}"><i class="icon-fixed-width icon-download"></i> Download</a></li>
                        % if perm:
                            <li><a href="${request.route_url('deleteversion', versionid=version.id)}"><i class="icon-fixed-width icon-trash"></i> Delete</a></li>
                            <li><a href="${request.route_url('editversion', versionid=version.id)}"><i class="icon-fixed-width icon-pencil"></i> Edit</a></li>
                        % endif
                    </ul>
                </div>
            </td>
        </tr>
    % endfor
</table>