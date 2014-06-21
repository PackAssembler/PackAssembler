<!DOCTYPE html>
<html>
<head>
    <title>${title} &middot; Pack Assembler</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta name="google-site-verification" content="yXuM2JTT_NbRwI9pbVruYjq9W9t7bF9wIe7eiqwAy1A" />
    <link href="//netdna.bootstrapcdn.com/bootswatch/3.1.1/cyborg/bootstrap.min.css" rel="stylesheet">
    <link href="//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css" rel="stylesheet">

    <link href="${request.static_url('packassembler:static/dist/css/master.css')}" rel="stylesheet">
    <link href="${request.static_url('packassembler:static/dist/img/favicon.ico')}" rel="icon">
    <%block name="style">
    </%block>
</head>
<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="${request.route_url('home')}">Pack Assembler</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <%def name="genclass(name)">
                        % if name == title:
                            <li class="active">
                        % else:
                            <li>
                        % endif
                    </%def>
                    ${genclass('Home')}
                        <a href="${request.route_url('home')}">Home</a>
                    </li>
                    ${genclass('Mods')}
                        <a href="${request.route_url('modlist')}">Mods</a>
                    </li>
                    ${genclass('Packs')}
                        <a href="${request.route_url('packlist')}">Packs</a>
                    </li>
                    ${genclass('Servers')}
                        <a href="${request.route_url('serverlist')}">Servers</a>
                    </li>
                    ${genclass('Users')}
                        <a href="${request.route_url('userlist')}">Users</a>
                    </li>
                    ${genclass('FAQ')}
                        <a href="${request.route_url('faq')}">FAQ</a>
                    </li>
                    <li>
                        <a href="http://forums.stephenmac.com/">Forums</a>
                    </li>
                </ul>
                <ul class="nav navbar-nav pull-right">
                    % if user == None:
                        <li class="pull-right">
                            <a href="${request.route_url('login')}">Login</a>
                        </li>
                    % else:
                        <li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                                Logged in as ${user.username}
                                <i class="fa fa-caret-down"></i>
                            </a>
                            <ul class="dropdown-menu">
                                <li><a href="${request.route_url('profile', id=user.id)}"><i class="fa fa-user fa-fw"></i> Profile</a></li>
                                <li><a href="${request.route_url('logout')}"><i class="fa fa-power-off fa-fw"></i> Logout</a></li>
                            </ul>
                        </li>
                    % endif
                </ul>
            </div>
        </div>
    </div>
    <div id="main-content" class="container padded-top">
        ${next.body()}
    </div>
    <script src="${request.static_url('packassembler:static/dist/js/lib/jquery-latest.js')}"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
    ## Tracking
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-5915643-11', 'stephenmac.com');
      ga('require', 'displayfeatures');
      ga('send', 'pageview');

    </script>
    <%block name="endscripts">
    </%block>
</body>
</html>
