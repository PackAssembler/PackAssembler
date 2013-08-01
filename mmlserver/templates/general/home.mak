<%inherit file="base.mak"/>
<%block name="style">
    <style type="text/css">
        h4 [class^="icon-"]:before
        {
            font-size: 28px;
            display: inline-block;
            font-size: 28px;
            margin-right: 5px;
            text-align: center;
            vertical-align: -10%;
            width: 1.07143em;
        }
        .span4
        {
            margin-bottom: 20px;
        }
    </style>
</%block>
<div class="hero-unit">
    <h1>MC Manager</h1>
    <p>The main server for MML compatible launchers, run by the creator of MML.</p>
    <p>
        <a href="${request.route_url('about')}" class="btn btn-primary btn-large">Get Started <i class="icon-double-angle-right"></i></a>
    </p>
</div>
<div class="row">
    <div class="span4">
        <h4>
            <i class="icon-flag"></i>
            One Site, Three Functions
        </h4>
        Easily search for and download mods. Create 'Packs', collections of mods easily downloadable by our launcher. Advertise 'Servers' using those packs.
    </div>
    <div class="span4">
        <h4>
            <i class="icon-ok"></i>
            Permission Granted
        </h4>
        When making a Pack or server you will never have to think about whether you have permission to use a mod. This is done prior, when a mod is added to the index. See the about page for more information.
    </div>
    <div class="span4">
        <h4>
            <i class="icon-user"></i>
            Track Your Content
        </h4>
        We store all the Mods, Packs, and Servers you maintain and ensure you can easily find them all easily, allowing you to update any maintain them quickly so you can get on with actually playing the game or managing your server.
    </div>
</div>
<div class="row">
    <div class="span4">
        <h4>
            <i class="icon-download"></i>
            Download Mods Easily
        </h4>
        With out simple and easy to use Mod index, you will never have to look in more than one place for your mod needs! All versions at your fingertips with the requirements listed plainly.
    </div>
    <div class="span4">
        <h4>
            <i class="icon-archive"></i>
            Automatically Create Packs
        </h4>
        Never worry about permissons or compatibility when creating a package of mods again! All versioning is handled by the automatic Pack Build generator.
    </div>
    <div class="span4">
        <h4>
            <i class="icon-hdd"></i>
            Your Players, Synchronized
        </h4>
        You can quickly and easily add your server to our index and keep your users updated on your latest mods and configs with minimal configuration.
    </div>
</div>
