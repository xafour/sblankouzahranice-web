<?php
/* Jednorázový mu-plugin (nahrává tools/deploy.sh). Čte wp-content/claude-payload.json:
   { design: {...design-system.json}, css: "...", page: {slug, title, source_id, elements:[...]} }
   1) záloha kitu do option, 2) přidá/aktualizuje globální barvy+písma sbz_* (ostatní nechá),
   3) písma Google načítat lokálně, 4) blok CSS mezi značkami BEGIN/END sbz, 5) vytvoří/aktualizuje kopii stránky. */
add_action( 'wp_loaded', function () {
	if ( ( $_GET['claude'] ?? '' ) !== '__TOKEN__' ) return;
	@set_time_limit( 300 ); header( 'Content-Type: application/json' );
	$f = WP_CONTENT_DIR . '/claude-payload.json';
	$p = json_decode( (string) file_get_contents( $f ), true ); @unlink( $f );
	if ( ! $p ) { echo wp_json_encode( array( 'error' => 'payload' ) ); exit; }
	$E = \Elementor\Plugin::$instance; $r = array();
	$u = get_user_by( 'login', 'claude-editor' ); if ( $u ) wp_set_current_user( $u->ID ); // Elementor ukládá jen s oprávněním
	$r['user'] = get_current_user_id();

	// 1+2) kit
	$kit_id = (int) get_option( 'elementor_active_kit' );
	$settings = (array) get_post_meta( $kit_id, '_elementor_page_settings', true );
	add_option( 'claude_backup_kit_' . $kit_id . '_' . gmdate( 'Ymd_His' ), $settings, '', false );
	$merge = function ( $list, $new ) { $by = array(); foreach ( (array) $list as $i => $x ) $by[ $x['_id'] ] = $i; foreach ( $new as $n ) { if ( isset( $by[ $n['_id'] ] ) ) $list[ $by[ $n['_id'] ] ] = $n; else $list[] = $n; } return array_values( $list ); };
	$colors = array_map( fn( $c ) => array( '_id' => $c['_id'], 'title' => $c['title'], 'color' => $c['color'] ), $p['design']['colors'] );
	$px = fn( $v ) => array( 'unit' => 'px', 'size' => $v, 'sizes' => array() );
	$typo = array();
	foreach ( $p['design']['typography'] as $t ) {
		$x = array( '_id' => $t['_id'], 'title' => $t['title'], 'typography_typography' => 'custom', 'typography_font_family' => $t['family'], 'typography_font_weight' => $t['weight'],
			'typography_font_size' => $px( $t['size'] ), 'typography_font_size_tablet' => $px( $t['size_tablet'] ), 'typography_font_size_mobile' => $px( $t['size_mobile'] ),
			'typography_line_height' => array( 'unit' => 'em', 'size' => $t['lh'], 'sizes' => array() ) );
		if ( ! empty( $t['transform'] ) ) $x['typography_text_transform'] = $t['transform'];
		if ( ! empty( $t['letter_spacing'] ) ) $x['typography_letter_spacing'] = $px( $t['letter_spacing'] );
		$typo[] = $x;
	}
	$settings['custom_colors'] = $merge( $settings['custom_colors'] ?? array(), $colors );
	$settings['custom_typography'] = $merge( $settings['custom_typography'] ?? array(), $typo );
	$kit = $E->documents->get( $kit_id, false );
	$r['kit_saved'] = $kit->save( array( 'settings' => $settings ) );
	$r['kit'] = array( 'id' => $kit_id, 'colors' => count( $settings['custom_colors'] ), 'typography' => count( $settings['custom_typography'] ) );

	// 3) lokální Google písma (GDPR + rychlost)
	update_option( 'elementor_local_google_fonts', '1' );

	// 4) CSS blok
	$css = (string) wp_get_custom_css();
	$css = preg_replace( '~/\* ===== BEGIN sbz design system.*?===== END sbz design system ===== \*/\s*~s', '', $css );
	$res = wp_update_custom_css_post( trim( $css . "\n\n" . $p['css'] ) );
	$r['css'] = is_wp_error( $res ) ? $res->get_error_message() : strlen( wp_get_custom_css() );

	// 5) stránka (kopie, původní se nemění)
	$pg = $p['page']; $src = (int) $pg['source_id'];
	$existing = get_page_by_path( $pg['slug'], OBJECT, 'page' );
	$id = $existing ? $existing->ID : wp_insert_post( array( 'post_type' => 'page', 'post_status' => 'publish', 'post_title' => $pg['title'], 'post_name' => $pg['slug'], 'post_author' => get_post_field( 'post_author', $src ) ) );
	if ( is_wp_error( $id ) ) { $r['page_error'] = $id->get_error_message(); echo wp_json_encode( $r ); exit; }
	if ( ! $existing ) foreach ( get_post_meta( $src ) as $k => $v ) if ( strpos( $k, '_kad' ) === 0 || $k === '_wp_page_template' ) update_post_meta( $id, $k, maybe_unserialize( $v[0] ) );
	update_post_meta( $id, '_elementor_edit_mode', 'builder' );
	update_post_meta( $id, '_yoast_wpseo_meta-robots-noindex', '1' );
	$doc = $E->documents->get( $id, false );
	$r['page_saved'] = $doc->save( array( 'elements' => $pg['elements'], 'settings' => array( 'hide_title' => 'yes' ) ) );
	$E->files_manager->clear_cache();
	if ( class_exists( 'Cache_Enabler' ) ) Cache_Enabler::clear_complete_cache();
	$r['page'] = array( 'id' => $id, 'created' => ! $existing, 'url' => get_permalink( $id ) );
	echo wp_json_encode( $r ); exit;
} );
