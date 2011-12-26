#!/usr/bin/python

import os
from sys import stdout
from glob import glob
from fnmatch import fnmatch, filter as fnfilter
from subprocess import Popen, PIPE
import re


def create_walker(root_dir = ".", inc_pattern = ["*.o", "*.pico"], check_hidden = False):
	for root, dirs, files in os.walk(root_dir):
		if not files: continue
		if not check_hidden and fnmatch(root[len(root_dir):], "/.[!.]*"): continue

		n = []
		for pat in inc_pattern:
			n.extend(fnfilter(files, pat))
		if not n: continue

#		print "\x1b[1;33m", root, "\x1b[0m", len(n)
		for file in n:
#			print "\t\t", os.path.join(root, file)
			yield os.path.join(root, file)
	pass



def check_stdlib(func):
	return func in [
			"connect", "execl", "perror", "getenv", "usleep", "memcpy", "signal",
			"mkdir", "getpwuid", "snprintf", "strcmp", "strlen", "strncpy", "rewind",
			"fseek", "vsprintf", "feof", "fprintf", "exit", "strchr", "strstr", "sscanf",
			"stderr", "malloc", "memset", "strerror", "putenv", "sigaction", "system",
			"socket", "abort", "fread", "close", "free", "strcpy", "stat", "getuid",
			"strdup", "read", "time", "write", "waitpid", "fork", "memcmp", "memmove",
			"sprintf", "strncmp", "strcat", "fopen", "fclose", "puts", "realloc",
			"bcopy", "fgets", "fwrite", "printf", "fileno", "fstat", "chdir", "fflush",
			"ftell", "opendir", "readdir", "atoi", "qsort", "scanf", "fputc", "fputs",
			"closedir", "setenv", "bsearch", "accept", "bind", "htonl", "htons", "listen",
			"rand", "srand", "unlink", "stdout", "log", "pow", "toupper", "tolower",
			"gettext", "textdomain", "getegid", "geteuid", "getifaddrs", "getpeername",
			"getpid", "gettimeofday", "inet_ntoa", "kill", "localtime",
			"pipe", "regcomp", "regexec", "regfree", "setpgrp", "vfprintf", "vsnprintf",
			"access", "bind_textdomain_codeset", "daemon", "dlopen", "dlsym", "dup2",
			"execlp", "freeifaddrs", "fscanf",
			"g_markup_escape_text", "g_object_class_install_property",
			"g_object_notify", "g_object_set", "g_object_set_data", "g_param_spec_enum",
			"g_return_if_fail_warning", "g_signal_handler_block", "g_signal_handler_unblock",
			"g_strdup_printf", "g_strndup", "g_type_check_instance_is_a", "g_type_class_peek",
			"g_type_class_peek_parent", "g_type_from_name", "g_type_name", "g_type_register_static",
			"g_convert", "g_free", "g_object_new", "g_signal_emit_by_name", "g_strdup",
			"g_type_check_class_cast", "g_type_check_instance_cast", "g_object_unref",
			"g_type_module_register_type", "gtk_im_context_get_type", "g_source_remove",
			"g_utf8_offset_to_pointer", "gdk_keyval_to_unicode", "g_signal_connect_data",
			"gdk_display_get_default", "gdk_draw_layout", "gdk_draw_pixbuf",
			"gdk_drawable_get_size", "gdk_error_trap_pop", "gdk_error_trap_push", "gdk_flush",
			"gdk_gc_new", "gdk_gc_set_rgb_fg_color", "gdk_pixbuf_get_height",
			"gdk_pixbuf_get_type", "gdk_pixbuf_get_width", "gdk_pixbuf_new_from_file",
			"gdk_pixbuf_new_from_file_at_size", "gdk_pixbuf_render_pixmap_and_mask",
			"gdk_screen_get_default", "gdk_screen_get_number", "gdk_screen_get_type",
			"gdk_screen_height", "gdk_screen_width", "gdk_window_add_filter",
			"gdk_window_clear_area", "gdk_window_get_origin", "gdk_window_lookup_for_display",
			"gdk_window_remove_filter", "gdk_window_set_back_pixmap",
			"gdk_window_set_override_redirect", "gdk_x11_display_get_xdisplay",
			"gdk_x11_get_server_time",
			"gtk_init", "gdk_init", "g_object_get", "g_snprintf", "g_timeout_add",
			"gdk_color_parse", "g_io_add_watch", "g_io_channel_unix_new",
			"gdk_display", "gdk_drawable_get_screen", "gdk_screen_get_display",
			"gdk_x11_drawable_get_xid", "gtk_container_add",
			"gdk_screen_get_root_window", "gdk_x11_drawable_get_xdisplay",
			"gtk_tree_model_get_iter_first",
			"gtk_tree_model_get_type",
			"gtk_tree_model_iter_next",
			"gtk_tree_path_free",
			"gtk_tree_path_get_indices",
			"gtk_tree_path_new_from_string",
			"gtk_tree_selection_select_iter",
			"gtk_tree_selection_set_mode",
			"gtk_tree_view_get_model",
			"gtk_tree_view_get_selection",
			"gtk_tree_view_get_type",
			"gtk_tree_view_insert_column_with_attributes",
			"gtk_tree_view_new_with_model",
			"gtk_tree_view_set_rules_hint",
			"gtk_vbox_new",
			"gtk_vseparator_new",
			"gtk_widget_add_events",
			"gtk_widget_create_pango_layout",
			"gtk_widget_destroy",
			"gtk_widget_destroyed",
			"gtk_widget_get_display",
			"gtk_widget_get_pango_context",
			"gtk_widget_get_screen",
			"gtk_widget_get_type",
			"gtk_widget_grab_default",
			"gtk_widget_hide",
			"gtk_widget_hide_all",
			"gtk_widget_modify_bg",
			"gtk_widget_modify_fg",
			"gtk_widget_modify_font",
			"gtk_widget_queue_draw",
			"gtk_widget_realize",
			"gtk_widget_set_app_paintable",
			"gtk_widget_set_double_buffered",
			"gtk_widget_set_size_request",
			"gtk_widget_set_tooltip_text",
			"gtk_widget_shape_combine_mask",
			"gtk_widget_show",
			"gtk_widget_show_all",
			"gtk_widget_show_now",
			"gtk_widget_size_request",
			"gtk_widget_translate_coordinates",
			"gtk_window_get_position",
			"gtk_window_get_size",
			"gtk_window_get_type",
			"gtk_window_move",
			"gtk_window_new",
			"gtk_window_present",
			"gtk_window_resize",
			"gtk_window_set_accept_focus",
			"gtk_window_set_default_size",
			"gtk_window_set_focus_on_map",
			"gtk_window_set_icon_from_file",
			"gtk_window_set_keep_above",
			"gtk_window_set_position",
			"gtk_window_set_title",
			"g_array_append_vals",
			"g_array_sized_new",
			"g_locale_from_utf8",
			"g_log",
			"g_value_set_enum",
			"gtk_adjustment_new",
			"gtk_alignment_new",
			"gtk_arrow_new",
			"gtk_box_get_type",
			"gtk_box_pack_end",
			"gtk_box_pack_start",
			"gtk_button_get_type",
			"gtk_button_new",
			"gtk_button_new_from_stock",
			"gtk_button_new_with_label",
			"gtk_button_set_label",
			"gtk_cell_renderer_pixbuf_new",
			"gtk_cell_renderer_text_new",
			"gtk_cell_renderer_toggle_get_type",
			"gtk_cell_renderer_toggle_new",
			"gtk_cell_renderer_toggle_set_radio",
			"gtk_check_button_new",
			"gtk_check_button_new_with_label",
			"gtk_check_menu_item_get_active",
			"gtk_check_menu_item_get_type",
			"gtk_check_menu_item_new_with_label",
			"gtk_check_menu_item_set_active",
			"gtk_clipboard_get",
			"gtk_clipboard_request_text",
			"gtk_clipboard_set_text",
			"gtk_color_selection_dialog_get_type",
			"gtk_color_selection_dialog_new",
			"gtk_color_selection_get_current_color",
			"gtk_color_selection_get_type",
			"gtk_color_selection_palette_to_string",
			"gtk_color_selection_set_current_color",
			"gtk_combo_box_append_text",
			"gtk_combo_box_get_active",
			"gtk_combo_box_get_type",
			"gtk_combo_box_new_text",
			"gtk_combo_box_set_active",
			"gtk_container_get_type",
			"gtk_container_set_border_width",
			"gtk_dialog_get_type",
			"gtk_dialog_run",
			"gtk_drawing_area_new",
			"gtk_entry_get_text",
			"gtk_entry_get_type",
			"gtk_entry_new",
			"gtk_entry_set_text",
			"gtk_event_box_get_type",
			"gtk_event_box_new",
			"gtk_event_box_set_visible_window",
			"gtk_expander_get_expanded",
			"gtk_expander_get_type",
			"gtk_expander_new",
			"gtk_file_chooser_dialog_new",
			"gtk_file_chooser_get_filename",
			"gtk_file_chooser_get_type",
			"gtk_font_button_get_font_name",
			"gtk_font_button_get_type",
			"gtk_font_button_new_with_font",
			"gtk_frame_get_type",
			"gtk_frame_new",
			"gtk_frame_set_shadow_type",
			"gtk_get_current_event_time",
			"gtk_hbox_new",
			"gtk_hseparator_new",
			"gtk_image_menu_item_get_type",
			"gtk_image_menu_item_new_with_label",
			"gtk_image_menu_item_set_image",
			"gtk_image_new_from_file",
			"gtk_image_new_from_stock",
			"gtk_label_get_text",
			"gtk_label_get_type",
			"gtk_label_new",
			"gtk_label_set_attributes",
			"gtk_label_set_justify",
			"gtk_label_set_markup",
			"gtk_label_set_selectable",
			"gtk_label_set_text",
			"gtk_list_store_append",
			"gtk_list_store_get_type",
			"gtk_list_store_new",
			"gtk_list_store_set",
			"gtk_main",
			"gtk_main_iteration_do",
			"gtk_main_quit",
			"gtk_menu_get_type",
			"gtk_menu_item_new_with_label",
			"gtk_menu_new",
			"gtk_menu_popup",
			"gtk_menu_shell_append",
			"gtk_menu_shell_get_type",
			"gtk_message_dialog_new",
			"gtk_object_get_type",
			"gtk_orientation_get_type",
			"gtk_plug_get_id",
			"gtk_plug_get_type",
			"gtk_radio_button_get_group",
			"gtk_radio_button_get_type",
			"gtk_radio_button_new_with_label",
			"gtk_rc_parse_string",
			"gtk_scrolled_window_get_type",
			"gtk_scrolled_window_new",
			"gtk_scrolled_window_set_policy",
			"gtk_scrolled_window_set_shadow_type",
			"gtk_settings_get_default",
			"gtk_spin_button_get_type",
			"gtk_spin_button_get_value",
			"gtk_spin_button_new",
			"gtk_status_icon_get_geometry",
			"gtk_status_icon_new_from_file",
			"gtk_status_icon_set_from_file",
			"gtk_table_attach_defaults",
			"gtk_table_get_type",
			"gtk_table_new",
			"gtk_text_buffer_apply_tag_by_name",
			"gtk_text_buffer_create_tag",
			"gtk_text_buffer_get_bounds",
			"gtk_text_buffer_get_char_count",
			"gtk_text_buffer_get_iter_at_offset",
			"gtk_text_buffer_get_selection_bound",
			"gtk_text_buffer_get_selection_bounds",
			"gtk_text_buffer_get_text",
			"gtk_text_buffer_set_text",
			"gtk_text_mark_set_visible",
			"gtk_text_view_get_buffer",
			"gtk_text_view_get_type",
			"gtk_text_view_new",
			"gtk_toggle_button_get_active",
			"gtk_toggle_button_get_type",
			"gtk_toggle_button_set_active",
			"gtk_tree_model_get",
			"gtk_tree_model_get_iter",
			"XGetSelectionOwner", "XGetWindowProperty", "XFree", "XFlush",
			"pango_attr_background_new", "pango_attr_foreground_new", "pango_attr_list_change",
			"pango_attr_list_new", "pango_attr_underline_new",
			"pango_attr_list_insert", "pango_attr_list_unref",
			"pango_context_get_font_description", "pango_font_description_free",
			"pango_font_description_from_string", "pango_font_description_merge",
			"pango_font_description_set_size", "pango_layout_get_font_description",
			"pango_layout_get_pixel_size", "pango_layout_set_font_description",
			"pango_layout_set_text",
			"XChangeProperty", "XCreateSimpleWindow", "XDestroyWindow", "XFilterEvent",
			"XGetWindowAttributes", "XGrabServer", "XIfEvent", "XInternAtom", "XKeysymToKeycode",
			"XLookupString", "XQueryPointer", "XSelectInput", "XSendEvent", "XSetErrorHandler",
			"XSetSelectionOwner", "XSync", "XTestFakeKeyEvent", "XTranslateCoordinates",
			"XUngrabServer", "XkbGetState", "XrmStringToQuark", "Xutf8TextListToTextProperty",
			"_GLOBAL_OFFSET_TABLE_"]

