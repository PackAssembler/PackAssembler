<%inherit file="base.mak"/>
<h2>${title}</h2>
<hr>
<div class="alert alert-danger">
    ${message}
</div>
% if request.referer:
    <a href="${request.referer}" class="btn btn-large btn-primary pull-right">Back</a>
    <%block name="endscripts">
        <script type="text/javascript">
            window.setTimeout(function(){
                window.location.replace('${request.referer}');
            }, 5000);
        </script>
    </%block>
% endif
