<%inherit file="base.mak"/>
<%namespace name="extras" file="extras.mak" />
<div class="row bpadding infobar">
    <div class="col-lg-8">
        <h2>${title}</h2>
    % if server.build:
        <a href="#" class="btn btn-primary btn-sm" id='showurl'>Copy MCUpdater URL</a>
    % endif
        <a href="#" class="btn btn-primary btn-sm" id='showid'>Copy ID to Clipboard</a>
        <h4><a href="${request.route_url('profile', id=server.owner.id)}">${server.owner.username}</a></h4>
    </div>
    <div class="col-lg-4">
    % if perm:
        <div class="btn-group pull-right tmargin">
            <a href="${request.route_url('editserver', id=server.id)}" class="btn btn-info action-edit">Edit Server</a>
            <a id="delete" class="btn btn-danger action-delete">Delete Server</a>
        </div>
    % endif
    </div>
</div>
% if perm:
    <div class="row pull-right">
        <a href="${request.route_url('editserverbanner', id=server.id)}" id="changeBanner">Change Banner</a>
    </div>
% endif
<hr>
<div class="row">
    <div class="col-lg-6">
        <div class="panel panel-default">
            <div class="panel-heading">Details</div>
            <table class="table">
                <tr>
                    <td>Homepage</td>
                    <td>
                        % if server.url:
                            <a rel="nofollow" href="${server.url}">${server.url}</a>
                        % else:
                            None
                        % endif
                    </td>
                </tr>
                <tr><td>Date Added</td><td>${server.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td></tr>
                <tr><td>Host</td><td>${server.host}</td></tr>
                <tr><td>Port</td><td>${server.port}</td></tr>
                <tr><td>Custom Config</td><td>${server.config}</td></tr>
            </table>
        </div>
    </div>
    <div class="col-lg-6">
        <div class="panel panel-default">
            <div class="panel-heading">Pack Build</div>
        % if server.build:
            <table class="table">
                <tr><td>Pack</td><td><a href="${request.route_url('viewpack', id=server.build.pack.id)}">${server.build.pack.name}</a></td></tr>
                <tr><td>Pack Revision</td><td>${server.build.revision}</td></tr>
                <tr><td>Minecraft Version</td><td>${server.build.mc_version}</td></tr>
                <tr><td>Forge Version</td><td>${server.build.forge_version}</td></tr>
            </table>
        % else:
            <div class="panel-body">No pack build associated with this server yet.</div>
        % endif
        </div>
    </div>
</div>
<%block name="style">
    ${extras.banner_style(server)}
</%block>
<%block name="endscripts">
    <script src="//rawgithub.com/makeusabrew/bootbox/master/bootbox.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#delete').click(function(){
                bootbox.confirm("Are you sure you want to delete this server?", function(result){
                    if (result)
                        window.location = "${request.route_url('deleteserver', id=server.id)}";
                });
            });
            $('#showid').click(function(){
                window.prompt("Copy to clipboard: Ctrl+C, Enter", "${server.id}");
            });
            $('#showurl').click(function(){
                window.prompt("Copy to clipboard: Ctrl+C, Enter", "${request.route_url('mcuxmlserver', id=server.id)}");
            });
        });
    </script>
</%block>