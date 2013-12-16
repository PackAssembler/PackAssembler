<!DOCTYPE html>
<html>
<head>
    <title>Pack Assembler &middot; ${title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="//netdna.bootstrapcdn.com/bootswatch/3.0.2/cyborg/bootstrap.min.css" rel="stylesheet">
    <link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet">

    <link href="${request.static_url('packassembler:static/css/master.css')}" rel="stylesheet">
    <link href="${request.static_url('packassembler:static/css/keys.min.css')}" rel="stylesheet">
    <link href="${request.static_url('packassembler:static/img/favicon.ico')}" rel="icon">
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
                                <i class="icon-caret-down"></i>
                            </a>
                            <ul class="dropdown-menu">
                                <li><a href="${request.route_url('profile', id=user.id)}"><i class="icon-fixed-width icon-user"></i> Profile</a></li>
                                <li><a href="${request.route_url('logout')}"><i class="icon-fixed-width icon-off"></i> Logout</a></li>
                            </ul>
                        </li>
                    % endif
                </ul>
            </div>
        </div>
    </div>
    <div id="main-content" class="container padded-top">
        ${next.body()}
        <div class="modal fade" id="keyboard-shortcuts">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <h4 class="modal-title">Keyboard Shortcuts</h4>
                    </div>
                    <div class="modal-body">
                        <div class="keyboard-shortcuts-inner">
                            <div>
                                <h3>Go to</h3>
                                <%def name="shortcut(desc, keys)">
                                    <dt>
                                        % for key in keys.split(' '):
                                            <kbd class="light">${key}</kbd>
                                        % endfor
                                    </dt>
                                    <dd>
                                        ${desc}
                                    </dd>
                                </%def>
                                <dl>
                                    ${shortcut('Home', 'g h')}
                                    ${shortcut('Mods', 'g m')}
                                    ${shortcut('Packs', 'g p')}
                                    ${shortcut('Servers', 'g s')}
                                    ${shortcut('FAQ', 'g f')}
                                    ${shortcut('Login/Profile', 'g l')}
                                </dl>
                            </div>
                            <div>
                                <h3>Show</h3>
                                <dl>
                                    ${shortcut('Keyboard Shortcuts', 's k')}
                                </dl>
                            </div>
                        </div>
                        <div class="keyboard-shortcuts-inner">
                            <div>
                                <h3>Focus</h3>
                                <dl>
                                    ${shortcut('List Search', 'f s')}
                                    ${shortcut('First Input', 'f f')}
                                    ${shortcut('Last Input', 'f l')}
                                </dl>
                            </div>
                            <div>
                                <h3>Action</h3>
                                <dl>
                                    ${shortcut('Add', 'a a')}
                                    ${shortcut('Edit', 'a e')}
                                    ${shortcut('Delete', 'a d')}
                                    ${shortcut('Flag', 'a f')}
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="${request.static_url('packassembler:static/js/jquery-latest.js')}"></script>
    <script src="${request.static_url('packassembler:static/js/mousetrap.min.js')}"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    <script type="text/javascript">
        // Go to
        Mousetrap.bind('g h', function() { window.location = '${request.route_url('home')}'; });
        Mousetrap.bind('g m', function() { window.location = '${request.route_url('modlist')}'; });
        Mousetrap.bind('g p', function() { window.location = '${request.route_url('packlist')}'; });
        Mousetrap.bind('g s', function() { window.location = '${request.route_url('serverlist')}'; });
        Mousetrap.bind('g f', function() { window.location = '${request.route_url('faq')}'; });
        % if user is None:
            Mousetrap.bind('g l', function() { window.location = '${request.route_url('login')}'; });
        % else:
            Mousetrap.bind('g l', function() { window.location = '${request.route_url('profile', id=user.id)}'; });
        % endif
        // Show
        Mousetrap.bind('s k', function() { $('#keyboard-shortcuts').modal('toggle'); });
        // Actions
        Mousetrap.bind('a a', function() { $('.action-add')[0].click(); });
        Mousetrap.bind('a e', function() { $('.action-edit')[0].click(); });
        Mousetrap.bind('a d', function() { $('.action-delete')[0].click(); });
        Mousetrap.bind('a f', function() { $('.action-flag')[0].click(); });
        // Focus
        Mousetrap.bind('f s', function() { $('input[name="q"]').focus(); });
        Mousetrap.bind('f f', function() { $('input').first().focus(); });
        Mousetrap.bind('f l', function() { $('input').last().focus(); });
        // Hidden
        Mousetrap.bind('esc', function() { $('.modal').modal('hide'); });
    </script>
    ## Tracking
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-5915643-11', 'stephenmac.com');
      ga('send', 'pageview');

    </script>
    <%block name="endscripts">
    </%block>
</body>
</html>
