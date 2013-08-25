<%inherit file="base.mak"/>
<div class="row">
    <div class="col-lg-8">
        <h2>${title}</h2>
        <a href="#" class="btn btn-primary" id='showid'>Copy ID to Clipboard</a>
        <h4><a href="${request.route_url('profile', id=pack.owner.id)}">${pack.owner.username}</a></h4>
    </div>
    <div class="col-lg-4">
    % if perm:
        <div class="btn-group pull-right tmargin">
            <a href="${request.route_url('editpack', id=pack.id)}" class="btn btn-info">Edit Pack</a>
            <a id="delete" class="btn btn-danger">Delete Pack</a>
        </div>
    % endif
    </div>
</div>
<hr>
<h3>Builds</h3>
% if perm:
    <div class="pull-right bmargin">
        <a href="${request.route_url('addbuild', id=pack.id)}"><i class="icon-plus no-decoration"></i> New Build</a>
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
            <td>${build.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td>
            <td><a href="${build.config}">${build.config}</a></td>
            <td>${build.mc_version}</td>
            <td>${build.forge_version}</td>
            <td>
                <div class="btn-group">
                    <a class="btn btn-primary" href="#">Action</a>
                    <a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">
                        <span class="icon-caret-down"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="${request.route_url('downloadbuild', id=build.id)}"><i class="icon-fixed-width icon-download"></i> JSON</a></li>
                        % if perm:
                            <li><a href="${request.route_url('removebuild', id=build.id)}"><i class="icon-fixed-width icon-trash"></i> Delete</a></li>
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
    % for mod in sorted(pack.mods):
        <li><a href="${request.route_url('viewmod', id=mod.id)}">${mod.name}</a> 
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
    <div class="tmargin">
        <a href="${request.route_url('addpackmod', id=pack.id)}"><i class="icon-plus no-decoration"></i> Add Mod to Pack</a>
    </div>
% endif
<%block name="endscripts">
    <script type="text/javascript">
        $(document).ready(function(){
            $('#showid').click(function(){
                window.prompt("Copy to clipboard: Ctrl+C, Enter", "${pack.id}");
            })
        })
    </script>
    <script src="//raw.github.com/makeusabrew/bootbox/master/bootbox.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#delete').click(function(){
                bootbox.confirm("Are you sure you want to delete this pack?", function(result){
                    if (result)
                        window.location = "${request.route_url('deletepack', id=pack.id)}";
                });
            });
        });
    </script>
</%block>