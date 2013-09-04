<%def name='avatar(user, size)'>
    <%
        if user.avatar_type:
            img_src = 'https://minotar.net/avatar/{0}/{1}'.format(user.username, str(size))
        else:
            img_src = 'http://www.gravatar.com/avatar/{0}?s={1}&r=pg&d=identicon'.format(user.email_hash, str(size))
    %>
    <img class="img-thumbnail" src="${img_src}" alt="avatar"></img>
</%def>