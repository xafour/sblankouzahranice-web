<?php
/* Jednorázově (tools/server/run.sh): nainstaluje a aktivuje TranslatePress (free) a nastaví čeština + němčina (/de/),
   bez plovoucího přepínače jazyků. Parametr step=install | settings | info. */
add_action( 'wp_loaded', function () {
	if ( ( $_GET['claude'] ?? '' ) !== '__TOKEN__' ) return;
	@set_time_limit( 85 ); header( 'Content-Type: text/plain' );
	$u = get_user_by( 'login', 'claude-editor' ); if ( $u ) wp_set_current_user( $u->ID );
	require_once ABSPATH . 'wp-admin/includes/plugin.php';
	$file = 'translatepress-multilingual/index.php';
	$step = $_GET['step'] ?? 'info';
	if ( $step === 'install' ) {
		if ( ! file_exists( WP_PLUGIN_DIR . '/' . $file ) ) {
			require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php'; require_once ABSPATH . 'wp-admin/includes/plugin-install.php'; require_once ABSPATH . 'wp-admin/includes/file.php';
			$api = plugins_api( 'plugin_information', array( 'slug' => 'translatepress-multilingual', 'fields' => array( 'sections' => false ) ) );
			if ( is_wp_error( $api ) ) { echo 'api: ', $api->get_error_message(); exit; }
			$up = new Plugin_Upgrader( new Automatic_Upgrader_Skin() ); $res = $up->install( $api->download_link );
			echo 'install: '; var_dump( $res ); echo "verze {$api->version}\n";
		}
		$a = activate_plugin( $file ); echo 'activate: ', is_wp_error( $a ) ? $a->get_error_message() : 'ok', "\n";
	}
	if ( $step === 'settings' ) {
		$s = get_option( 'trp_settings', array() );
		$s['default-language'] = 'cs_CZ';
		$s['translation-languages'] = array( 'cs_CZ', 'de_DE' );
		$s['publish-languages'] = array( 'cs_CZ', 'de_DE' );
		$s['url-slugs'] = array( 'cs_CZ' => 'cs', 'de_DE' => 'de' );
		$s['add-subdirectory-to-default-language'] = 'no';
		$s['force-language-to-custom-links'] = 'yes';
		$s['trp-ls-floater'] = 'no';
		update_option( 'trp_settings', $s );
		// TranslatePress 3.x má plovoucí přepínač v samostatném nastavení
		$ls = get_option( 'trp_language_switcher_settings', array() );
		if ( isset( $ls['floater'] ) ) { $ls['floater']['enabled'] = false; update_option( 'trp_language_switcher_settings', $ls ); }
		// chybějící tabulky + stažení jazykového balíčku (jako při uložení nastavení v administraci)
		require_once ABSPATH . 'wp-admin/includes/file.php'; require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php'; require_once ABSPATH . 'wp-admin/includes/translation-install.php';
		update_option( 'trp_settings', TRP_Translate_Press::get_trp_instance()->get_component( 'settings' )->sanitize_settings( get_option( 'trp_settings' ) ) );
		if ( class_exists( 'Cache_Enabler' ) ) Cache_Enabler::clear_complete_cache();
		// tabulky slovníku vytvoří TranslatePress sám
		if ( class_exists( 'TRP_Translate_Press' ) ) { $trp = TRP_Translate_Press::get_trp_instance(); $q = $trp->get_component( 'query' );
			if ( method_exists( $q, 'check_table' ) ) { $q->check_table( 'cs_CZ', 'de_DE' ); echo "check_table ok\n"; }
			if ( method_exists( $q, 'check_gettext_table' ) ) $q->check_gettext_table( 'de_DE' ); }
		flush_rewrite_rules();
		print_r( $s );
	}
	if ( $step === 'info' ) {
		global $wpdb; echo 'active: ', is_plugin_active( $file ) ? 'yes' : 'no', "\n"; print_r( get_option( 'trp_settings' ) );
		print_r( $wpdb->get_col( "SHOW TABLES LIKE '{$wpdb->prefix}trp%'" ) );
	}
	exit;
} );
