<?php
/* Bod 3: velké neprůhledné PNG (fotky a grafiky z Canvy) převést na JPG. Spouští se přes tools/server/run.sh po dávkách:
     krok=seznam            – jen vypíše kandidáty a odhad úspory (nic nemění)
     krok=prevod&od=0&po=25 – převede dávku: originál + všechny zmenšeniny → .jpg (kvalita 85) + .webp, přepíše záznam v knihovně médií
     krok=odkazy            – v obsahu stránek, datech Elementoru a nastaveních nahradí .png → .jpg u převedených obrázků
   Původní PNG soubory zůstávají na disku, takže staré odkazy (Google obrázky, sdílení) dál fungují.
   Převedené obrázky se zapisují do option sbz_png2jpg (id => stará relativní cesta bez přípony). */
add_action( 'wp_loaded', function () {
	if ( ( $_GET['claude'] ?? '' ) !== '__TOKEN__' ) return;
	@set_time_limit( 85 ); header( 'Content-Type: text/plain; charset=utf-8' );
	global $wpdb;
	$krok = $_GET['krok'] ?? 'seznam';
	$up = wp_upload_dir(); $base = $up['basedir'];
	$hotovo = (array) get_option( 'sbz_png2jpg', array() );

	$kandidati = function () use ( $base ) {
		$out = array();
		$ids = get_posts( array( 'post_type' => 'attachment', 'post_mime_type' => 'image/png', 'numberposts' => -1, 'fields' => 'ids', 'post_status' => 'inherit', 'orderby' => 'ID', 'order' => 'ASC' ) );
		foreach ( $ids as $id ) {
			$f = get_attached_file( $id );
			if ( ! $f || ! is_readable( $f ) || filesize( $f ) < 150 * 1024 ) continue;
			if ( file_exists( preg_replace( '/\.png$/i', '.jpg', $f ) ) ) continue; // jméno .jpg už existuje – raději vynechat
			$im = @imagecreatefrompng( $f ); if ( ! $im ) continue;
			$w = imagesx( $im ); $h = imagesy( $im ); $pruhledny = false;
			for ( $x = 0; $x < $w && ! $pruhledny; $x += max( 1, intdiv( $w, 80 ) ) )
				for ( $y = 0; $y < $h; $y += max( 1, intdiv( $h, 80 ) ) )
					if ( ( imagecolorat( $im, $x, $y ) >> 24 ) & 0x7F ) { $pruhledny = true; break; }
			imagedestroy( $im );
			if ( ! $pruhledny ) $out[] = $id;
		}
		return $out;
	};
	$na_jpg = function ( $png, $jpg ) {
		$im = @imagecreatefrompng( $png ); if ( ! $im ) return false;
		$bg = imagecreatetruecolor( imagesx( $im ), imagesy( $im ) );
		imagefill( $bg, 0, 0, imagecolorallocate( $bg, 255, 255, 255 ) );
		imagecopy( $bg, $im, 0, 0, 0, 0, imagesx( $im ), imagesy( $im ) );
		imageinterlace( $bg, true );
		$ok = imagejpeg( $bg, $jpg, 85 );
		imagedestroy( $im ); imagedestroy( $bg );
		return $ok;
	};

	if ( $krok === 'seznam' ) {
		$ids = $kandidati(); $pred = 0; $po = 0; $n = 0;
		foreach ( $ids as $id ) {
			$f = get_attached_file( $id ); $tmp = tempnam( get_temp_dir(), 'sbz' );
			if ( $na_jpg( $f, $tmp ) ) { $pred += filesize( $f ); $po += filesize( $tmp ); $n++; }
			@unlink( $tmp );
			if ( $n >= 40 ) break; // odhad z prvních 40 (časový limit)
		}
		printf( "kandidátů: %d (již převedeno: %d)\nodhad z %d originálů: %.1f MB → %.1f MB\n", count( $ids ), count( $hotovo ), $n, $pred / 1048576, $po / 1048576 );
		exit;
	}

	if ( $krok === 'prevod' ) {
		$od = (int) ( $_GET['od'] ?? 0 ); $pocet = (int) ( $_GET['po'] ?? 25 );
		$ids = array_slice( array_values( array_diff( $kandidati(), array_keys( $hotovo ) ) ), $od, $pocet );
		foreach ( $ids as $id ) {
			$rel = get_post_meta( $id, '_wp_attached_file', true ); $meta = wp_get_attachment_metadata( $id );
			$dir = dirname( get_attached_file( $id ) ); $soubory = array( basename( $rel ) );
			if ( ! empty( $meta['original_image'] ) ) $soubory[] = $meta['original_image'];
			foreach ( (array) ( $meta['sizes'] ?? array() ) as $s ) $soubory[] = $s['file'];
			// i staré zmenšeniny, které už v metadatech nejsou, ale v obsahu na ně může vést odkaz
			foreach ( (array) glob( $dir . '/' . preg_replace( '/\.png$/i', '', basename( $rel ) ) . '-*x*.png' ) as $g ) if ( preg_match( '/-\d+x\d+\.png$/i', $g ) ) $soubory[] = basename( $g );
			$ok = true;
			foreach ( array_unique( $soubory ) as $s ) {
				if ( ! preg_match( '/\.png$/i', $s ) ) continue;
				$png = "$dir/$s"; $jpg = preg_replace( '/\.png$/i', '.jpg', $png );
				if ( ! is_readable( $png ) ) continue;
				if ( ! $na_jpg( $png, $jpg ) ) { $ok = false; break; }
				if ( function_exists( 'sbz_webp_vytvor' ) ) sbz_webp_vytvor( $jpg );
			}
			if ( ! $ok ) { echo "$id CHYBA $rel\n"; continue; }
			$jpgrel = preg_replace( '/\.png$/i', '.jpg', $rel );
			update_post_meta( $id, '_wp_attached_file', $jpgrel );
			$meta['file'] = preg_replace( '/\.png$/i', '.jpg', $meta['file'] ?? $rel );
			if ( ! empty( $meta['original_image'] ) ) $meta['original_image'] = preg_replace( '/\.png$/i', '.jpg', $meta['original_image'] );
			foreach ( (array) ( $meta['sizes'] ?? array() ) as $k => $s ) { $meta['sizes'][ $k ]['file'] = preg_replace( '/\.png$/i', '.jpg', $s['file'] ); $meta['sizes'][ $k ]['mime-type'] = 'image/jpeg'; unset( $meta['sizes'][ $k ]['filesize'] ); }
			$meta['filesize'] = filesize( "$base/$jpgrel" );
			wp_update_attachment_metadata( $id, $meta );
			$wpdb->update( $wpdb->posts, array( 'post_mime_type' => 'image/jpeg', 'guid' => preg_replace( '/\.png$/i', '.jpg', get_post_field( 'guid', $id ) ) ), array( 'ID' => $id ) );
			clean_post_cache( $id );
			$hotovo[ $id ] = preg_replace( '/\.png$/i', '', $rel );
			printf( "%d %s %d kB → %d kB\n", $id, $rel, filesize( "$base/$rel" ) / 1024, filesize( "$base/$jpgrel" ) / 1024 );
		}
		update_option( 'sbz_png2jpg', $hotovo, false );
		echo 'zbývá: ', max( 0, count( array_diff( $kandidati(), array_keys( $hotovo ) ) ) ), "\n";
		exit;
	}

	if ( $krok === 'odkazy' ) {
		// stejná délka řetězce (.png → .jpg), takže serializovaná data zůstanou platná
		$vzory = array();
		foreach ( $hotovo as $id => $stem ) {
			$q = preg_quote( $stem, '#' );
			$vzory[] = '#(' . $q . '(?:-\d+x\d+)?(?:-scaled)?)\.png#i';
			$vzory[] = '#(' . str_replace( '/', '\\\\\\/', $q ) . '(?:-\d+x\d+)?(?:-scaled)?)\.png#i'; // JSON: 2024\/04\/x.png
		}
		$nahrad = fn( $s ) => preg_replace( $vzory, '$1.jpg', $s );
		$zmeny = 0;
		foreach ( $wpdb->get_results( "SELECT ID, post_content FROM {$wpdb->posts} WHERE post_type NOT IN ('revision','attachment') AND post_content LIKE '%.png%'" ) as $p ) {
			$n = $nahrad( $p->post_content ); if ( $n !== $p->post_content ) { $wpdb->update( $wpdb->posts, array( 'post_content' => $n ), array( 'ID' => $p->ID ) ); clean_post_cache( $p->ID ); $zmeny++; }
		}
		foreach ( $wpdb->get_results( "SELECT m.meta_id, m.meta_value FROM {$wpdb->postmeta} m JOIN {$wpdb->posts} p ON p.ID=m.post_id WHERE p.post_type NOT IN ('revision','attachment') AND m.meta_key NOT IN ('_wp_attached_file','_wp_attachment_metadata','_elementor_element_cache') AND m.meta_value LIKE '%.png%'" ) as $m ) {
			$n = $nahrad( $m->meta_value ); if ( $n !== $m->meta_value ) { $wpdb->update( $wpdb->postmeta, array( 'meta_value' => $n ), array( 'meta_id' => $m->meta_id ) ); $zmeny++; }
		}
		foreach ( $wpdb->get_results( "SELECT option_id, option_value FROM {$wpdb->options} WHERE option_value LIKE '%.png%' AND option_name NOT LIKE '%transient%' AND option_name NOT LIKE 'claude_backup%'" ) as $o ) {
			$n = $nahrad( $o->option_value ); if ( $n !== $o->option_value ) { $wpdb->update( $wpdb->options, array( 'option_value' => $n ), array( 'option_id' => $o->option_id ) ); $zmeny++; }
		}
		$wpdb->query( "DELETE FROM {$wpdb->postmeta} WHERE meta_key='_elementor_element_cache'" );
		wp_cache_flush();
		\Elementor\Plugin::$instance->files_manager->clear_cache();
		if ( class_exists( 'Cache_Enabler' ) ) Cache_Enabler::clear_complete_cache();
		echo "upraveno záznamů: $zmeny\n"; exit;
	}
} );
