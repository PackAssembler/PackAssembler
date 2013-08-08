<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row"><div class="span10">
    <form class="form-horizontal" method="post" action="${request.url}" novalidate="novalidate" id="send-reset-password">
        ${form.horfield('txtEmail', 'Email', 'text', auto=False, attr={
            'data-type': 'email',
            'required': 'required'
        })}
        ${form.horsubmit(request.route_url('login'))}
    </form>
</div></div>
<%block name="endscripts">
    ${form.formscripts('send-reset-password')}
</%block>