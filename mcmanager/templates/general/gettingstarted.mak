<%inherit file="base.mak"/>
<h2>${title}</h2>
<hr>
<h3>Get Ready...</h3>
<h4>Downloading the Launcher</h4>
<p>Before being able to use most of the capability of this site you will need to download <a href="http://files.mcupdater.com/MCU-Bootstrap.jar">MCUpdater</a>.
<hr>
<h3>Packs</h3>
<h4>Creating a Pack</h4>
Click the <a href="${request.route_url('addpack')}">Add Pack</a> link on the Pack List and name your Pack.
<h4>Adding a mod to a pack</h4>
Currently, there are two ways to add mods to packs. The first (and recommended way) is to go to the mod's page and click on the dropdown labeled "Add to Pack" then select the pack which you would like the mod to be added to. The second way is to the "Add Mod to Pack" link under the mod list and enter the id of the mod.
<h4>Creating a Pack Build</h4>
In order to distribute your Pack, you must create a Pack Build. In order to do so, click the "New Build" link on your Pack's page and insert a Minecraft version, a Forge version, and a link to an optional configuration zipfile.