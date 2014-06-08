<%inherit file="base.mak"/>
<%namespace name="g" module="packassembler.template_helpers.general" />
<%namespace name="listcommon" file="list.mak" />
<%namespace name="extras" file="extras.mak" />

## Similar to listcommon.head(), but with extra filters/buttons
<div class="row">
    <div class="col-lg-6">
        <h2>${title}</h2>
    </div>
    <div class="col-lg-6">
        <div class="pull-right">
            <form id="search-form" class="form-inline" method="GET" action="${request.url}">
                <div class="form-group">
                    <input type="hidden" name="mc_version" value="${request.params.get('mc_version', '')}">
                    <div id="version-dropdown" class="dropdown" display="none">
                        <button class="btn btn-default dropdown-toggle" type="button" id="version-dropdown-button" data-toggle="dropdown">
                            MC Version
                            <span class="caret"></span>
                        </button>
                        <ul class="dropdown-menu">
                            % for version in mc_versions:
                                <li><a href="#">${version}</a></li>
                            % endfor
                        </ul>
                    </div>
                    <input type="search" name="q" class="form-control" value="${request.params.get('q', '')}" x-webkit-speech>
                </div>
                <button type="submit" class="btn">Search</button>
                <button name="outdated" type="submit" class="btn btn-danger">Outdated</button>
            </form>
        </div>
    </div>
</div>

<hr>
${extras.flash()}
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
            <tr class="${g.show_if('danger', mod.outdated)} linked" data-href="${request.route_url('viewmod', id=mod.id)}">
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
                <td>${v.mc_version if v else None}</td>
                <td>${(mod.owner and mod.owner.username) or None}</td>
            </tr>
        % endfor
        </tbody>
    </table>
</form>
<small class="pull-right">${len(mods)} mods, ${len(mods(outdated=True))} flagged.</small>
<%block name="endscripts">
    <script src="${request.static_url('packassembler:static/js/bundled/wrapper.js')}"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            common.linkRows();
            common.linkAutoCheck('topcheck', 'mods');
            common.linkDynamicSubmit('form');

            $('#version-dropdown').css('display', 'inline-block')
            $('#version-dropdown > ul > li > a').click(function(){
                var val = $(this).html();
                $('input[name="mc_version"]').attr('value', val);
            % if 'outdated' in request.params:
                $('<input />').attr('type', 'hidden')
                               .attr('name', 'outdated')
                               .appendTo('#search-form');
            % endif
                $('#search-form').submit();
            });
        });
    </script>
</%block>
