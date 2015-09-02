<?php 
/*
 * Run the Sender in the background as thread
 * 
 * To run this script you have to install pthreads manually
 * 
 * 
 */
require_once 'BayEOSGatewayClient.php';
$path='/tmp/PHP-Delay-Test-ultrabook-tmp-WS0.05-M2560.0';
$name="PHP-Delay-Test-ultrabook-tmp-WS0.05-M2560.0";
$url="http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveMatrix";
$max_chunk = 2560;
$writer_sleep = 0.05;

//Create a BayEOSWriter
$w = new BayEOSWriter($path, $max_chunk);
$w->saveMessage("testtimedelay.php started");

// //Create a BayEOSSender and start it as thread
// class SenderThread extends Thread {
// 	public function run() {
// 		$s = new BayEOSSender($GLOBALS['path'],$GLOBALS['name'],$GLOBALS['url']);
// 	}
// }
// $s_thread=new SenderThread();
// $s_thread->start();
//mktime(date('H'), date('i'), date('s'), date('m'), date('d'), date('y'))

$today = mktime(0, 0, 0, date('m'), date('d'), date('y'));
$start = microtime(true);
$t_run = microtime(true) - $start;
echo $today, PHP_EOL;
echo $start, PHP_EOL;
echo $t_run, PHP_EOL;
echo (microtime(true)-$today);

while($t_run <= 1000){
	$t = microtime(true);
	$t_run = $t - $start;
	$w->save(array($t_run, ($t-$today)));
	sleep($writer_sleep);
}

$s = new BayEOSSender($path,$name,$url);

while($t_run <= 1500){
	$c = $s->send();
	$t_run = $t - $start;
	if($c){
		echo "Successfully sent $c frames\n";
	}
	sleep(0.1);	
}


?>
