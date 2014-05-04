<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<%namespace name="extras" file="extras.mak" />
<h2>${title}</h2>
<hr>
<div class="row">
    <div class="col-lg-12">
        ${extras.flash()}
        ${form.formerror(error)}
        <form method="POST" role="form" class="form-horizontal">
            ${form.showfield(f.username)}
            ${f.came_from()}
            ${form.showfield(f.password)}
            ${form.showsubmit(f.came_from.data)}
            <div class="col-lg-offset-2 col-lg-10">
                <a href="${request.route_url('signup')}">Create a new account</a><br>
                <a href="${request.route_url('sendreset')}">Forgot Password</a>
            </div>
        </form>
    </div>
</div>
