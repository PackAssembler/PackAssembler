<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
<%namespace name="extras" file="extras.mak" />
<div class="row bpadding infobar">
    <div class="col-lg-8">
        <h2>${title}</h2>
        <a href="#" class="btn btn-primary btn-sm" id='showurl'>Copy MCUpdater URL</a>
        <a href="#" class="btn btn-primary btn-sm" id='showid'>Copy ID to Clipboard</a>
        <a href="${request.route_url('clonepack', id=pack.id)}" class='btn btn-default btn-sm'>Clone</a>
        <h4><a href="${request.route_url('profile', id=pack.owner.id)}">${pack.owner.username}</a></h4>
    </div>
    <div class="col-lg-4">
    % if perm:
        <div class="btn-group pull-right tmargin">
            <a href="${request.route_url('editpack', id=pack.id)}" class="btn btn-info action-edit">Edit Pack</a>
            <a id="delete" class="btn btn-danger action-delete">Delete Pack</a>
        </div>
    % endif
    </div>
</div>
% if perm:
    <div class="row pull-right">
        <a href="${request.route_url('editpackbanner', id=pack.id)}" id="changeBanner">Change Banner</a>
    </div>
% endif
<hr>
<h3>Builds</h3>
% if perm:
    <div class="pull-right bmargin">
        <a href="${request.route_url('addbuild', id=pack.id)}" class="action-add"><i class="icon-plus no-decoration"></i> New Build</a>
    </div>
% endif
<table class="table table-hover table-bordered">
    <thead>
    <tr><th>Revision</th><th>Build Date</th><th>Config</th><th>Minecraft Version</th><th>Forge Version</th><th>Action</th></tr>
    </thead>
    <tbody>
    % for build in pack.builds[::-1]:
        <tr class="button-height">
            <td>${build.revision}</td>
            <td>${build.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td>
            <td><a href="${build.config}">${build.config}</a></td>
            <td>${build.mc_version}</td>
            <td>${build.forge_version}</td>
            <td>
                <div class="btn-group">
                    <a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">
                        Action
                        <span class="icon-caret-down"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="${request.route_url('downloadbuild', id=build.id)}"><i class="icon-fixed-width icon-download"></i> JSON</a></li>
                        <li><a href="${request.route_url('mcuxml', id=build.id)}"><i class="icon-fixed-width icon-file-text"></i> MCU XML</a></li>
                        % if perm:
                            <li><a href="${request.route_url('deletebuild', id=build.id)}"><i class="icon-fixed-width icon-trash"></i> Delete</a></li>
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
    <div class="bmargin dropdown">
        ${listcommon.add_to_pack(packs, message='Add To Pack')}${'<a href="#" id="deleteSel" class="btn btn-sm btn-danger">Delete Selected</a>' if perm else '' | n}
    </div>
    <form method="POST" action="${request.route_url('removepackmod', id=pack.id)}">
        <table class="table table-bordered table-hover">
            <thead>
                <tr>
                    <th class="center"><input type="checkbox" id="topcheck"></th>
                    <th>Mod</th>
                </tr>
            </thead>
            <tbody>
            % for mod in sorted(pack.mods):
                <tr>
                    <td class="center nolink">
                        <input type="checkbox" name="mods" value="${mod.id}">
                    </td>
                    <td data-href="${request.route_url('viewmod', id=mod.id)}" class="linked giant">
                        ${mod.name}
                    </td>
                </tr>
            % endfor
            </tbody>
        </table>
    </form>
    <small class="pull-right">${len(pack.mods)} mods.</small>
% else:
    No Mods Yet!
% endif
<%block name="style">
    ${extras.banner_style(pack)}
</%block>
<%block name="endscripts">
    <script src="//rawgithub.com/makeusabrew/bootbox/master/bootbox.js"></script>
    <script src="${request.static_url('packassembler:static/js/bundled/wrapper.js')}"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            common.linkRows();
        % if pack.mods:
            common.linkAutoCheck('topcheck', 'mods');
            common.linkDynamicSubmit('form');
            $('#deleteSel').click(function(){
                $('form').attr('action', '${request.route_url("removepackmod", id=pack.id)}');
                $('form').submit();
            })
        % endif
            $('#delete').click(function(){
                bootbox.confirm("Are you sure you want to delete this pack?", function(result){
                    if (result)
                        window.location = "${request.route_url('deletepack', id=pack.id)}";
                });
            });
            $('#showid').click(function(){
                window.prompt("Copy to clipboard: Ctrl+C, Enter", "${pack.id}");
            });
            $('#showurl').click(function(){
                window.prompt("Copy to clipboard: Ctrl+C, Enter", "${request.route_url('mcuxmlpack', id=pack.id)}");
            });
        });
    </script>
</%block>
