function timerStart() {
        i = 10;
        var count = setInterval(function() {
            document.getElementById("timer").innerHTML = i;
            if (i == 0) {
                document.location.href = "/";
            }
            i = i - 1;
        }, 1000);
};