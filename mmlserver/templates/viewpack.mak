<%inherit file="base.mak"/>
<div class="row">
    <div class="span8">
        <h2>${title}</h2>
        <h4 class="muted">${pack.owner.username}</h4>
    </div>
    <div class="span4">
    % if perm:
        <div class="btn-group pull-right" style="margin-top: 10px">
            <a href="${request.route_url('editpack', packid=pack.id)}" class="btn btn-info">Edit Pack</a>
            <a href="${request.route_url('deletepack', packid=pack.id)}" class="btn btn-danger">Delete Pack</a>
        </div>
    % endif
    </div>
</div>
<hr>
<h3>Mods</h3>
% if pack.mods:
    <ul>
    % for mod in pack.mods:
        <li><a href="${request.route_url('viewmod', modid=mod.id)}">${mod.name}</a> 
        % if perm:
            <a href="${request.route_url('removepackmod', modid=mod.id, packid=pack.id)}"><i class="icon-remove text-error"></i></a>
        % endif
        </li>
    % endfor
    </ul>
% else:
    No Mods Yet!
% endif
% if perm:
    <div style="margin-top: 11px">
        <a href="${request.route_url('addpackmod', packid=pack.id)}"><i class="icon-plus" style="text-decoration: none;"></i> Add Mod to Pack</a>
    </div>
% endif
<h3>Builds</h3>
% if perm:
    <a href="${request.route_url('addbuild', packid=pack.id)}"><i class="icon-plus" style="text-decoration: none;"></i> New Build</a>
% endif