<%def name="head()">
<div class="row">
    <div class="col-lg-6">
        <h2>${title}</h2>
    </div>
    <div class="col-lg-6">
        <div class="pull-right">
            <form class="form-inline" method="GET" action="${request.url}">
                <div class="form-group">
                    <input type="search" name="q" class="form-control" value="${request.params['q'] if 'q' in request.params else ''}" x-webkit-speech>
                </div>
                <button type="submit" class="btn">Search</button>
            </form>
        </div>
    </div>
</div>
</%def>

<%def name="add_to_pack(packs, message='Add to Pack')">
    <a class="btn btn-primary btn-sm dropdown-toggle" data-toggle="dropdown" href="#">
        ${message}
        <span class="icon-caret-down"></span>
    </a>
    <ul class="dropdown-menu">
        % if packs:
            % for pack in packs:
            <li><a href="#" data-id="${pack.id}">${pack.name}</a></li>
            % endfor
        % else:
            <li><a href="#">You have no packs!</a></li>
        % endif
        <li class="divider"></li>
        <li><a href="${request.route_url('addpack')}" class="action-add">Add Pack</a></li>
    </ul>
</%def>

<%def name="add_to_pack_script()">
    <script type="text/javascript">
        $(document).ready(function(){
            $('[data-id]').click(function(){
                $('form').attr('action', '/packs/' + $(this).data('id') + '/addmod');
                $('form').submit();
            });
        })
    </script>
</%def>
