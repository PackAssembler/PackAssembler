<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row"><div class="span10">
    <form class="form-horizontal" method="post" action="${request.url}" novalidate="novalidate" id="edit-server">
        ${form.formerror(error)}
        ${form.horfield('txtName', 'Name', 'text', attr={
            'data-maxlength': '32',
            'data-regexp': '^[\w ]+$',
            'required': 'required'
        })}
        ${form.horfield('txtUrl', 'Homepage', 'text', attr={
            'data-type': 'url'
        })}
        ${form.horfield('txtHost', 'Host', 'text', attr={
            'required': 'required'
        })}
        ${form.horfield('txtPort', 'Port', 'text', attr={
            'data-type': 'number',
            'value': '25565',
            'required': 'required'
        })}
        ${form.horfield('txtPackID', 'Pack ID', 'text', attr={
            'data-regexp': '^[0-9a-f]{24}$',
            'required': 'required'
        })}
        ${form.horfield('txtRevision', 'Pack Revision', 'text', attr={
            'data-type': 'number',
            'required': 'required'
        })}
        ${form.horfield('txtConfig', 'Custom Config', 'text', attr={
            'data-type': 'url'
        })}
        ${form.horsubmit(request.route_url('home'))}
    </form>
</div></div>
<%block name="endscripts">
    ${form.formscripts('edit-server')}
    % if v is not UNDEFINED:
        <script type="text/javascript">
            $(document).ready(function(){
                $('#txtName').val("${v.name}");
                % if v.url:
                    $('#txtUrl').val("${v.url}");
                % endif
                $('#txtHost').val("${v.host}");
                $('#txtPort').val("${v.port}");
                $('#txtPackID').val("${v.build.pack.id}");
                $('#txtRevision').val("${v.build.revision}");
                % if v.config:
                    $('#txtConfig').val("${v.config}");
                % endif
            });
        </script>
    % endif
</%block>
<%block name="style">
    ${form.formstyle()}
</%block>