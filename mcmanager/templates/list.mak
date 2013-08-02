<%def name="head()">
<div class="row">
    <div class="span8">
        <h2>${title}</h2>
    </div>
    <div class="span4">
        <div class="pull-right">
            <form class="form-search" method="GET" action="${request.url}">
                <input type="text" name="txtSearch" class="input-medium search-query">
                <button type="submit" name="btnSubmit" class="btn">Search</button>
            </form>
        </div>
    </div>
</div>
</%def>