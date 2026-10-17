<?php
/* Jednorázově (tools/server/run.sh): mode=export vypíše JSON řetězců slovníku TranslatePress (cs → de) pro danou stránku,
   mode=import načte wp-content/claude-trp.json {"original": "překlad", ...} a uloží překlady jako ruční (status 2);
   s add=1 chybějící originály vloží jako nové řádky.
   Parametr lang=de_DE (výchozí). */
add_action( 'wp_loaded', function () {
	if ( ( $_GET['claude'] ?? '' ) !== '__TOKEN__' ) return;
	@set_time_limit( 85 ); header( 'Content-Type: application/json' );
	global $wpdb; $lang = strtolower( preg_replace( '/[^A-Za-z_]/', '', $_GET['lang'] ?? 'de_DE' ) );
	$t = $wpdb->prefix . 'trp_dictionary_cs_cz_' . $lang;
	if ( ( $_GET['mode'] ?? 'export' ) === 'export' ) {
		$where = empty( $_GET['all'] ) ? 'WHERE status = 0' : '';
		echo wp_json_encode( $wpdb->get_results( "SELECT id, original, translated, status FROM $t $where ORDER BY id", ARRAY_A ), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ); exit;
	}
	$f = WP_CONTENT_DIR . '/claude-trp.json'; $map = json_decode( (string) file_get_contents( $f ), true ); @unlink( $f );
	$n = 0; $miss = array();
	foreach ( (array) $map as $orig => $tr ) {
		$id = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $t WHERE BINARY original = %s", $orig ) );
		if ( ! $id ) {
			// řetězce, které TranslatePress sám nezaregistruje (titulek, meta popisy, alt obrázků) – vložit rovnou
			if ( ! empty( $_GET['add'] ) ) { $n += (int) $wpdb->insert( $t, array( 'original' => $orig, 'translated' => $tr, 'status' => 2, 'block_type' => 0 ) ); continue; }
			$miss[] = $orig; continue;
		}
		$n += (int) $wpdb->update( $t, array( 'translated' => $tr, 'status' => 2 ), array( 'id' => $id ) );
	}
	if ( class_exists( 'Cache_Enabler' ) ) Cache_Enabler::clear_complete_cache();
	echo wp_json_encode( array( 'ulozeno' => $n, 'nenalezeno' => $miss ), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ); exit;
} );
