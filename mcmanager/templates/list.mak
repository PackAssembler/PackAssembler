<%def name="head()">
<div class="row">
    <div class="span8">
        <h2>${title}</h2>
    </div>
    <div class="span4">
        <div class="pull-right">
            <form class="form-search" method="GET" action="${request.url}">
                <input type="search" name="q" class="input-medium search-query" value="${request.params['q'] if 'q' in request.params else ''}">
                <button type="submit" class="btn">Search</button>
            </form>
        </div>
    </div>
</div>
</%def>
