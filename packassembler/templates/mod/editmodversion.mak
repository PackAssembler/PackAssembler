<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<%namespace name="g" module="packassembler.template_helpers.general" />
<h2>${title}</h2>
<hr>
<div class="row">
    <div class="col-lg-12">
        % if error is not UNDEFINED:
            ${form.formerror(error)}
        % endif
        <form method="POST" action="" role="form" class="form-horizontal" enctype="multipart/form-data">
            <div class="panel-group" id="accordion">
                <%self:autopanel header="General" id="general-header" default="True">
                    ${form.showfield(f.version)}
                    ${form.showfield(f.changelog)}
                    ${form.showfield(f.devel)}
                </%self:autopanel>
                <%self:autopanel header="Dependencies" id="dependencies-header">
                    <h4>MC and Forge</h4>
                    ${form.showfield(f.mc_version)}
                    ${form.showfield(f.forge_min)}
                    <h4>Mod Dependencies</h4>
                    <%form:showinput name="add_depends" label="Add Dependency">
                        <select id="add_depends" class="form-control">
                            <option></option>
                        % for mod in mods:
                            <option value="${mod.id}">${mod.name}</option>
                        % endfor
                        </select>
                    </%form:showinput>
                    <table class="table table-bordered listtable" id="depends_table">
                        <tbody>
                        </tbody>
                    </table>
                </%self:autopanel>
                <%self:autopanel header="File" id="file-header">
                    <%form:showinput label="${f.mod_file.label.text}" name="${f.mod_file.name}">
                        ${f.mod_file()}
                    </%form:showinput>
                    ${form.showfield(f.mod_file_url)}
                    ${form.showfield(f.upload_from_url)}
                </%self:autopanel>
            </div>
            <hr>
            ${form.showsubmit(cancel, offset=0)}
        </form>
    </div>
</div>

<%def name="autopanel(header, id, parent='accordion', default=False)">
    <div class="panel panel-default">
        <div class="panel-heading">
            <h4 class="panel-title">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#${parent}" href="#${id}">${header}</a>
            </h4>
        </div>
        <div id="${id}" class="panel-collapse collapse ${g.show_if('in', default)}">
            <div class="panel-body">
                ${caller.body()}
            </div>
        </div>
    </div>
</%def>

<%block name="endscripts">
    <script type="text/javascript">
        var depends = [];

        function remove_from_array(array, value){
            array.splice(array.indexOf(value), 1);
        }

        function add_one(name, id){
            // Check that we don't have it
            if (depends.indexOf(id) == -1){
                // Add our new html
                $('#depends_table').find('tbody').append(
                    $('<tr>').append($('<td>')
                        .attr('class', 'linked middle center link-hover')
                        .append(
                            $('<i>').attr('class', 'fa fa-times text-danger')
                        )
                        .click(function(){
                            remove_from_array(depends, id);
                            $(this).parent().remove();
                        })
                    ).append($('<td>')
                        .attr('class', 'giant')
                        .text(name)
                        .append($('<input>')
                            .attr('type', 'hidden')
                            .attr('value', id)
                            .attr('name', 'depends')
                        )
                    )
                );

                // Add it to the list
                depends.push(id);
            }
        }

        $(document).ready(function(){
            $('#add_depends').change(function(){
                // Assign useful variable to the data we want
                var name = $("#add_depends option:selected").html();
                var id = $(this).val();

                // Make it blank again
                $(this).val('');

                add_one(name, id);
            });
            % if mv:
                % for dep in mv.depends:
                    add_one('${dep.name}', '${dep.id}');
                % endfor
            % endif
        });
    </script>
</%block>
