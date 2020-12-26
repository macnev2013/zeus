$("#sidebarCollapse").on("click", function() {
    $("#content").toggleClass("active");
    $("#sidebar").toggleClass("active");
});


$("#jenkins-users-cb").on("click", function() {
if($("#jenkins-users-cb").is(':checked'))
    $("#jenkins-users-input").toggleClass("d-none");
else
    $("#jenkins-users-input").toggleClass("d-none");
});