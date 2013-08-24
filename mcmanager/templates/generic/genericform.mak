<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row">
    <div class="col-lg-12">
        <form method="POST" action="" role="form" class="form-horizontal">
            ${form.showfields(f)}
            ${form.showsubmit(request.referrer or cancel)}
        </form>
    </div>
</div>