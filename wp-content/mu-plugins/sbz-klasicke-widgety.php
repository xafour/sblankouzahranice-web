<?php
/**
 * Plugin Name: sbz – klasická obrazovka widgetů
 * Description: Vzhled → Widgety a Přizpůsobit používají klasický editor widgetů místo blokového. Blokový editor ukládá přes
 *              /wp-json/batch/v1 a tu adresu blokuje ochrana hostingu WEDOS (pravidlo wp_cve_2026_63030_batch) – uložení pak
 *              končí hláškou „Odpověď není platná ve formátu JSON“. Klasický editor ukládá přes admin-ajax.php, který projde.
 *              Stávající widgety (obrázky, HTML, bloky) zůstávají, jak jsou. Vrácení: smazat tento soubor.
 * Version: 1.0 (Blanka 17. 10. 2026)
 */

defined( 'ABSPATH' ) || exit;

add_filter( 'use_widgets_block_editor', '__return_false' );
add_filter( 'gutenberg_use_widgets_block_editor', '__return_false' );
