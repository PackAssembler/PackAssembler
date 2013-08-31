<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row">
    <div class="col-lg-12">
        ${form.formerror(error)}
        <form method="POST" action="" role="form" class="form-horizontal">
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
