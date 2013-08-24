<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row">
    <div class="col-lg-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h4>Change Password</h3>
            </div>
            <div class="panel-body">
                <form method="POST" action="" role="form" class="form-horizontal">
                    ${form.showfield(f.password)}
                    ${form.showfield(f.confirm)}
                    <hr>
                    ${form.showfield(f.current)}
                    ${f.current_user()}
                    ${form.showsubmit(request.referrer or cancel)}
                </form>
            </div>
        </div>
    </div>
</div>