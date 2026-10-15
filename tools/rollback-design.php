<?php
/* Návrat redesignu na sandboxu (jednorázový mu-plugin, spouští se stejně jako deploy):
   odebere globální barvy/písma sbz_* z kitu, odstraní CSS blok sbz a přesune kopii stránky do koše.
   Původní stránky se redesignem nikdy neměnily, takže po tomhle je web ve stavu jako v main. */
add_action( 'wp_loaded', function () {
	if ( ( $_GET['claude'] ?? '' ) !== '__TOKEN__' ) return;
	header( 'Content-Type: application/json' );
	$u = get_user_by( 'login', 'claude-editor' ); if ( $u ) wp_set_current_user( $u->ID );
	$E = \Elementor\Plugin::$instance; $r = array();
	$kit_id = (int) get_option( 'elementor_active_kit' );
	$s = (array) get_post_meta( $kit_id, '_elementor_page_settings', true );
	foreach ( array( 'custom_colors', 'custom_typography' ) as $k ) $s[ $k ] = array_values( array_filter( (array) ( $s[ $k ] ?? array() ), fn( $x ) => strpos( $x['_id'] ?? '', 'sbz_' ) !== 0 ) );
	$r['kit_saved'] = $E->documents->get( $kit_id, false )->save( array( 'settings' => $s ) );
	$css = preg_replace( '~/\* ===== BEGIN sbz design system.*?===== END sbz design system ===== \*/\s*~s', '', (string) wp_get_custom_css() );
	wp_update_custom_css_post( trim( $css ) );
	foreach ( array( 'viden-cestovni-podpora-novy-design', 'den-ve-vidni-novy-design', 'viden-cestovni-podpora-varianta-b', 'viden-cestovni-podpora-varianta-c', 'viden-cestovni-podpora-uvod-broskev', 'viden-cestovni-podpora-uvod-oliva', 'viden-cestovni-podpora-uvod-karta', 'viden-cestovni-podpora-uvod-zelena' ) as $slug ) { $p = get_page_by_path( $slug, OBJECT, 'page' ); $r['page_trashed'][ $slug ] = $p ? (bool) wp_trash_post( $p->ID ) : 'n/a'; }
	$E->files_manager->clear_cache();
	if ( class_exists( 'Cache_Enabler' ) ) Cache_Enabler::clear_complete_cache();
	echo wp_json_encode( $r ); exit;
} );
