<%inherit file="base.mak"/>
<div class="row">
    <div class="span8">
        <h2>${title}</h2>
        <a href="#" class="btn btn-primary" id='showid'>Copy ID to Clipboard</a>
        <h4><a href="${request.route_url('profile', id=server.owner.id)}">${server.owner.username}</a></h4>
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
    <tr><td>Added</td><td>${server.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td></tr>
    <tr><td>Homepage</td><td>${server.url}</td></tr>
    <tr><td>Host</td><td>${server.host}</td></tr>
    <tr><td>Port</td><td>${server.port}</td></tr>
    <tr><td>Pack</td><td><a href="${request.route_url('viewpack', packid=server.build.pack.id)}">${server.build.pack.name}</a></td></tr>
    <tr><td>Pack Revision</td><td>${server.build.revision}</td></tr>
    <tr><td>Custom Config</td><td>${server.config}</td></tr>
</table>
<%block name="endscripts">
    <script type="text/javascript">
        $(document).ready(function(){
            $('#showid').click(function(){
                window.prompt("Copy to clipboard: Ctrl+C, Enter", "${server.id}");
            })
        })
    </script>
</%block>