<%inherit file="base.mak"/>
<%namespace name="form" file="form.mak" />
<h2>${title}</h2>
<hr>
<div class="row"><div class="span10">
    <form class="form-horizontal" method="post" action="${request.url}" novalidate="novalidate" id="edit-pack">
        ${form.formerror(error)}
        ${form.horfield('txtName', 'Name', 'text', attr={
            'data-maxlength': '32',
            'data-regexp': '^[\w ]+$',
            'required': 'required'
        })}
        ${form.horsubmit(request.route_url('home'))}
    </form>
</div></div>
<%block name="endscripts">
    ${form.formscripts('add-pack')}
    % if v is not UNDEFINED:
        <script type="text/javascript">
            $(document).ready(function(){
                $('#txtName').val("${v.name}");
            });
        </script>
    % endif
</%block>
<%block name="style">
    ${form.formstyle()}
</%block>