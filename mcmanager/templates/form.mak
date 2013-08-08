<%def name="horfield(name, label, itype, attr={}, auto=True)">
    <%
        exp_attr = ''
        for key in attr:
            exp_attr += ' ' + key + '="' + attr[key] + '"'
        if auto == False:
            exp_attr += ' autocomplete="off"'
    %>
    <div class="control-group">
        <label class="control-label" for="${name}">${label}</label>
        <div class="controls">
            <input type="${itype}" id="${name}" name="${name}"${exp_attr | n}>
        </div>
    </div>
</%def>
<%def name="horgeneric(name, label)">
    <div class="control-group">
        <label class="control-label" for="${name}">${label}</label>
        <div class="controls">
            ${caller.body()}
        </div>
    </div>
</%def>
<%def name="mcopts()">
    % for mcver in ['1.5.2', '1.5.1', '1.5', '1.4.7']:
        <option value=${mcver}>${mcver}</option>
    % endfor
</%def>
<%def name="mcselect(name, label)">
    <%self:horgeneric name="${name}" label="${label}">
        <select id="${name}" name="${name}">
            ${mcopts()}
        </select>
    </%self:horgeneric>
</%def>
<%def name="forgefield(name, label, required=False)">
    <%
        attrs = {
            'data-regexp': '^([0-9]\.){3}[0-9]{3}$'
        }
        if required is True:
            attrs['required'] = 'required'
    %>
    ${horfield(name, label, 'text', attr=attrs)}
</%def>
<%def name="horsubmit(cancel, name='btnSubmit', extracontrols='')">
    <div class="control-group">
        <div class="controls">
            <button type="submit" name="${name}" class="btn btn-primary">Submit</button>
            <a href="${cancel}" class="btn">Cancel</a><br>
            % if extracontrols != '':
            ${extracontrols | n}
            % endif
        </div>
    </div>
</%def>
<%def name="formerror(error)">
    % if error != '':
        <div class="alert alert-error">
            ${error | n}
        </div>
    % endif
</%def>
<%def name="formscripts(formid, include_garlic=False)">
    <script src="${request.static_url('mcmanager:static/js/parsley.min.js')}"></script>
    % if include_garlic:
    <script src="${request.static_url('mcmanager:static/js/garlic.min.js')}"></script>
    % endif
    <script type="text/javascript">
        $(document).ready(function () {
            $('#${formid}').parsley({
                successClass: 'success',
                errorClass: 'error',
                errors: {
                    classHandler: function(el) {
                        return $(el).closest('.control-group');
                    },
                    errorsWrapper: '<span class=\"help-inline\"></span>',
                    errorElem: '<span></span>'
                }
            });
        });
    </script>
</%def>
