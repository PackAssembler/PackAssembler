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
