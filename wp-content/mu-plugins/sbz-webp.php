<?php
/**
 * Plugin Name: sbz – obrázky jako WebP
 * Description: Kde vedle obrázku existuje soubor .webp (obrazek.jpg.webp), pošle návštěvníkovi rovnou WebP – v HTML i v CSS Elementoru (obrázky na pozadí sekcí).
 *              Řeší dvě slabiny Cache Enableru: první (necachovaná) odpověď je bez WebP a CDN si ji podrží; pozadí v CSS souborech Elementoru se nepřevádí vůbec.
 *              Vrácení: smazat tento soubor a v Elementoru „Regenerovat soubory a data“.
 * Version: 1.0
 */

defined( 'ABSPATH' ) || exit;

function sbz_webp_url( $url ) {
	static $cache = array();
	if ( isset( $cache[ $url ] ) ) return $cache[ $url ];
	$up   = wp_get_upload_dir();
	$base = preg_replace( '#^https?:#', '', $up['baseurl'] );
	$rel  = preg_replace( '#^(https?:)?' . preg_quote( $base, '#' ) . '#', '', $url, 1, $n );
	$out  = $url;
	if ( $n && preg_match( '#\.(jpe?g|png)$#i', $rel ) && strpos( $rel, '..' ) === false && is_readable( $up['basedir'] . $rel . '.webp' ) ) {
		$out = $url . '.webp';
	}
	return $cache[ $url ] = $out;
}

function sbz_webp_html( $html ) {
	if ( stripos( $html, '<html' ) === false ) return $html;
	return preg_replace_callback(
		'#(?:https?:)?\\\\?/\\\\?/[^"\'\s(),]+?\\\\?/wp-content\\\\?/uploads\\\\?/[^"\'\s(),]+?\.(?:jpe?g|png)(?=[\s"\'),&]|\\\\")#i',
		function ( $m ) {
			$u = str_replace( '\\/', '/', $m[0] );
			$w = sbz_webp_url( $u );
			if ( $w === $u ) return $m[0];
			return strpos( $m[0], '\\/' ) !== false ? str_replace( '/', '\\/', $w ) : $w;
		},
		$html
	);
}

// HTML stránek (spustí se dřív než uložení do Cache Enableru, takže i první odpověď je s WebP)
add_action( 'template_redirect', function () {
	if ( is_admin() || wp_doing_ajax() || is_feed() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) return;
	if ( isset( $_GET['elementor-preview'] ) || isset( $_GET['sbz-bez-webp'] ) ) return;
	ob_start( 'sbz_webp_html' );
}, 1 );

// Obrázky na pozadí v CSS souborech Elementoru (Elementor bere adresu z knihovny médií podle ID)
add_filter( 'wp_get_attachment_image_src', function ( $image ) {
	if ( is_admin() || ! is_array( $image ) || empty( $image[0] ) ) return $image;
	$image[0] = sbz_webp_url( $image[0] );
	return $image;
} );
add_filter( 'elementor/files/css/property', function ( $value ) {
	if ( is_array( $value ) && ! empty( $value['url'] ) && is_string( $value['url'] ) ) {
		$value['url'] = sbz_webp_url( $value['url'] );
	}
	return $value;
} );