#
#  B   bss
#  T   text
#  D   data
#  R   read only
#
#  U   undefined
#
# table
#   name: string
#   have: list of string
#   need: list of dict: reference -> link target
#
NAME = 0
HAVE = 1
NEED = 2
pat = re.compile(r"\s+([BCDRTU])\s([^@\.]+)")
def create_symbol_table(filename):
	proc = Popen(["nm", filename], shell=False, stdout=PIPE)
	output = proc.communicate()
	if not output[0]:
		return None
	#print repr(output[0])
	tbl = [ filename, [], [] ]
	syms = output[0].strip().split("\n")
	for line in syms:
		g = pat.search(line)
		if not g: continue
		t, ref = g.groups()
		if t == 'U':
			if not check_stdlib(ref):
				tbl[NEED].append( [ref, None] )
			#else:
			#	print filename, "ignore:", ref
		else:
			tbl[HAVE].append(ref)
	return tbl

def resolve_symbol(tbl, name):
	for obj in tbl:
		if not obj[HAVE]: continue
		if name in obj[HAVE]:
			#print "        found", name, "in", obj[NAME]
			return obj[NAME]
	return None

def analyze_symbol(tbl):
	for obj in tbl:
		if not obj[NEED]: continue
#		print "analyzing", obj[NAME]
		for sym_pair in obj[NEED]:
			#print "    resolving", sym_pair[0]
			sym_pair[1] = resolve_symbol(tbl, sym_pair[0])
