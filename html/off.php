<?php
system ( "gpio -g write 14 0");
system ( "gpio -g write 15 1");
header("Location:index.html");
system ( "cp status_off.html status.html");
?>

