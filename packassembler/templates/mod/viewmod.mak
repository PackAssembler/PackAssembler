<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
<%namespace name="extras" file="extras.mak" />
<%!
    import re
    def linejoin(text):
        try:
            return '<br />'.join(text.splitlines())
        except AttributeError:
            return 'None'

    def externallink(text):
        trun = text[:35] + (text[35:] and '...')
        #return '<a href="{0}" target="_blank" rel="nofollow">{1}</a>'.format(text, trun)
        return '<a href="{0}" rel="nofollow">{1}</a>'.format(text, trun)

    def autolink(text):
        urlre = re.compile('(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
        try:
            return urlre.sub(lambda m: externallink(m.group(0)), text)
        except TypeError:
            return 'None'
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
            <a href="${request.route_url('editmod', id=mod.id)}" class="btn btn-info action-edit">Edit Mod</a>
            <a id="delete" class="btn btn-danger action-delete">Delete Mod</a>
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
    <div class="col-lg-4">
        <div class="panel panel-default">
            <div class="panel-heading">Details</div>
            <table class="table">
                <tr><td>Author</td><td><a href="${request.route_url('modlist')}?q=${mod.author}" rel="nofollow">${mod.author}</a></td></tr>
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
    <table class="table table-hover">
        <thead>
            <tr><th>Version</th><th>Devel</th><th>MC Min</th><th>MC Max</th><th>Action</th></tr>
        </thead>
        <tbody>
        % for version in mod.versions[::-1]:
            <tr class="button-height">
                <td>${version.version}</td>
                <td>${version.devel}</td>
                <td>${version.mc_min}</td>
                <td>${version.mc_max}</td>
                ##<td>&nbsp;</td>
                <td>
                    <div class="btn-group">
                        <a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">
                            Action
                            <span class="icon-caret-down"></span></a>
                        <ul class="dropdown-menu">
                            <li><a href="${request.route_url('downloadversion', id=version.id)}"><i class="icon-fixed-width icon-download"></i> Download</a></li>
                            <li><a href="${request.route_url('versiondetails', id=version.id)}" class="details"><i class="icon-fixed-width icon-file-text"></i> Details</a></li>
                            % if perm:
                                <li><a href="${request.route_url('deleteversion', id=version.id)}"><i class="icon-fixed-width icon-trash"></i> Delete</a></li>
                                <li><a href="${request.route_url('editversion', id=version.id)}"><i class="icon-fixed-width icon-pencil"></i> Edit</a></li>
                                % if loop.index != 0:
                                    <li><a href="${request.route_url('moveversion', id=mod.id, shift=1, index=loop.index)}"><i class="icon-fixed-width icon-arrow-up"></i> Move Up</a></li>
                                % endif
                                % if loop.index != len(mod.versions) - 1:
                                    <li><a href="${request.route_url('moveversion', id=mod.id, shift=-1, index=loop.index)}"><i class="icon-fixed-width icon-arrow-down"></i> Move Down</a></li>
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
<small>Permission: ${mod.permission | autolink,linejoin,n}</small>
<%block name="style">
    ${extras.banner_style(mod)}
</%block>
<%block name="endscripts">
    <script src="//rawgithub.com/makeusabrew/bootbox/master/bootbox.js"></script>
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
