<?php
/* Zapíše Blankou schválené SEO texty z tools/seo/schvaleno.json (vloží se při spuštění místo __DATA__).
   krok=nahled – jen vypíše, co by se změnilo; krok=zapis – zapíše. Původní hodnoty uloží do option sbz_seo_zaloha. */
add_action( 'wp_loaded', function () {
	if ( ( $_GET['claude'] ?? '' ) !== '__TOKEN__' ) return;
	@set_time_limit( 85 ); header( 'Content-Type: text/plain; charset=utf-8' );
	global $wpdb;
	$d = json_decode( base64_decode( '__DATA__' ), true );
	$zapis = ( $_GET['krok'] ?? 'nahled' ) === 'zapis';
	$zaloha = (array) get_option( 'sbz_seo_zaloha', array() );
	$najdi = function ( $cesta ) {
		if ( preg_match( '#^/category/(?:.+/)?([^/]+)/$#', $cesta, $m ) ) { $t = get_term_by( 'slug', $m[1], 'category' ); return $t ? array( 'term', $t->term_id ) : null; }
		if ( strpos( $cesta, '/elementor-hf/' ) === 0 ) { $p = get_page_by_path( basename( $cesta ), OBJECT, 'elementor-hf' ); return $p ? array( 'post', $p->ID ) : null; }
		$p = get_page_by_path( trim( $cesta, '/' ), OBJECT, array( 'page', 'post' ) );
		return $p ? array( 'post', $p->ID ) : null;
	};
	$nastav = function ( $cesta, $pole, $hodnota ) use ( $najdi, $zapis, &$zaloha ) {
		$c = $najdi( $cesta );
		if ( ! $c ) { echo "!! nenalezeno: $cesta\n"; return; }
		if ( $c[0] === 'term' ) {
			$tm = get_option( 'wpseo_taxonomy_meta', array() );
			$klic = array( 'title' => 'wpseo_title', 'metadesc' => 'wpseo_desc', 'meta-robots-noindex' => 'wpseo_noindex' )[ $pole ];
			$stare = $tm['category'][ $c[1] ][ $klic ] ?? '';
			if ( $pole === 'meta-robots-noindex' ) $hodnota = 'noindex';
			printf( "%s [%s] %s → %s\n", $cesta, $pole, $stare ?: '(prázdné)', $hodnota );
			if ( $zapis ) { $zaloha[ "term:{$c[1]}:$klic" ] ??= $stare; $tm['category'][ $c[1] ][ $klic ] = $hodnota; update_option( 'wpseo_taxonomy_meta', $tm ); }
			return;
		}
		$stare = get_post_meta( $c[1], "_yoast_wpseo_$pole", true );
		printf( "%s (#%d) [%s] %s → %s\n", $cesta, $c[1], $pole, $stare === '' ? '(prázdné)' : $stare, $hodnota );
		if ( $zapis ) { $zaloha[ "post:{$c[1]}:$pole" ] ??= $stare; update_post_meta( $c[1], "_yoast_wpseo_$pole", $hodnota ); }
	};
	foreach ( $d['titulky'] as $c => $v ) $nastav( $c, 'title', $v );
	foreach ( $d['popisy'] as $c => $v ) $nastav( $c, 'metadesc', $v );
	foreach ( $d['skryt'] as $c ) $nastav( $c === '/sample-page/' ? '/ochrana-osobnich-udaju/' : $c, 'meta-robots-noindex', '1' );

	// popisky obrázků: podle názvu souboru (bez velikosti a přípony – část PNG je teď JPG)
	foreach ( $d['alt'] as $stem => $alt ) {
		$ids = $wpdb->get_col( $wpdb->prepare( "SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key='_wp_attached_file' AND meta_value REGEXP %s", '(^|/)' . preg_quote( $stem ) . '(-scaled|-e[0-9]+)?\\.(png|jpe?g)$' ) );
		if ( ! $ids ) { echo "!! obrázek nenalezen: $stem\n"; continue; }
		foreach ( $ids as $id ) {
			$stare = get_post_meta( $id, '_wp_attachment_image_alt', true );
			printf( "alt #%d %s: %s → %s\n", $id, $stem, $stare === '' ? '(prázdné)' : $stare, $alt );
			if ( $zapis ) { $zaloha[ "alt:$id" ] ??= $stare; update_post_meta( $id, '_wp_attachment_image_alt', $alt ); }
		}
	}

	// nadpis v textu stránky (obsah i data Elementoru)
	foreach ( $d['nadpisy'] as $c => list( $z, $na ) ) {
		$p = $najdi( $c ); if ( ! $p ) continue;
		$el = get_post_meta( $p[1], '_elementor_data', true ); $obsah = get_post_field( 'post_content', $p[1] );
		$zj = trim( wp_json_encode( $z ), '"' ); $naj = trim( wp_json_encode( $na ), '"' ); // Elementor ukládá diakritiku jako \u00e1
		if ( strpos( $el, $zj ) === false ) { $zj = trim( json_encode( $z ), '"' ); $naj = trim( json_encode( $na ), '"' ); }
		printf( "nadpis %s: „%s“ → „%s“ (Elementor %d×, obsah %d×)\n", $c, $z, $na, substr_count( $el, $zj ), substr_count( $obsah, $z ) );
		if ( $zapis ) {
			update_option( 'sbz_seo_zaloha_el_' . $p[1], $el, false );
			$wpdb->update( $wpdb->postmeta, array( 'meta_value' => str_replace( $zj, $naj, $el ) ), array( 'post_id' => $p[1], 'meta_key' => '_elementor_data' ) );
			$wpdb->update( $wpdb->posts, array( 'post_content' => str_replace( $z, $na, $obsah ) ), array( 'ID' => $p[1] ) );
			clean_post_cache( $p[1] );
		}
	}
	foreach ( $d['smazat'] as $c ) { $p = $najdi( $c ); if ( $p ) { echo "do koše: $c (#{$p[1]})\n"; if ( $zapis ) wp_trash_post( $p[1] ); } }

	if ( $zapis ) {
		update_option( 'sbz_seo_zaloha', $zaloha, false );
		$wpdb->query( "DELETE FROM {$wpdb->postmeta} WHERE meta_key='_elementor_element_cache'" );
		\Elementor\Plugin::$instance->files_manager->clear_cache();
		if ( class_exists( 'Cache_Enabler' ) ) Cache_Enabler::clear_complete_cache();
		wp_cache_flush(); echo "ZAPSÁNO\n";
	}
	exit;
} );
