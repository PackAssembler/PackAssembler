<%inherit file="base.mak"/>
<%!
    import re
    def linejoin(text):
        try:
            return '<br />'.join(text.splitlines())
        except AttributeError:
            return 'None'

    def externallink(text):
        trun = text[:35] + (text[35:] and '...')
        return '<a href="{0}" target="_blank" rel="nofollow">{1}</a>'.format(text, trun)

    def autolink(text):
        urlre = re.compile("(\(?https?://[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|])(\">|</a>)?")
        try:
            return urlre.sub(lambda m: externallink(m.group(0)), text)
        except TypeError:
            return 'None'
%>
<div class="row bpadding" id="modInfobar">
    <div class="col-lg-8">
        <h2>${title}</h2>
        <div class="dropdown inline">
            <a class="btn btn-primary btn-sm dropdown-toggle" data-toggle="dropdown" href="#">
                Add to Pack
                <span class="icon-caret-down"></span>
            </a>
            <ul class="dropdown-menu">
                % if packs:
                    % for pack in packs:
                    <li><a href="${request.route_url('addpackmod', id=pack.id)}?id=${mod.id}">${pack.name}</a></li>
                    % endfor
                % else:
                    <li><a href="#">You have no packs!</a></li>
                % endif
                <li class="divider"></li>
                <li><a href="${request.route_url('addpack')}">Add Pack</a></li>
            </ul>
        </div>
        % if mod.owner.group == 'orphan':
            % if user is not None and user.group != 'user':
                <a href="${request.route_url('adoptmod', id=mod.id)}" class="btn btn-default btn-sm">Adopt</a>
            % else:
                <%block name="userlink"><h4><a href="${request.route_url('profile', id=mod.owner.id)}">${mod.owner.username}</a></h4></%block>
            % endif
        % else:
            % if perm:
                <a href="${request.route_url('disownmod', id=mod.id)}" class="btn btn-default btn-sm">Disown</a>
            % endif
            ${userlink()}
        % endif
    </div>
    <div class="col-lg-4">
    % if perm:
        <div class="btn-group pull-right tmargin">
            <a href="${request.route_url('editmod', id=mod.id)}" class="btn btn-info action-edit">Edit Mod</a>
            <a id="delete" class="btn btn-danger action-delete">Delete Mod</a>
        </div>
    % endif
    </div>
</div>
% if perm:
    <div class="row pull-right">
        <a href="${request.route_url('editbanner', id=mod.id)}" id="changeBanner">Change Banner</a>
    </div>
% endif
<hr>
<div class="row">
    <div class="col-lg-4">
        <div class="panel panel-default">
            <div class="panel-heading">Details</div>
            <table class="table">
                <tr><td>Author</td><td><a href="${request.route_url('modlist')}?q=${mod.author}">${mod.author}</a></td></tr>
                <tr><td>Homepage</td><td>
                % if mod.url:
                    ${mod.url | externallink}
                % else:
                    None
                % endif
                </td></tr>
                <tr><td>Date Added</td><td>${mod.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td></tr>
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
            </table>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="panel panel-default">
            <div class="panel-heading">Description</div>
            <div class="panel-body">${mod.description | autolink,linejoin,n}</div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="panel-group">
            <div class="panel panel-default">
                <div class="panel-heading">Mods by ${mod.author}</div>
                <div class="list-group">
                % for m in by_author:
                    <a href="${request.route_url('viewmod', id=m.id)}" class="list-group-item">${m.name}</a>
                % endfor
                </div>
            </div>
            <div class="panel panel-default">
                <div class="panel-heading">Packs with ${mod.name}</div>
                <div class="list-group">
                % for p in with_mod:
                    <a href="${request.route_url('viewpack', id=p.id)}" class="list-group-item">${p.name}</a>
                % endfor
                </div>
            </div>
        </div>
    </div>
</div>
<br>
<h3>Versions</h3>
<div class="row bmargin relative-position">
    <div class="col-lg-8">
        <a href="${request.route_url('flagmod', id=mod.id)}" class="action-flag btn ${'btn-danger' if not mod.outdated else 'btn-default'}" id="flag">
            <i class="icon-flag"></i> <span>${'Unf' if mod.outdated else 'F'}</span>lag as Outdated
        </a>
    </div>
    % if perm:
    <div class="col-lg-4 force-bottom">
        <div class="pull-right">
            <a href="${request.route_url('addversion', id=mod.id)}" class="action-add"><i class="icon-plus no-decoration"></i> Add Version</a>
        </div>
    </div>
    % endif
</div>
<div class="table-responsive">
    <table class="table table-hover table-bordered">
        <thead>
            <tr><th>Version</th><th>Devel</th><th>MC Min</th><th>MC Max</th><th>Uploaded</th><th>MD5</th><th>Action</th></tr>
        </thead>
        <tbody>
        % for version in mod.versions[::-1]:
            <tr class="button-height">
                <td>${version.version}</td>
                <td>${version.devel}</td>
                <td>${version.mc_min}</td>
                <td>${version.mc_max}</td>
                <td>${version.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td>
                <td>${version.mod_file.md5 if version.mod_file else version.mod_file_url_md5}</td>
                ##<td>&nbsp;</td>
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
</div>
<small>Permission: ${mod.permission | autolink,linejoin,n}</small>
<%block name="style">
    <style type="text/css">
    % if mod.banner:
        div#modInfobar
        {
            background: url("${mod.banner.image}") no-repeat scroll left;
            background-size: cover;
            color: ${mod.banner.text_color};
            background-width: 100%;
        }
    % endif
    </style>
</%block>
<%block name="endscripts">
    <script src="//raw.github.com/makeusabrew/bootbox/master/bootbox.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#delete').click(function(){
                bootbox.confirm("Are you sure you want to delete this mod?", function(result){
                    if (result)
                        window.location = "${request.route_url('deletemod', id=mod.id)}";
                });
            });
            $('#flag').click(function(e){
                e.preventDefault();
                var $flag = $(this)

                $.get($(this).attr('href'), function(data){
                    if (data['success'] === true) {
                        $flag.toggleClass('btn-default');
                        $flag.toggleClass('btn-danger');
                        if (data['outdated'] === true) {
                            $flag.children().last().html('Unf');
                        }
                        else {
                            $flag.children().last().html('F');
                        }
                    }
                    else{
                        window.location = $flag.attr('href');
                    }
                }, 'json');
            });
        });
    </script>
</%block>
