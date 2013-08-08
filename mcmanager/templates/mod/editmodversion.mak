<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row"><div class="span10">
    <form class="form-horizontal" method="post" action="${request.url}" novalidate="novalidate" id="edit-version" enctype="multipart/form-data">
        ${form.formerror(error)}
        ${form.horfield('txtVersion', 'Version', 'text', attr={
            'required': 'required'
        })}
        ${form.mcselect('selMCMin', 'Minecraft Min')}
        ${form.mcselect('selMCMax', 'Minecraft Max')}
        ${form.forgefield('txtForgeMin', 'Forge Min')}
        ${form.forgefield('txtForgeMax', 'Forge Max')}
        <%form:horgeneric name="uplModFile" label="File">
            <div class="fileupload fileupload-new" data-provides="fileupload">
                <div class="input-append inputexp">
                    <div class="uneditable-input"><i class="icon-file fileupload-exists"></i> <span class="fileupload-preview"></span></div><span class="btn btn-file"><span class="fileupload-new">Select file</span><span class="fileupload-exists">Change</span><input type="file" name="uplModFile" id="uplModFile" required="required" /></span><a href="#" class="btn fileupload-exists" data-dismiss="fileupload" data-trigger="mouseover">Remove</a>
                </div>
            </div>
        </%form:horgeneric>
        ${form.horsubmit(request.referer)}
    </form>
</div></div>
<%block name="style">
    <link href="${request.static_url('mcmanager:static/css/bootstrap-fileupload.min.css')}" rel="stylesheet">
</%block>
<%block name="endscripts">
    <script src="${request.static_url('mcmanager:static/js/bootstrap-fileupload.min.js')}"></script>
    ${form.formscripts('edit-version')}
    % if v is not UNDEFINED:
        <script type="text/javascript">
            $(document).ready(function(){
                $('#txtVersion').val("${v.version}");
                $('#selMCMin').val("${v.mc_min}");
                $('#selMCMax').val("${v.mc_max}");
                % if v.forge_min:
                    $('#txtForgeMin').val("${v.forge_min}");
                % endif
                % if v.forge_max:
                    $('#txtForgeMax').val("${v.forge_max}");
                % endif
                $('#uplModFile').parsley('removeConstraint', 'required');
            });
        </script>
    % endif
</%block>
