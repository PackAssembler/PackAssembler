<%inherit file="base.mak"/>
<div class="row">
    <div class="span8">
        <h2>${title}</h2>
        <a href="#" class="btn btn-primary" id='showid'>Show ID</a>
        <h4 class="muted">${pack.owner.username}</h4>
    </div>
    <div class="span4">
    % if perm:
        <div class="btn-group pull-right" style="margin-top: 10px">
            <a href="${request.route_url('editpack', packid=pack.id)}" class="btn btn-info">Edit Pack</a>
            <a href="${request.route_url('deletepack', packid=pack.id)}" class="btn btn-danger">Delete Pack</a>
        </div>
    % endif
    </div>
</div>
<hr>
<h3>Builds</h3>
% if perm:
    <div class="pull-right" style="margin-bottom: 10px;">
        <a href="${request.route_url('addbuild', packid=pack.id)}"><i class="icon-plus" style="text-decoration: none;"></i> New Build</a>
    </div>
% endif
<table class="table table-hover table-bordered">
    <thead>
    <tr><th>Revision</th><th>Build Date</th><th>Config</th><th>Minecraft Version</th><th>Forge Version</th><th>Action</th></tr>
    </thead>
    <tbody>
    % for build in pack.builds[::-1]:
        <tr>
            <td>${build.revision}</td>
            <td>${build.build_date.strftime('%e %b %Y %I:%m:%S %p')}</td>
            <td><a href="${build.config}">${build.config}</a></td>
            <td>${build.mc_version}</td>
            <td>${build.forge_version}</td>
            <td>
                <div class="btn-group">
                    <a class="btn btn-primary" href="#">Action</a>
                    <a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">
                        <span class="icon-caret-down"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="${request.route_url('getbuild', buildid=build.id)}"><i class="icon-fixed-width icon-download"></i> JSON</a></li>
                        % if perm:
                            <li><a href="${request.route_url('removebuild', buildid=build.id)}"><i class="icon-fixed-width icon-trash"></i> Delete</a></li>
                        % endif
                    </ul>
                </div>
            </td>
        </tr>
    % endfor
    </tbody>
</table>
<h3>Mods</h3>
% if pack.mods:
    <ul>
    % for mod in pack.mods:
        <li><a href="${request.route_url('viewmod', modid=mod.id)}">${mod.name}</a> 
        % if perm:
            <a href="${request.route_url('removepackmod', modid=mod.id, packid=pack.id)}"><i class="icon-remove text-error"></i></a>
        % endif
        </li>
    % endfor
    </ul>
% else:
    No Mods Yet!
% endif
% if perm:
    <div style="margin-top: 11px">
        <a href="${request.route_url('addpackmod', packid=pack.id)}"><i class="icon-plus" style="text-decoration: none;"></i> Add Mod to Pack</a>
    </div>
% endif
<%block name="endscripts">
    <script type="text/javascript">
        $(document).ready(function(){
            $('#showid').click(function(){
                $(this).replaceWith("${pack.id}")
            })
        })
    </script>
</%block>