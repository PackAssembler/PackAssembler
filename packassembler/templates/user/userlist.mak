<%inherit file="base.mak"/>
<%namespace name="extras" file="extras.mak" />
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
% for user in users:
    <div class="userbox well col-lg-2 center linked" data-href="${request.route_url('profile', id=user.id)}">
        <div class="userbox-avatar">
            ${extras.avatar(user, 100)}
        </div>
        <br>
        <div>
            <h4>${user.username}</h4>
            ${extras.show_group('h5', user)}
        </div>
    </div>
% endfor

<%block name="endscripts">
    <script src="${request.static_url('packassembler:static/js/bundled/wrapper.js')}"></script>
    <script type="text/javascript">$(document).ready(function(){common.linkRows();});</script>
</%block>