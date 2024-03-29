#!/usr/bin/python

import os
from sys import stdout as _stdout
from glob import glob
from fnmatch import fnmatch, filter as fnfilter
from subprocess import Popen, PIPE as _PIPE
import re
# note: this module will be deprecated since py2.7
from optparse import OptionParser


def create_walker(root_dir = ".", depth = 0, inc_pattern = ["*.o", "*.pico"], check_hidden = False):
	root_dir_depth = root_dir.count(os.path.sep)
	for root, dirs, files in os.walk(root_dir):
#		print "path:", root_dir, ", root:", root, ", dirs:", dirs, root.count(os.path.sep) - root_dir_depth, depth
		if depth and depth <= (root.count(os.path.sep) - root_dir_depth): continue
		if not files: continue
		if not check_hidden and fnmatch(root[len(root_dir):], "/.[!.]*"): continue

		n = []
		for pat in inc_pattern:
			n.extend(fnfilter(files, pat))
		if not n: continue

#		print "\x1b[1;33m", root, "\x1b[0m", len(n), "items"
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
NAME = 0
HAVE = 1
NEED = 2
LINK = 3
BREF = 4	# back reference
_pat = re.compile(r"\s+([BCDRTU])\s([^@\.]+)")

def create_symbol_table(filename):
	"""\
create symbol table from the input file

table: list
  name: string
  have: list of string
  need: list of list: [ref tag, link target]
  link: a set of string: linked target name
"""
	proc = Popen(["nm", filename], shell=False, stdout=_PIPE)
	output = proc.communicate()
	if not output[0]:
		return None
	#print repr(output[0])
	tbl = [ filename, [], [], set([]), set([]) ]
	syms = output[0].strip().split("\n")
	for line in syms:
		g = _pat.search(line)
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

def find_symbol(pkgs, pkgname, tagname):
	"""\
return the owner of a tag name (might be a public function
or an exported variable) from a list of obj symbol tables.
"""
	# search the same package first
	for obj in pkgs[pkgname]:
		if not obj[HAVE]: continue
		if tagname in obj[HAVE]:
			#print "        found", tagname, "in", obj[NAME]
			return obj
	# search other packages
	for pkg in pkgs:
		for obj in pkgs[pkg]:
			if not obj[HAVE]: continue
			if tagname in obj[HAVE]:
				#print "        found", tagname, "in", obj[NAME]
				return obj
	return None

def analyze_symbol(pkgs):
	for pkg in pkgs:
		for obj in pkgs[pkg]:
			if not obj[NEED]: continue
#			print "analyzing", obj[NAME]
			links = obj[LINK]
			for ref_pair in obj[NEED]:
				#print "    resolving", ref_pair[0]
				link_obj = find_symbol(pkgs, pkg, ref_pair[0])

				if link_obj and link_obj[NAME]:
					ref_pair[1] = link_obj[NAME]
					links.add(ref_pair[1])
					link_obj[BREF].add(obj[NAME])
#					print "    ", obj[NAME], "ref to", ref_pair[1]
#				else:
#					print "missing", ref_pair[0]
					pass
	pass

def dump_dot(pkgs, fout):
	def _name(s):
		return s.replace('.', '_').replace('/', '_').replace('-', '_')

	header = """digraph g
{
	/*bgcolor="transparent";*/
	node [color = lightgray, style = filled];

"""
	fout.write(header)
	# write node
	for pkg in pkgs:
		fout.write("\tsubgraph cluster_%s {\n\t\tlabel = \"%s\";\n\n" % (_name(pkg), pkg))
		for obj in pkgs[pkg]:
			color_prop = ''
			if not obj[LINK]:
				color_prop = ', color = "cyan"'
			elif not obj[BREF]:
				color_prop = ', color = "hotpink"'
#				fout.write("\t\t%s [label=\"%s (%d/%d)\", color = \"lightgreen\"];\n" % (_name(obj[NAME]), obj[NAME], len(obj[BREF]), len(obj[LINK])))

			fout.write("\t\t%s [label=\"%s (%d/%d)\"%s];\n" % (_name(obj[NAME]), obj[NAME], len(obj[BREF]), len(obj[LINK]), color_prop))
		fout.write("\t}\n\n")
	# write link
	for pkg in pkgs:
		for obj in pkgs[pkg]:
			if not obj[NEED]: continue

			links = obj[LINK]
			for ref in links:
				fout.write("\t%s -> %s [label=\"%s\"];\n" % (_name(obj[NAME]), _name(ref), reduce(lambda cnt, need: (need[1] == ref) and cnt + 1 or cnt , obj[NEED], 0)))

	fout.write("}\n")
	pass

