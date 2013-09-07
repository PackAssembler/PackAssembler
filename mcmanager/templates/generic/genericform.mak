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
            ${form.showfields(f)}
            ${form.showsubmit(cancel)}
        </form>
    </div>
</div>
<%block name="endscripts">
    <script src="${request.static_url('mcmanager:static/js/wysihtml5-0.3.0.min.js')}"></script>
</%block>