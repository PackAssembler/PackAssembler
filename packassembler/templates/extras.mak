<%def name='avatar(user, size)'>
    <%
        if user.avatar_type:
            img_src = 'https://minotar.net/avatar/{0}/{1}'.format(user.username, str(size))
        else:
            img_src = 'http://www.gravatar.com/avatar/{0}?s={1}&r=pg&d=identicon'.format(user.email_hash, str(size))
    %>
    <img class="img-thumbnail" src="${img_src}" alt="avatar">
</%def>

<%def name='show_group(e, user)'>
    <%
        g = user.group.title()
        colors = {'User': '', 'Contributor': 'text-success', 'Moderator': 'text-info', 'Admin': 'text-danger'}
    %>
    % if g in colors.keys():
        <${e} class="${colors[g]}">${g}</${e}>
    % else:
        <${e}>N/A</${e}>
    % endif
</%def>

<%def name='banner_style(obj)'>
    <style type="text/css">
    % if obj.banner:
        div.infobar
        {
            background: url("${obj.banner.image}") no-repeat scroll left;
            background-size: cover;
            background-width: 100%;
        }
        div.infobar h2
        {
            color: ${obj.banner.text_color};
        }
    % endif
    </style>
</%def>