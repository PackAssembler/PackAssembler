<table class="table">
    <tr>
        <td>Uploaded</td><td>${version.id.generation_time.strftime('%e %b %Y %I:%m:%S %p')}</td>
    </tr>
    <tr>
        <td>MD5</td><td>${version.mod_file.md5 if version.mod_file else version.mod_file_url_md5}</td>
    </tr>
% if version.depends or version.opt_depends:
    <tr>
        <td>Dependencies</td>
        <td>
        % for dep in version.depends:
            <a href="${request.route_url('viewmod', id=dep.id)}">${dep.name}</a><br>
        % endfor
        % for dep in version.opt_depends:
            <a href="${request.route_url('viewmod', id=dep.id)}">${dep.name}</a> (Optional)<br>
        % endfor
        </td>
    </tr>
% endif
</table>
