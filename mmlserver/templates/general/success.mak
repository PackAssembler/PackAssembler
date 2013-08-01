<%inherit file="base.mak"/>
<h2>${title}</h2>
<hr>
<div class="alert alert-success">
    ${message}
</div>
<a href="${redir}" class="btn btn-primary pull-right btn-large">Continue</a>
<%block name="endscripts">
    <script type="text/javascript">
        window.setTimeout(function(){
            window.location.replace('${redir}');
        }, 5000);
    </script>
</%block>
