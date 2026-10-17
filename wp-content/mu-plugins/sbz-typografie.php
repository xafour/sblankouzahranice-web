<?php
/**
 * Plugin Name: sbz – česká typografie (zalamování řádků)
 * Description: Jednopísmenné předložky a spojky (a, i, k, o, s, u, v, z) i krátké (do, nad, pod, na, že, ať…) nezůstanou na konci řádku – za ně se vloží pevná mezera.
 *              Stejně se drží pohromadě číslo + jednotka (6 km, 40 €) a pomlčka nezačne nový řádek. Nadpisy mají vyrovnané řádky,
 *              odstavce nekončí jedním osamoceným slovem (CSS text-wrap). Platí pro celý web a všechny šířky obrazovky.
 *              Upravuje jen text mezi značkami HTML, ne skripty, styly, atributy ani formuláře. Vrácení: smazat tento soubor.
 * Version: 1.2 – jen české stránky (na /de/ by pevné mezery vadily překladům TranslatePressu); 1.1 – i krátké předložky a spojky
 */

defined( 'ABSPATH' ) || exit;

function sbz_typo_text( $t ) {
	if ( trim( $t ) === '' ) return $t;
	$nb = "\u{00A0}";
	// jednopísmenná slova (norma) + krátké předložky a spojky (přání Blanky): za ně pevná mezera, takže nezůstanou na konci řádku
	$slova = 'a|i|k|o|s|u|v|z|do|od|ode|na|nad|pod|po|za|ze|ve|ke|ku|se|pro|při|před|bez|přes|že|ať|ani|než|ale|aby|až|či';
	for ( $i = 0; $i < 2; $i++ ) { // dvakrát kvůli „a v Praze“, „že do…“
		$t = preg_replace( '/(^|[\s\x{00A0}(„"“\[])(' . $slova . ')[ \t\r\n]+(?=\S)/iu', '$1$2' . $nb, $t );
	}
	// číslo + jednotka / měna / procenta
	$t = preg_replace( '/(\d)[ \t]+(km|m|cm|kg|g|l|h|min|hod\.?|let|dní|dny|osob|€|EUR|Euro|Kč|CZK|%|°C)(?![\p{L}\d])/u', '$1' . $nb . '$2', $t );
	// pomlčka nezačíná řádek
	$t = preg_replace( '/[ \t]+([–—])/u', $nb . '$1', $t );
	return $t === null ? '' : $t;
}

function sbz_typo_html( $html ) {
	if ( stripos( $html, '<html' ) === false ) return $html;
	// skripty, styly, formulářová pole, kód a ikony nejdřív odložit celé (skripty můžou obsahovat znaky < a >)
	$schovano = array();
	$html2 = preg_replace_callback( '#<(script|style|textarea|pre|code|svg|noscript|title)\b.*?</\1\s*>|<!--.*?-->#is', function ( $m ) use ( &$schovano ) {
		$schovano[] = $m[0];
		return "\x01" . ( count( $schovano ) - 1 ) . "\x02";
	}, $html );
	if ( $html2 === null ) return $html;
	$casti = preg_split( '/(<[^>]*>)/', $html2, -1, PREG_SPLIT_DELIM_CAPTURE );
	$out = '';
	foreach ( $casti as $c ) {
		$out .= ( $c !== '' && $c[0] === '<' ) ? $c : preg_replace_callback( '/[^\x01\x02]+(?=\x01|$)|[^\x01\x02]+/', fn( $m ) => sbz_typo_text( $m[0] ), $c );
	}
	return preg_replace_callback( '/\x01(\d+)\x02/', fn( $m ) => $schovano[ (int) $m[1] ], $out );
}

add_action( 'template_redirect', function () {
	if ( is_admin() || wp_doing_ajax() || is_feed() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) return;
	if ( isset( $_GET['elementor-preview'] ) || isset( $_GET['sbz-bez-typo'] ) ) return;
	global $TRP_LANGUAGE;
	if ( ! empty( $TRP_LANGUAGE ) && $TRP_LANGUAGE !== 'cs_CZ' ) return; // česká pravidla jen pro češtinu
	ob_start( 'sbz_typo_html' );
}, 2 );

add_action( 'wp_head', function () {
	echo "<style id=\"sbz-typografie\">h1,h2,h3,h4,.elementor-heading-title{text-wrap:balance}p,li,.elementor-testimonial-content,.elementor-icon-box-description{text-wrap:pretty}</style>\n";
}, 99 );
