<?php
/* Jednorázově (přes tools/server/run.sh): 1) nadpisy H1 podle wp-content/claude-h1.json [{path,text,from}],
   2) opraví staré odkazy (www./http://, test.subdoména, /kontakt, /viden-s-podporou) ve všech stránkách a příspěvcích.
   Původní _elementor_data se zálohuje do option claude_backup_h1links_<id>. Parametr dry=1 jen vypíše, co by se změnilo. */
add_action( 'wp_loaded', function () {
	if ( ( $_GET['claude'] ?? '' ) !== '__TOKEN__' ) return;
	@set_time_limit( 85 ); header( 'Content-Type: application/json' );
	$dry = ! empty( $_GET['dry'] ); $r = array( 'h1' => array(), 'odkazy' => array() );
	$norm = fn( $s ) => trim( preg_replace( '/\s+/u', ' ', html_entity_decode( wp_strip_all_tags( (string) $s ) ) ) );
	// jen hodnoty odkazů (pole url v Elementoru, href v HTML) – text s adresou webu zůstane, jak je
	$fix_one = function ( $u ) {
		if ( ! preg_match( '#^\s*(?:https?://)?(www\.)?(test\.)?sblankouzahranice\.eu(/[^\s]*)?\s*$#i', $u, $m ) ) return $u;
		$path = $m[3] ?? '/'; $path = $path === '' ? '/' : $path;
		if ( ! empty( $m[2] ) && preg_match( '#^/vylety/?$#', $path ) ) return '/vylety/';
		if ( preg_match( '#^/kontakt/?$#', $path ) ) return '/kontakt-s-blankou-za-hranice/';
		if ( preg_match( '#^/viden-s-podporou/?$#', $path ) ) return '/viden-s-podporou-za-zady/';
		return $path;
	};
	$fix_html = fn( $h ) => preg_replace_callback( '#(href=)(\\\\?["\'])(.*?)\2#i', fn( $m ) => $m[1] . $m[2] . $fix_one( $m[3] ) . $m[2], $h );
	$fix_url = function ( $s ) use ( $fix_html ) { return $fix_html( $s ); };
	$fix_tree = function ( &$a ) use ( &$fix_tree, $fix_one, $fix_html ) {
		foreach ( $a as $k => &$v ) {
			if ( is_array( $v ) ) $fix_tree( $v );
			elseif ( is_string( $v ) ) $v = $k === 'url' ? $fix_one( $v ) : ( stripos( $v, 'href=' ) !== false ? $fix_html( $v ) : $v );
		}
	};
	$walk = function ( &$els, callable $fn ) use ( &$walk ) { foreach ( $els as &$e ) { $fn( $e ); if ( ! empty( $e['elements'] ) ) $walk( $e['elements'], $fn ); } };
	$map = array(); $f = WP_CONTENT_DIR . '/claude-h1.json';
	if ( is_readable( $f ) ) { foreach ( json_decode( file_get_contents( $f ), true ) as $x ) $map[ $x['path'] ] = $x; @unlink( $f ); }
	$front = (int) get_option( 'page_on_front' );
	$ids = get_posts( array( 'post_type' => array( 'page', 'post', 'elementor_library' ), 'post_status' => 'publish', 'numberposts' => -1, 'fields' => 'ids' ) );
	foreach ( $ids as $id ) {
		$path = $id === $front ? '' : trim( (string) wp_make_link_relative( get_permalink( $id ) ), '/' );
		$raw = get_post_meta( $id, '_elementor_data', true ); $data = $raw ? json_decode( $raw, true ) : null;
		$changed = false;
		if ( is_array( $data ) ) {
			if ( isset( $map[ $path ] ) ) {
				$want = $map[ $path ]; $done = false;
				$walk( $data, function ( &$e ) use ( $want, $norm, &$done ) {
					if ( $done || ( $e['widgetType'] ?? '' ) !== 'heading' ) return;
					$t = $norm( $e['settings']['title'] ?? '' ); $tag = $e['settings']['header_size'] ?? 'h2';
					if ( $tag === $want['from'] && mb_strpos( $t, $norm( $want['text'] ) ) === 0 ) { $e['settings']['header_size'] = 'h1'; $done = true; }
				} );
				$r['h1'][ $path ] = $done ? 'ok' : 'NENALEZENO';
				$changed = $changed || $done;
				unset( $map[ $path ] );
			}
			if ( $path === 'viden-nejzelenejsi-mesto-sveta' ) { $n = 0;
				$walk( $data, function ( &$e ) use ( &$n, &$changed ) { if ( ( $e['widgetType'] ?? '' ) === 'heading' && ( $e['settings']['header_size'] ?? '' ) === 'h1' && ++$n > 1 ) { $e['settings']['header_size'] = 'h2'; $changed = true; } } );
				$r['h1'][ $path ] = "druhý H1 → H2 ($n)"; }
			$json = wp_json_encode( $data ); $copy = $data; $fix_tree( $copy ); $fixed = wp_json_encode( $copy );
			if ( $fixed !== $json ) { $r['odkazy'][ $path ] = 'elementor'; $changed = true; $data = json_decode( $fixed, true ); }
			if ( $changed && ! $dry ) {
				add_option( 'claude_backup_h1links_' . $id, $raw, '', false );
				update_post_meta( $id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
				delete_post_meta( $id, '_elementor_element_cache' );
			}
		}
		$c = get_post_field( 'post_content', $id ); $c2 = $fix_url( $c );
		if ( $c2 !== $c ) { $r['odkazy'][ $path ] = ( $r['odkazy'][ $path ] ?? '' ) . ' obsah'; if ( ! $dry ) wp_update_post( array( 'ID' => $id, 'post_content' => $c2 ) ); }
	}
	foreach ( $map as $p => $x ) $r['h1'][ $p ] = 'stránka nenalezena';
	if ( ! $dry ) { \Elementor\Plugin::$instance->files_manager->clear_cache(); if ( class_exists( 'Cache_Enabler' ) ) Cache_Enabler::clear_complete_cache(); }
	echo wp_json_encode( $r, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ); exit;
} );
