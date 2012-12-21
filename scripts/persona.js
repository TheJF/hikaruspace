$(document).ready(function() {
    /* Persona Code */
    $('#signin').click(function() {
        navigator.id.request();
    });

    $('#signout').click(function () {
        navigator.id.logout();
        window.signOutLoad = true;
    });

    navigator.id.watch({
        loggedInUser: '{{ login_name }}',
        onlogin: function(assertion) {
            $.ajax({
                type: 'POST',
                url: '/auth/login',
                data: {assertion: assertion},
                success: function(res, status, xhr) { window.location.reload(); },
                error: function(xhr, status, err) { console.log("Login failure: " + err); }
            });
        },
        onlogout: function() {
            $.ajax({
                type: 'POST',
                url: '/auth/logout',
                success: function(res, status, xhr) { if (window.signOutLoad) { window.location.reload(); } },
                error: function(xhr, status, err) { console.log("Logout failure: " + err); }
            });
        }
    });
});