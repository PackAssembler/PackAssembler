## Bootstrap 3
<%def name="showinput(label, name='')">
    <div class="form-group">
        <label class="col-lg-2 control-label" for="${name}">${label}</label>
        <div class="col-lg-10">
            ${caller.body()}
        </div>
    </div>
</%def>

<%def name="showsubmit(cancel, name='submit', offset=2)">
    <div class="form-group">
        <div class="col-lg-offset-${offset} col-lg-${12-offset}">
            <button type="submit" class="btn btn-primary" name="${name}">Submit</button>&nbsp;
        % if cancel:
            <a href="${cancel}">Cancel</a>
        % endif
        </div>
    </div>
</%def>

<%def name="formerror(error)">
    % if error != '':
        <div class="alert alert-danger">
            ${error | n}
        </div>
    % endif
</%def>

## WTForms
<%def name="showfield(field)">
    <div class="form-group">
        ${field.label(class_='col-lg-2 control-label')}
        <div class="col-lg-10">
            ${field(class_='form-control')}
            % if field.errors:
                % for error in field.errors:
                    <span class="text-danger">${error}&nbsp;</span>
                % endfor
            % endif
        </div>
    </div>
</%def>

<%def name="showfields(form)">
    % for field in form:
        ${showfield(field)}
    % endfor
</%def>

## Captcha
<%def name="captcha()">
    <%self:showinput label="Captcha">
        <%
            pkey = request.registry.settings.get('recaptcha_pub_key')
        %>
        <script type="text/javascript" src="https://www.google.com/recaptcha/api/challenge?k=${pkey}"></script>
        <noscript>
            <iframe src="https://www.google.com/recaptcha/api/noscript?k=${pkey}"
                height="300" width="500" frameborder="0"></iframe><br>
            <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
            <input type="hidden" name="recaptcha_response_field" value="manual_challenge">
        </noscript>
    </%self:showinput>
</%def>
