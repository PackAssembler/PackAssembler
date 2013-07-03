<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<form class="form-horizontal" method="post" action="${request.route_url('login')}">
    ${form.formerror(error)}
    <input type="hidden" name="came_from" value="${came_from}" />
    ${form.horfield('txtUsername', 'Username', 'text', attr={'required': 'required'})}
    ${form.horfield('txtPassword', 'Password', 'password', attr={'required': 'required'})}
    <%
        ec = '<a href="' + request.route_url('signup') + '">Create a new account</a>'
    %>
    ${form.horsubmit(came_from, extracontrols=ec)}
</form>
