<?php
/**
 * Plugin Name: sbz – němčina jen na vybraných stránkách
 * Description: TranslatePress překládá celý web, ale přeložené jsou jen stránky v seznamu níže (Blanka 17. 10. 2026:
 *              Domů, Do Rakouska, Výlety v Rakousku, Projekt v médiích, Spolupráce, Reference + ukázka Den ve Vídni).
 *              – Na těchto stránkách je v menu přepínač CZ | DE.
 *              – Ostatní stránky v němčině (/de/…) přesměruje na českou verzi a Google o nich nedostane odkaz (hreflang).
 *              Přidání stránky: doplnit její ID do sbz_de_stranky(). Vrácení: smazat tento soubor.
 * Version: 1.0
 */

defined( 'ABSPATH' ) || exit;

function sbz_de_stranky() {
	// 97 Domů, 19142 Do Rakouska, 12734 Výlety v Rakousku, 22296 Projekt v médiích, 14873 Spolupráce, 23091 Reference,
	// 25033 Den ve Vídni (nový design, ukázka)
	return array( 97, 19142, 12734, 22296, 14873, 23091, 25033 );
}

function sbz_de_povoleno( $id = null ) {
	if ( $id === null ) {
		if ( is_front_page() ) return true;
		if ( ! is_page() ) return false;
		$id = get_queried_object_id();
	}
	return in_array( (int) $id, sbz_de_stranky(), true );
}

function sbz_jazyk() {
	global $TRP_LANGUAGE;
	return $TRP_LANGUAGE ?? 'cs_CZ';
}

function sbz_url_jazyka( $jazyk ) {
	if ( ! class_exists( 'TRP_Translate_Press' ) ) return '';
	return TRP_Translate_Press::get_trp_instance()->get_component( 'url_converter' )->get_url_for_language( $jazyk ); // s #TRPLINKPROCESSED, aby odkaz TranslatePress nepřepsal
}

// nepřeložená stránka v němčině → česká verze
add_action( 'template_redirect', function () {
	if ( sbz_jazyk() !== 'de_DE' || is_admin() || isset( $_GET['trp-edit-translation'] ) || sbz_de_povoleno() ) return;
	$cz = str_replace( '#TRPLINKPROCESSED', '', sbz_url_jazyka( 'cs_CZ' ) );
	if ( $cz ) { wp_safe_redirect( $cz, 302, 'sbz-jazyky' ); exit; }
}, 1 );

// hreflang (odkaz pro Google na jazykovou verzi) jen u přeložených stránek
add_filter( 'trp-exclude-hreflang', function ( $vyloucit, $url ) {
	$id = untrailingslashit( $url ) === untrailingslashit( home_url() ) ? (int) get_option( 'page_on_front' ) : url_to_postid( $url );
	return $vyloucit || ! sbz_de_povoleno( $id );
}, 10, 2 );

// přepínač CZ | DE na konci hlavního menu (počítač i mobil), jen na přeložených stránkách
add_filter( 'wp_nav_menu_items', function ( $items, $args ) {
	if ( ! in_array( $args->theme_location ?? '', array( 'primary', 'mobile' ), true ) || ! sbz_de_povoleno() ) return $items;
	$akt = sbz_jazyk();
	$odkaz = function ( $jazyk, $text, $nazev ) use ( $akt ) {
		$a = $jazyk === $akt ? ' aria-current="true" class="sbz-jazyk-akt"' : '';
		return '<a href="' . esc_url( sbz_url_jazyka( $jazyk ) ) . '" hreflang="' . substr( $jazyk, 0, 2 ) . '" lang="' . substr( $jazyk, 0, 2 ) . '" title="' . esc_attr( $nazev ) . '"' . $a . ' data-no-translation>' . $text . '</a>';
	};
	return $items . '<li class="menu-item sbz-jazyk">' . $odkaz( 'cs_CZ', 'CZ', 'Česky' ) . '<span aria-hidden="true">|</span>' . $odkaz( 'de_DE', 'DE', 'Deutsch' ) . '</li>';
}, 10, 2 );

add_action( 'wp_head', function () {
	if ( ! sbz_de_povoleno() ) return;
	echo '<style id="sbz-jazyky">.sbz-jazyk{display:flex;align-items:center;gap:6px}.sbz-jazyk>a{font-weight:600}'
		. '.sbz-jazyk>a.sbz-jazyk-akt{color:#145A38!important;text-decoration:underline;text-underline-offset:4px}.sbz-jazyk>span{opacity:.5}'
		// počítač: vpravo nahoře nad menu, aby se menu nezalomilo na dva řádky
		. '#primary-menu{position:relative}#primary-menu>.sbz-jazyk{position:absolute;right:0;top:-38px;font-size:14px}'
		. '#primary-menu>.sbz-jazyk>a{padding:4px 2px!important}'
		// mobil: bez rámečků, vedle sebe
		. '#mobile-menu .sbz-jazyk{padding:14px 0;gap:14px;border:0}#mobile-menu .sbz-jazyk>a{border:0!important;background:none!important;width:auto!important;padding:4px 6px!important;font-size:17px;color:#fff!important}'
		. '#mobile-menu .sbz-jazyk>a.sbz-jazyk-akt{color:#DEE5A3!important}#mobile-menu .sbz-jazyk>span{color:#fff}'
		. '</style>' . "\n";
}, 99 );
