<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row">
    <div class="col-lg-12">
        % if error is not UNDEFINED:
            ${form.formerror(error)}
        % endif
        <form method="POST" action="" role="form" class="form-horizontal" enctype="multipart/form-data">
            ${form.showfield(f.version)}
            ${form.showfield(f.mc_min)}
            ${form.showfield(f.mc_max)}
            ${form.showfield(f.forge_min)}
            ${form.showfield(f.forge_min)}
            <%form:showinput label="File" name="file">
                <input id="mod_file" type="file" name="mod_file"></input>
            </%form:showinput>
            ${form.showsubmit(cancel)}
        </form>
    </div>
</div>