def dump_tbl(pkgs, fout):
	def _name(s):
		return s.replace('.', '_').replace('/', '_').replace('-', '_')

	# write node
	for pkg in pkgs:
		fout.write("**************************************\n")
		fout.write("** package: %s\n" % (pkg,))
		for obj in pkgs[pkg]:
			fout.write("======================================\n")
			fout.write("** file: %s (%s)\n" % (obj[NAME], _name(obj[NAME])))
			if obj[HAVE]:
				fout.write("++++++++ have: %s\n" % (repr(obj[HAVE]),) )
			else:
				fout.write("++++++++ have: all private\n")

			if obj[NEED] and obj[LINK]:
				fout.write("++++++++ need: %d, %s\n" % (len(obj[NEED]), repr(obj[NEED])) )
				fout.write("++++++++ link: %d, %s\n" % (len(obj[LINK]), repr(obj[LINK])) )
			else:
				fout.write("++++++++ need: standalone\n")
				fout.write("++++++++ link: standalone\n")

			if obj[BREF]:
				fout.write("++++++++ bref: %d, %s\n" % (len(obj[BREF]), repr(obj[BREF])) )
			else:
				fout.write("++++++++ bref: standalone\n")

			fout.write("\n")
	pass

def dump_trace(pkgs, fout, filename):
#	from sys import setrecursionlimit
#	setrecursionlimit(10000)

	def _n(s):
		return s.split('.')[0] + '.c'

	def find_table(pkgs, name, cache):
		if name in cache:
	#		print "** cache hit:", name
			return cache[name]
	#	print "** search:", name
		for pkg in pkgs:
	#		print "** package:, pkg
			for obj in pkgs[pkg]:
				if obj[NAME].split(os.path.sep)[-1] == name or obj[NAME].find(name) >= 0:
	#			if obj[NAME].find(name) >= 0:
					cache[name] = obj
					return obj
		return None

	def trace(pkgs, name, cache, level = 0):
		leading = ''
		if level:
			leading = ' ' * (level * 2)
		print leading, 'tracing target:', _n(name)

		obj = find_table(pkgs, name, cache)
		if not obj:
			print leading, 'failed:', name, 'not found'
			return
		if not obj[LINK]:
	#		print leading, 'no outgoing links'
			return
		print leading, 'found:', _n(obj[NAME]), ',', len(obj[LINK]), 'outgoing links'
		for link in obj[LINK]:
			link_name = link.split(os.path.sep)[-1]
			print leading, '+-->', _n(link_name)
			# don't trace a file twice
			if link_name in cache or link_name == name: continue
			try:
				trace(pkgs, link_name, cache, level + 1)
			except RuntimeError:
				print leading, 'warn: got except on analyzing', name, '->', link_name, 'level:', level

		pass

	def write_dep(pkgs, fout, name, cache, finished):
		obj = find_table(pkgs, name, cache)
		if not obj: return
		if name in finished: return
	#	if not obj[LINK]:
	#		fout.write("%s: %s\n\n" % (name, _n(name)))
	#		finished.add(name)
	#		return
		for link in obj[LINK]:
			link_name = link.split(os.path.sep)[-1]
			if link_name in finished or link_name == name: continue
			try:
				write_dep(pkgs, fout, link_name, cache, finished)
			except RuntimeError:
				print 'warn: got except on analyzing', name, '->', link_name
		if not name in finished:
			fout.write("%s: %s %s\n\n" % (name, _n(name), ' '.join(map(lambda p: p.split(os.path.sep)[-1], obj[LINK]))))
			finished.add(name)
		pass

	# init cache
	cache = {}

	print 'analyzing target:', _n(filename)
	trace(pkgs, filename, cache)

	print "\ngenerating dep list:\n"
	finished = set([])
	write_dep(pkgs, fout, filename, cache, finished)
	pass

def extract_symbols(path = '.', depth = 0):
	pkglist = {}

	walker = create_walker(path, depth)
	for f in walker:
		p = f.split('/')
		basedir = '/'.join(p[:-1])

		if not basedir in pkglist:
			pkglist[basedir] = []

		tbl = create_symbol_table(f)
		if not tbl: continue

		if 'main' in tbl[HAVE]:
			#print 'found main() in', f
			basedir = '.'.join(f.split('.')[:-1])
			if not basedir in pkglist:
				pkglist[basedir] = []

		pkglist[basedir].append(tbl)

	return pkglist


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-g", "--dot", help = "generate dot file (default)",
		action="store_true", dest = "gendot", default = True)
	parser.add_option("-s", "--silent", help = "don't generate anything",
		action="store_true", dest = "slient", default = False)
	parser.add_option("-x", "--dump", help = "dump raw file",
		action="store_false", dest = "gendot", default = False)
	parser.add_option("-p", "--path", help = "start path (default: .)",
		action="store", dest = "path", default = '.')
	parser.add_option("-o", "--output", help = "output file (default: stdout)",
		action="store", dest="outfile", type = "string", default = '-')
	parser.add_option("-m", "--depth", help = "max depth (default: 0, unlimited)",
		action="store", dest="depth", type = "int", default = 0)
	parser.add_option("-t", "--trace", help = "trace dependency of single file",
		action="store", dest="trace", type = "string", default = '')
	parser.set_defaults(gendot = True)

	options, args = parser.parse_args()

	pkglist = extract_symbols(options.path.rstrip(os.path.sep), options.depth)
	analyze_symbol(pkglist)

	if not options.slient:
		if options.outfile == '-':
			of = _stdout
		else:
			of = file(options.outfile, "w")

		if options.trace:
			dump_trace(pkglist, of, options.trace)
		elif options.gendot:
			dump_dot(pkglist, of)
		else:
			dump_tbl(pkglist, of)

		pass
