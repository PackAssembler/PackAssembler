<!DOCTYPE html>
<html>
<head>
    <title>MC Manager &middot; ${title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    ##<link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0-rc1/css/bootstrap.min.css" rel="stylesheet">
    <link href="//netdna.bootstrapcdn.com/bootswatch/2.3.2/united/bootstrap.min.css" rel="stylesheet">
    <link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet">
    <style type="text/css">
        body {
            padding-top: 60px;
            background: url("http://subtlepatterns.com/patterns/cream_pixels.png") repeat scroll 0% 0% transparent;
        }
        @media (max-width: 980px) {
            .navbar-text.pull-right {
                float: none;
                padding-left: 5px;
                padding-right: 5px;
            }
        }
        .padded {
            padding-bottom: 100px;
        }
    </style>
    <%block name="style">
    </%block>
</head>
<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="navbar-inner">
            <div class="container">
                <button class="btn btn-navbar" data-target=".nav-collapse"
                 data-toggle="collapse" type="button">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="brand" href="${request.route_url('home')}">MC Manager</a>
                <div class="nav-collapse collapse">
                    <ul class="nav">
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
                        ${genclass('Mod List')}
                            <a href="${request.route_url('modlist')}">Mod List</a>
                        </li>
                        ${genclass('Pack List')}
                            <a href="${request.route_url('packlist')}">Pack List</a>
                        </li>
                        ${genclass('Server List')}
                            <a href="${request.route_url('serverlist')}">Server List</a>
                        </li>
                        ${genclass('About')}
                            <a href="${request.route_url('about')}">About</a>
                        </li>
                    </ul>
                    <ul class="nav pull-right">
                    <%def name="makedropdown()">
                        % if user == None:
                        <li class="pull-right">
                            <a href="${request.route_url('login')}">Login</a>
                        </li>
                        % else:
                        <li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                                Logged in as ${user.username}
                                <i class="icon-caret-down"></i>
                            </a>
                            <ul class="dropdown-menu">
                                <li><a href="${request.route_url('profile', userid=user.id)}"><i class="icon-fixed-width icon-user"></i> Profile</a></li>
                                <li><a href="${request.route_url('logout')}"><i class="icon-fixed-width icon-off"></i> Logout</a></li>
                            </ul>
                        </li>
                        % endif
                    </%def>
                        ${makedropdown()}
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div class="container padded">
        ${next.body()}
    </div>
    <script src="${request.static_url('mcmanager:static/jquery-latest.js')}"></script>
    <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js"></script>
    ##<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0-rc1/js/bootstrap.min.js"></script>
    <%block name="endscripts">
    </%block>
</body>
</html>
