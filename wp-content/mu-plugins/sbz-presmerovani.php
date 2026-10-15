<?php
/**
 * Plugin Name: sbz – přesměrování starých adres
 * Description: Stará adresa → nová (301), aby nefungující odkazy a záložky lidí i Googlu vedly na správnou stránku.
 * Version: 1.0
 */

defined( 'ABSPATH' ) || exit;

add_action( 'template_redirect', function () {
	if ( ! is_404() ) return;
	$mapa = array(
		'sample-page' => '/ochrana-osobnich-udaju/', // 15. 10. 2026: stránka Ochrana osobních údajů měla výchozí adresu WordPressu
	);
	$cesta = trim( (string) parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ), '/' );
	if ( isset( $mapa[ $cesta ] ) ) { wp_safe_redirect( home_url( $mapa[ $cesta ] ), 301 ); exit; }
} );
