<?php

require 'vendor/autoload.php';
use PhpParser\ParserFactory;

$code = file_get_contents($argv[1]);
$parser = (new ParserFactory)->create(ParserFactory::PREFER_PHP7);

try {
    $stmts = $parser->parse($code);

    echo json_encode($stmts, JSON_PRETTY_PRINT), "\n";
} catch (PhpParser\Error $e) {
    echo 'Parse Error: ', $e->getMessage();
}
