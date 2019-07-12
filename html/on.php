<?php
system ( "gpio -g write 14 1");
system ( "gpio -g write 15 0");
header("Location:index.html");
system ( "cp status_on.html status.html");
?>

