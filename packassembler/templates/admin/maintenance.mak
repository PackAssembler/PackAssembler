<%inherit file="../base.mak"/>
<%namespace name="extras" file="../extras.mak" />

${extras.flash()}
<h2>${title}</h2>
<hr>
<div>
    <h3>Actions</h3>
    <form action="" method="post">
        <input type="submit" class="btn btn-danger" name="remove_old_users" value="Remove Old Users" />
    </form>
</div>
