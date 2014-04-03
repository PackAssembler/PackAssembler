<table class="table">
% if version.changelog:
    <tr><td>Changelog</td><td>${version.changelog}</td></tr>
% endif
    <tr>
        <td>Uploaded</td><td>${version.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td>
    </tr>
    <tr>
        <td>MD5</td><td>${version.mod_file.md5 if version.mod_file else version.mod_file_url_md5}</td>
    </tr>
% if version.forge_min:
    <tr><td>Forge Min</td><td>${version.forge_min}</td></tr>
% endif
% if version.forge_max:
    <tr><td>Forge Max</td><td>${version.forge_max}</td></tr>
% endif
% if version.depends:
    <tr>
        <td>Dependencies</td>
        <td>
        % for dep in version.depends:
            <a href="${request.route_url('viewmod', id=dep.id)}">${dep.name}</a><br>
        % endfor
        </td>
    </tr>
% endif
</table>
