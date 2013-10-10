<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row">
    <div class="col-lg-12">
        ${form.formerror(error)}
        <form method="POST" role="form" class="form-horizontal">
            ${form.showfields(f)}
            ${form.captcha()}
            ${form.showsubmit(request.referrer or request.route_url('login'))}
        </form>
    </div>
</div>
