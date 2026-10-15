<?php
add_action( 'wp_loaded', function () {
	if ( ( $_GET['claude'] ?? '' ) !== '__TOKEN__' ) return;
	header( 'Content-Type: application/json' );
	global $wpdb;
	$out = array( 'posts' => array() );
	$types = array( 'page', 'post', 'elementor_library', 'wp_block', 'wpcode', 'wp_navigation' );
	$q = get_posts( array( 'post_type' => $types, 'post_status' => array( 'publish', 'private', 'draft', 'pending', 'future' ), 'numberposts' => -1, 'orderby' => 'ID', 'order' => 'ASC' ) );
	foreach ( $q as $p ) {
		$meta = array();
		foreach ( get_post_meta( $p->ID ) as $k => $v ) if ( strpos( $k, '_elementor' ) === 0 || strpos( $k, '_wpcode' ) === 0 || in_array( $k, array( '_wp_page_template', '_thumbnail_id', '_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_meta-robots-noindex', '_yoast_wpseo_focuskw' ), true ) ) $meta[ $k ] = maybe_unserialize( $v[0] );
		$cats = $p->post_type === 'post' ? wp_get_post_categories( $p->ID, array( 'fields' => 'names' ) ) : array();
		$out['posts'][] = array( 'ID' => $p->ID, 'type' => $p->post_type, 'status' => $p->post_status, 'has_password' => $p->post_password !== '', 'title' => $p->post_title, 'slug' => $p->post_name, 'parent' => $p->post_parent, 'date' => $p->post_date, 'modified' => $p->post_modified, 'excerpt' => $p->post_excerpt, 'content' => $p->post_content, 'categories' => $cats, 'link' => get_permalink( $p ), 'meta' => $meta );
	}
	$menus = array();
	foreach ( wp_get_nav_menus() as $m ) { $items = array(); foreach ( wp_get_nav_menu_items( $m->term_id ) as $i ) $items[] = array( 'title' => $i->title, 'url' => $i->url, 'parent' => (int) $i->menu_item_parent, 'id' => $i->ID, 'order' => $i->menu_order ); $menus[ $m->name ] = $items; }
	$out['menus'] = $menus;
	$out['custom_css'] = wp_get_custom_css();
	$out['theme'] = get_stylesheet();
	$out['theme_mods'] = get_theme_mods();
	if ( ! function_exists( 'get_plugins' ) ) require_once ABSPATH . 'wp-admin/includes/plugin.php';
	$act = (array) get_option( 'active_plugins' ); $pl = array();
	foreach ( get_plugins() as $f => $d ) $pl[] = array( 'file' => $f, 'name' => $d['Name'], 'version' => $d['Version'], 'active' => in_array( $f, $act, true ) );
	$out['plugins'] = $pl;
	$out['wp_version'] = get_bloginfo( 'version' );
	$out['settings'] = array( 'blogname' => get_option( 'blogname' ), 'blogdescription' => get_option( 'blogdescription' ), 'permalink_structure' => get_option( 'permalink_structure' ), 'page_on_front' => get_option( 'page_on_front' ), 'page_for_posts' => get_option( 'page_for_posts' ), 'WPLANG' => get_locale() );
	echo wp_json_encode( $out ); exit;
} );
