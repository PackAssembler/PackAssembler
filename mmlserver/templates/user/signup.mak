<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<form class="form-horizontal" method="post" action="${request.route_url('signup')}" novalidate="novalidate" id="new-user">
    ${form.formerror(error)}
    ${form.horfield('txtUsername', 'Username', 'text', auto=False, attr={
        'data-minlength': '6',
        'data-maxlength': '32',
        'data-remote': 'taken',
        'data-remote-message': 'Username is taken.',
        'data-type': 'alphanum',
        'required': 'required'
    })}
    ${form.horfield('txtEmail', 'Email', 'text', auto=False, attr={
        'data-type': 'email',
        'required': 'required'
    })}
    ${form.horfield('txtPassword', 'Password', 'password', auto=False, attr={
        'required': 'required'
    })}
    ${form.horfield('txtConfirm', 'Confirm', 'password', auto=False, attr={
        'data-equalto': '#txtPassword',
        'required': 'required'
    })}
    <%form:horgeneric name="txtCaptcha" label="Captcha">
        <script type="text/javascript" src="https://www.google.com/recaptcha/api/challenge?k=6LfMiuUSAAAAAHAzuJ60jYSZYPI8IO5kWBNURpIA"></script>
        <noscript>
            <iframe src="https://www.google.com/recaptcha/api/noscript?k=6LfMiuUSAAAAAHAzuJ60jYSZYPI8IO5kWBNURpIA"
                height="300" width="500" frameborder="0"></iframe><br>
            <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
            <input type="hidden" name="recaptcha_response_field" value="manual_challenge">
        </noscript>
    </%form:horgeneric>
    ${form.horsubmit(request.route_url('login'))}
</form>
<%block name="endscripts">
    ${form.formscripts('new-user')}
</%block>
