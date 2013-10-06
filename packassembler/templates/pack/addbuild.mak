<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row">
    <div class="col-lg-12">
    % if depends:
        <div class="alert alert-danger">
            Unresolved Dependencies:
        % for modid, deps in depends.items():
            <ul>
            % for dep in deps:
            <li><a href="${request.route_url('viewmod', id=dep.id)}" target="_blank">${dep.name}</a></li>
            % endfor
            </ul>
        % endfor
        </div>
    % endif
        ${form.formerror(error)}
        <form method="POST" action="" role="form" class="form-horizontal">
            ${form.showfield(f.mc_version)}
            <%form:showinput name="forge_version" label="${f.mc_version.label}">
                <select id="forge_version" name="forge_version" class="form-control"></select>
                % if f.forge_version.errors:
                    % for error in f.forge_version.errors:
                        <span class="text-danger">${error}&nbsp;</span>
                    % endfor
                % endif
            </%form:showinput>
            ${form.showfield(f.config)}
            <hr>
            % for mod in mods:
                <%form:showinput name="${mod.id}" label="${mod.name}">
                    <div class="input-group" id="select_${mod.id}">
                        <select name="${mod.id}" class="form-control">
                        % for version in mod.versions[::-1]:
                            <option value="${version.id}" data-mc-max="${version.mc_max}" data-mc-min="${version.mc_min}">${version.version}</option>
                        % endfor
                        </select>
                        <span class="input-group-addon">
                            <input type="checkbox" id="${mod.id}_checkbox" class="pull-right" title="Enable All Versions">
                        </span>
                    </div>
                </%form:showinput>
            % endfor
            ${form.showsubmit(cancel)}
        </form>
    </div>
</div>
<%block name="endscripts">
    <script type="text/javascript">
        $(document).ready(function(){
            function update_forge_versions(){
                $.get(
                    "${request.route_url('forgeversions')}",
                    {mc_version: $('#mc_version')[0].value},
                    function(data){
                        var $select = $('#forge_version')
                        $select.empty();
                        $.each(data, function(key, value) {
                            $select
                                .append($("<option></option>")
                                .attr("value",value)
                                .text(value));
                        });
                    },
                    'json'
                );
            }

            function update_mod_versions(only){
                var $select = only || $('div[id^=select]');
                var mc_version = $('#mc_version')[0].value.split('.');

                $select.each(function(){
                    var checked = $(this).find('input')[0].checked;
                    $(this).find('select').children().each(function(){
                        if (checked ||
                            $(this).data('mc-min').split('.') <= mc_version &&
                            $(this).data('mc-max').split('.') >= mc_version){
                            $(this).prop('disabled', false);
                        }
                        else{
                            $(this).prop('disabled', true);
                        }
                    });
                });
            }
            $('#mc_version').change(function(){
                update_forge_versions();
                update_mod_versions();
            });
            $('input[id$=checkbox]').change(function(){
                update_mod_versions($(this).parent().parent());
            });
            update_forge_versions();
            update_mod_versions();
        });
    </script>
</%block>