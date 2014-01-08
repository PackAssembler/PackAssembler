<%inherit file="base.mak"/>
<h2>Frequently Asked Questions</h2>
<hr>

<h3>Overview</h3>
<h4>Isn't this kind of like &lt;insert project name here&gt;?</h4>
Surely, the goal this site must be similar to other projects but we believe there is no website with the greatest emphasis on Pack creation.

<h4>This sounds great, but how exactly do I use this site?</h4>
Try the <a href="${request.route_url('gettingstarted')}">Getting Started</a> page.

<h4>So, do you support anything below 1.6.2? I see other options but can't make them work.</h4>
Support for anything under 1.5.2 is deprecated. We will be removing it from the site soon.


<h3>Mods</h3>
<h4>Why can't I add any mods?</h4>
In order to ensure that we don't have duplicates or mods with no permissions defined, we have made a decision to only allow contributors to add mods.

<h4 id="permissions">How do permissions work?</h4>
When assesing the legality of having a copyrighted mod on our servers, we assume:
<ol>
    <li>If no permission is specified for this unique situation, one must follow restrictions given for 'modpacks'.</li>
    <li>No license given (or none which applies) by the creator means all rights reserved.</li>
</ol>
If the mod author does not allow uploading directly to the site according to the policy above, there is a second option: One may add a mod version by url. \
However, this is not allowed if the mod author specifically disallows the practice. In that case, the mod doesn't deserve to be used.
<strong>If a mod is found without a satisfactory permission description all mod versions will be deleted.</strong>

<h4>Do I have to use quotes when I'm quoting the author?</h4>
No, you do not. We can assume:
<ul>
    <li>Links either point to the author's permission to use the mod or to a license text</li>
    <li>Statements were originally made by the author</li>
</ul>
In other cases, please specify.


<h3>Packs</h3>
<h4>What is the difference between using this site and creating a "modpack" manually?</h4>
There are many benefits to using this site rather than manually doing the work, including
<ol>
	<li>Easier - no need to download any mods, host your own "modpack", or think about permissions</li>
	<li>Compatible - when creating a Pack Build, you will be informed of any incompatibilities with your version of Forge or Minecraft</li>
	<li>Standardized - this website has a standard format for every Pack, ensuring all software built for our platform will be compatible with your Pack</li>
</ol>
<h4>Why do my pack builds have development versions?</h4>
Either you checked the 'Use Development Versions' checkbox on your Pack's settings or there is no other version available.


<h3>Other</h3>
<h4>How can I change my avatar?</h4>
Visit <a href="http://gravatar.com/">Gravatar</a>.
<h4>My things got deleted!</h4>
In order to keep things clean, we have opted to delete useless, empty, and inactive objects. If you don't want your things to be deleted, use the site correctly.

<h4 id="groups">So, what exactly are these user groups that I see on profile pages?</h4>
There are currently four types of users: user, contributor, moderator, and administrator. Each has specific permissions, limiting what they can do. Permissions are comulative.
<dl class="well">
    <dt>User</dt><dd>Can create and edit their Packs and Servers</dd>
    <dt>Contributor</dt><dd>Can create and edit their Mods</dd>
    <dt>Moderator</dt><dd>Can edit other people's things</dd>
    <dt>Admin</dt><dd>Can change user's group</dd>
</dl>