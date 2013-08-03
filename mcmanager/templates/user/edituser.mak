<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row"><div class="span10">
    <form class="form-horizontal" method="post" action="${request.url}" novalidate="novalidate" id="edit-build">
        ${form.formerror(error)}
        ${form.horfield('txtCurrentPassword', 'Current Password', 'password', auto=False, attr={
            'required': 'required'
        })}
        ${form.horfield('txtNewPassword', 'New Password', 'password', auto=False, attr={
            'required': 'required'
        })}
        ${form.horfield('txtConfirmPassword', 'Confirm Password', 'password', auto=False, attr={
            'data-equalto': '#txtNewPassword',
            'required': 'required'
        })}
        ${form.horsubmit(request.route_url('profile', id=request.matchdict['id']))}
    </form>
</div></div>
<%block name="style">
    ${form.formstyle()}
</%block>
<%block name="endscripts">
    ${form.formscripts('edit-build')}
</%block>