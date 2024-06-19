document.getElementById("sign_in_with_email").addEventListener("click", displayDiv);
function displayDiv() {
	document.getElementById("email_form").style.display = "block";
}
document.getElementById("login_button").addEventListener("click", loginForTesting);
function loginForTesting() { }


// Get references to the clickable elements
const signinWithGoogleDiv = document.getElementById("signinWithGoogle");
const googleDiv = document.getElementById("googleDiv");

// Add click event listeners to the divs
signinWithGoogleDiv.addEventListener("click", function () {
	// Redirect to /perfil when the signin_with_google div is clicked
	window.location.href = "/login_with_google";
});

googleDiv.addEventListener("click", function () {
	// Redirect to /change_user when the google_div is clicked
	window.location.href = "/login_with_google";
});