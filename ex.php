<?php
$command="python ex.py ";
exec($command,$output);
print "$output[0]\n";
print "$output[1]\n";
?>