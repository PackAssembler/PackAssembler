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
                    ${form.showfield(pf.password)}
                    ${form.showfield(pf.confirm)}
                    <hr>
                    ${form.showfield(pf.current)}
                    ${pf.current_user()}
                    ${form.showsubmit(None, name='password_submit')}
                </form>
            </div>
        </div>
        <div class="panel panel-default">
            <div class="panel-heading">
                <h4>Change Email</h3>
            </div>
            <div class="panel-body">
                <form method="POST" action="" role="form" class="form-horizontal">
                    ${form.showfield(ef.email)}
                    ${ef.current_user()}
                    ${form.showfield(ef.current)}
                    ${form.showsubmit(None, name='email_submit')}
                </form>
            </div>
        </div>
        <div class="panel panel-default">
            <div class="panel-heading">
                <h4>Avatar Type</h3>
            </div>
            <div class="panel-body">
                <form method="POST" action="" role="form" class="form-horizontal">
                    ${form.showfields(af)}
                    ${form.showsubmit(None, name='avatar_submit')}
                </form>
            </div>
        </div>
    </div>
</div>