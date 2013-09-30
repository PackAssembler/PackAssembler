<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
<div class="row bmargin relative-position">
    <div class="col-lg-10">
        <a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">
            Add to Pack
            <span class="icon-caret-down"></span>
        </a>
        <ul class="dropdown-menu">
            % if packs:
                % for pack in packs:
                <li><a href="#" data-id="${pack.id}">${pack.name}</a></li>
                % endfor
            % else:
                <li><a href="#">You have no packs!</a></li>
            % endif
            <li class="divider"></li>
            <li><a href="${request.route_url('addpack')}" class="action-add">Add Pack</a></li>
        </ul>
    </div>
    <div class="col-lg-2 force-bottom">
        <div class="pull-right">
            <a href="${request.route_url('addmod')}"><i class="icon-plus no-decoration"></i> Add Mod</a>
        </div>
    </div>
</div>
<form method="POST" action="" role="form">
    <table class="table table-hover table-bordered listtable">
        <thead>
            <tr><th class="center"><input type="checkbox" id="topcheck"></th><th>Name</th><th>Author</th><th>Latest Version</th><th>Latest Supported</th><th>Maintainer</th></tr>
        </thead>
        <tbody>
        % for mod in mods:
            <tr class="${'danger' if mod.outdated else ''} linked" data-href="${request.route_url('viewmod', id=mod.id)}">
                <td class="nolink center">
                    <%doc><a href="${request.route_url('viewmod', id=mod.id)}"></%doc>
                    <input type="checkbox" name="mods" value="${mod.id}">
                </td>
                <td>${mod.name}</a></td>
                <td>${mod.author}</td>
                <%
                    if mod.versions:
                        v = max(mod.versions, key=lambda v: v.version.split('.'))
                    else:
                        v = None
                %>
                <td>${v.version if v else None}</td>
                <td>${v.mc_max if v else None}</td>
                <td>${mod.owner.username}</td>
            </tr>
        % endfor
        </tbody>
    </table>
</form>
<small class="pull-right">${len(mods.filter(outdated=True))} flagged mods.</small>
<%block name="endscripts">
    <script src="${request.static_url('packassembler:static/js/rowlink.js')}"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#topcheck').change(function(){
                $('input[name="mods"]').prop('checked', this.checked);
            });
            $('[data-id]').click(function(){
                $('form').attr('action', '/pack/addmod/' + $(this).data('id'))
                $('form').submit();
            });
        });
    </script>
</%block>
