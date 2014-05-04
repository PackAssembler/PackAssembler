<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
<%namespace name="extras" file="extras.mak" />
<%!
    from packassembler.template_helpers.filters import autolink, linejoin, externallink
%>
<div class="row bpadding infobar">
    <div class="col-lg-8">
        <h2>${title}</h2>
        <div class="dropdown inline">
            <form method="POST">
                <input type="hidden" name="mods" value="${mod.id}">
            </form>
            ${listcommon.add_to_pack(packs)}
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
            <a href="${request.route_url('editmod', id=mod.id)}" class="btn btn-info">Edit Mod</a>
            <a id="delete" class="btn btn-danger">Delete Mod</a>
        </div>
    % endif
    </div>
</div>
% if perm:
    <div class="row pull-right">
        <a href="${request.route_url('editmodbanner', id=mod.id)}" id="changeBanner">Change Banner</a>
    </div>
% endif
<hr>
<div class="row">
    <div class="col-lg-12">
        ${extras.flash()}
    </div>
</div>
<div class="row">
    <div class="col-lg-4">
        <div class="panel panel-default">
            <div class="panel-heading"><h4 class="panel-title">Details</div></h4>
            <table class="table">
                <tr><td>Author</td><td><a href="${request.route_url('modlist')}?q=${mod.author}" rel="nofollow">${mod.author}</a></td></tr>
                <tr><td>Homepage</td><td>
                % if mod.url:
                    ${mod.url | externallink}
                % else:
                    None
                % endif
                </td></tr>
                <tr><td>Permission</td><td>${mod.permission | autolink,linejoin,n}</td></tr>
            % if mod.donate:
                <tr><td>Donate</td><td>${mod.donate | externallink}</td></tr>
            % endif
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
            <div class="panel-heading"><h4 class="panel-title">Description</div></h4>
            <div class="panel-body">${mod.description | autolink,linejoin,n}</div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="panel-group" id="reference-accordion">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title"><a data-toggle="collapse" data-parent="#reference-accordion" href="#mods-by-panel">
                            Mods by ${mod.author}</div>
                        </a></h4>
                <div class="collapse panel-collapse in" id="mods-by-panel">
                    <div class="list-group">
                    % for m in by_author:
                        <a href="${request.route_url('viewmod', id=m.id)}" class="list-group-item">${m.name}</a>
                    % endfor
                    </div>
                </div>
            </div>
        % if with_mod:
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title"><a data-toggle="collapse" data-parent="#reference-accordion" href="#packs-with-panel">
                        Packs with ${mod.name}
                    </a></h4>
                </div>
                <div class="collapse panel-collapse" id="packs-with-panel">
                    <div class="list-group">
                    % for p in with_mod:
                        <a href="${request.route_url('viewpack', id=p.id)}" class="list-group-item">${p.name}</a>
                    % endfor
                    </div>
                </div>
            </div>
        % endif
        </div>
    </div>
</div>
<br>
<h3>Versions</h3>
<div class="row bmargin relative-position">
    <div class="col-lg-8">
        <a href="${request.route_url('flagmod', id=mod.id)}" class="btn ${'btn-danger' if not mod.outdated else 'btn-default'}" id="flag">
            <i class="fa fa-flag"></i> <span>${'Unf' if mod.outdated else 'F'}</span>lag as Outdated
        </a>
    </div>
    % if perm:
    <div class="col-lg-4 force-bottom">
        <div class="pull-right">
            <a href="${request.route_url('addversion', id=mod.id)}"><i class="fa fa-plus no-decoration"></i> Add Version</a>
        </div>
    </div>
    % endif
</div>
<div class="table-responsive">
    <table class="table table-hover">
        <thead>
            <tr><th>Version</th><th>Direct Link<th>Devel</th><th>Minecraft</th><th>Action</th></tr>
        </thead>
        <tbody>
        % for version in mod.versions[::-1]:
            <tr class="button-height">
                <td>${version.version}</td>
                <td>
                % if version.mod_file_url != None:
                    <span class="text-danger">True</span>
                % else:
                    False
                % endif
                </td>
                <td>${version.devel}</td>
                <td>${version.mc_min} - ${version.mc_max}</td>
                <td>
                    <div class="dropdown">
                        <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" href="#">
                            Action
                            <span class="fa fa-caret-down"></span></button>
                        <ul class="dropdown-menu">
                            <li><a href="${request.route_url('downloadversion', id=version.id)}"><i class="fa fa-download fa-fw"></i> Download</a></li>
                            <li><a href="${request.route_url('versiondetails', id=version.id)}" class="details"><i class="fa fa-file-text fa-fw"></i> Details</a></li>
                            % if perm:
                                <li><a href="${request.route_url('deleteversion', id=version.id)}"><i class="fa fa-trash-o fa-fw"></i> Delete</a></li>
                                <li><a href="${request.route_url('editversion', id=version.id)}"><i class="fa fa-pencil fa-fw"></i> Edit</a></li>
                                % if loop.index != 0:
                                    <li><a href="${request.route_url('moveversion', id=mod.id, shift=1, index=loop.index)}"><i class="fa fa-arrow-up fa-fw"></i> Move Up</a></li>
                                % endif
                                % if loop.index != len(mod.versions) - 1:
                                    <li><a href="${request.route_url('moveversion', id=mod.id, shift=-1, index=loop.index)}"><i class="fa fa-arrow-down fa-fw"></i> Move Down</a></li>
                                % endif
                            % endif
                        </ul>
                    </div>
                </td>
            </tr>
        % endfor
        </tbody>
    </table>
</div>
<div class="modal fade" id="details-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title">Version Details</h4>
      </div>
      <div class="modal-body" id="details-modal-content">
        <p>Nothing Here</p>
      </div>
    </div>
  </div>
</div>
<%block name="style">
    ${extras.banner_style(mod)}
</%block>
<%block name="endscripts">
    <script src="${request.static_url('packassembler:static/js/lib/bootbox.min.js')}"></script>
    <script src="${request.static_url('packassembler:static/js/bundled/wrapper.js')}"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            common.linkRows();
            common.linkDynamicSubmit('form');
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
            $('.details').click(function(e){
                e.preventDefault();
                console.log($(this).attr('href'));
                $('#details-modal-content').load($(this).attr('href'));
                $('#details-modal').modal();
            })
        });
    </script>
</%block>