#			if not sym_pair[1]:
#				print "missing", sym_pair[0]
	pass

def dump_dot(tbl, fout):
	def _name(s):
		return s.replace('.', '_').replace('/', '_').replace('-', '_')

	header = """digraph g
{
	/*bgcolor="transparent";*/

"""
	fout.write(header)
	# write node
	for obj in tbl:
		fout.write("%s [label=\"%s\"];\n" % (_name(obj[NAME]), obj[NAME]))
	# write link
	for obj in tbl:
		if not obj[NEED]: continue

		refs = set([])
		for ref_pair in obj[NEED]:
			if ref_pair[1]:
				refs.add(ref_pair[1])
				#print "    ", obj[NAME], "add", ref_pair[1]
		for ref in refs:
			fout.write("%s -> %s;\n" % (_name(obj[NAME]), _name(ref)))
	fout.write("}\n")
	pass

if __name__ == '__main__':
	obj_table_list = []

	walker = create_walker(".")
	for f in walker:
		tbl = create_symbol_table(f)
		if not tbl: continue

		obj_table_list.append(tbl)

	analyze_symbol(obj_table_list)

	#print "obj_table_list: ", len(obj_table_list)

	#print obj_table_list
	dump_dot(obj_table_list, stdout)

	#f = "./src/im-client/hime-crypt-fpic.o"
	#f = "./src/hime1.so"
	#f = "./build.sh"
	#print create_symbol_table(f)



