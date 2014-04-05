<%inherit file="base.mak"/>
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
<div class="row bmargin relative-position">
    <div class="col-lg-10">
        <div class="dropdown">
            ${listcommon.add_to_pack(packs)}
        </div>
    </div>
    <div class="col-lg-2 force-bottom">
        <div class="pull-right">
            <a href="${request.route_url('addmod')}"><i class="fa fa-plus no-decoration"></i> Add Mod</a>
        </div>
    </div>
</div>
<form method="POST" role="form">
    <table class="table table-hover table-bordered listtable">
        <thead>
            <tr><th class="center"><input type="checkbox" id="topcheck"></th><th>Name</th><th>Author</th><th>Latest Version</th><th>Latest Supported</th><th>Maintainer</th></tr>
        </thead>
        <tbody>
        % for mod in mods:
            <tr class="${'danger' if mod.outdated else ''} linked" data-href="${request.route_url('viewmod', id=mod.id)}">
                <td class="nolink center">
                    <input type="checkbox" name="mods" value="${mod.id}">
                </td>
                <td>${mod.name}</td>
                <td>${mod.author}</td>
                <%
                    if mod.versions:
                        v = mod.versions[-1]
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
<small class="pull-right">${len(mods)} mods, ${len(mods.filter(outdated=True))} flagged.</small>
<%block name="endscripts">
    <script src="${request.static_url('packassembler:static/js/bundled/wrapper.js')}"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            common.linkRows();
            common.linkAutoCheck('topcheck', 'mods');
            common.linkDynamicSubmit('form');
        });
    </script>
</%block>
