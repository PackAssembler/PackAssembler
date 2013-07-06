<%inherit file="base.mak"/>
<div class="row">
    <div class="span8">
        <h2>${title}</h2>
        <h4 class="muted">${server.owner.username}</h4>
    </div>
    <div class="span4">
    % if perm:
        <div class="btn-group pull-right" style="margin-top: 10px">
            <a href="${request.route_url('editserver', serverid=server.id)}" class="btn btn-info">Edit Server</a>
            <a href="${request.route_url('deleteserver', serverid=server.id)}" class="btn btn-danger">Delete Server</a>
        </div>
    % endif
    </div>
</div>
<hr>
<h3>Server Information</h3>
<table class="table table-hover table-bordered">
    <tr><td>Homepage</td><td>${server.url}</td></tr>
    <tr><td>Pack</td><td><a href="${request.route_url('viewpack', packid=server.build.pack.id)}">${server.build.pack.name}</a></td></tr>
    <tr><td>Pack Revision</td><td>${server.build.revision}</td></tr>
</table>