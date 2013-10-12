<%inherit file="base.mak"/>
<%namespace name="extras" file="extras.mak" />
<%namespace name="listcommon" file="list.mak" />
${listcommon.head()}
<hr>
% for user in users:
    <div class="userbox well col-lg-2 center">
        <div class="userbox-avatar">
            ${extras.avatar(user, 100)}
        </div>
        <br>
        <div>
            <h4>${user.username}</h4>
            ${extras.show_group('h5', user)}
            <a href="${request.route_url('profile', id=user.id)}">View Profile</a>
        </div>
    </div>
% endfor