<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<title>Hikaruspace</title>
		<link href="/libs/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
		<link type="text/css" href="styles/persona-buttons.css" rel="stylesheet" media="screen"/>
		<link type="text/css" href="styles/style.css" rel="stylesheet" media="screen"/>
		<!--[if IE]>
			<script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
		<![endif]-->
		<script src="http://code.jquery.com/jquery-latest.js"></script>
		<script src="/libs/bootstrap/js/bootstrap.min.js"></script>
		<script src="https://login.persona.org/include.js"></script>
		<script src="/libs/hikaruspace.js" type="text/javascript"></script>
		<script src="/scripts/persona.js" type="text/javascript"></script>
	</head>
	<body id="home">
		<div id="header">
			<span id="status">Hikaruspace</span>
			<span id="observing">Observing HubCityLabs Hackerspace</span>
			<div id="menu">
				<span id="account_logged">
					{{ login_bar }}
            	</span>
			</div>
		</div>
		<div id="content">
			<span id="widget-1" class="widget">
				<span id="widget-1-title" class="widget-title">
					Door Status
				</span>
				<span id="widget-1-content" class="widget-content">
					Locked
				</span>
			</span>

			<span id="widget-2" class="widget">
				<span id="widget-2-title" class="widget-title">
					Door Last Opened
				</span>
				<span id="widget-3-content" class="widget-content">
					9:25 PM, November 16, 2012.
				</span>
			</span>

			<span id="widget-3" class="widget">
				<span id="widget-3-title" class="widget-title">
					Members currently at space
				</span>
				<span id="widget-3-content" class="widget-content">
					2/12
				</span>
			</span>

			<span id="widget-4" class="widget status_green">
				<span id="widget-4-title" class="widget-title">
					Reader # 1 Active?
				</span>
				<span id="widget-4-content" class="widget-content">
					Yes
				</span>
			</span>

			<span id="widget-5" class="widget status_red">
				<span id="widget-5-title" class="widget-title">
					Reader # 2 Active?
				</span>
				<span id="widget-5-content" class="widget-content">
					No
				</span>
			</span>

			<span id="widget-6" class="widget status_yellow">
				<span id="widget-5-title" class="widget-title">
					Nerf Turret Status
				</span>
				<span id="widget-6-content" class="widget-content">
					Standby
				</span>
			</span>
		</div>

		<form name="loginForm" id="loginForm" class="form-horizontal">
			<div id="login" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="loginLabel" aria-hidden="true">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
	    			<h3 id="loginLabel">Login</h3>
				</div>
				<div class="modal-body">
					<div class="control-group">
						<label class="control-label" for="inputUsername">Username</label>
						<div class="controls">
							<input type="text" id="inputUsername" placeholder="Username">
						</div>
					</div>
					<div class="control-group">
						<label class="control-label" for="inputPassword">Password</label>
						<div class="controls">
							<input type="password" id="inputPassword" placeholder="Password">
						</div>
					</div>
					<div class="control-group">
						<div class="controls">
							<label class="checkbox">
								<input type="checkbox"> Remember me
							</label>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<a href="#" class="btn" data-dismiss="modal">Cancel</a>
					<a href="#" class="btn btn-primary">Login</a>
				</div>
			</div>
		</form>
	</body>
</html>