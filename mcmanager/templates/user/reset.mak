<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row"><div class="span10">
    <form class="form-horizontal" method="post" action="${request.url}" novalidate="novalidate" id="reset-password">
        ${form.horfield('txtPassword', 'New Password', 'password', auto=False, attr={
            'required': 'required'
        })}
        ${form.horfield('txtConfirmPassword', 'Confirm Password', 'password', auto=False, attr={
            'data-equalto': '#txtPassword',
            'required': 'required'
        })}
        ${form.horsubmit(request.route_url('login'))}
    </form>
</div></div>
<%block name="endscripts">
    ${form.formscripts('reset-password')}
</%block>