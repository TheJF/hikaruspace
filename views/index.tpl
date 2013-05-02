<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<title>{{ template_info['app_name'] }}</title>
		<link href="/libs/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
		<link type="text/css" href="styles/persona-buttons.css" rel="stylesheet" media="screen"/>
		<link type="text/css" href="styles/style.css" rel="stylesheet" media="screen"/>
		<!--[if IE]>
			<script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
		<![endif]-->
		<script src="http://code.jquery.com/jquery-latest.js"></script>
		<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js"></script>
		<script src="/libs/bootstrap/js/bootstrap.min.js"></script>
		<script src="https://login.persona.org/include.js"></script>
		<script src="/scripts/hikaruspace.js" type="text/javascript"></script>
		<script src="/scripts/persona.js" type="text/javascript"></script>
	</head>
	<body id="home">
		<div id="header">
			<span id="status">{{ template_info['app_name'] }}</span>
			<span id="observing">Observing {{ template_info['observing'] }}</span>
			<div id="menu">
				<span id="account_logged">
					{{ template_info['login_bar'] }}
            	</span>
			</div>
		</div>
		<div id="content">
			<div id="widgetbox">
           
			</div>
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
