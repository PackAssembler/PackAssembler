<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row">
    <div class="col-lg-12">
        % if error is not UNDEFINED:
            ${form.formerror(error)}
        % endif
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
            $('#mc_version').change(function(){
                update_forge_versions();
            });
            update_forge_versions();
        });
    </script>
</%block>