import sys


dev_mode = False

debug_mode = True and dev_mode
auto_upload = True and dev_mode
auto_submit = True and dev_mode

bundled_mode = False or getattr(sys, 'frozen', False)

test_files_directory = ''
compare_set_test_files = [
]
golden_set_test_files = [
]
metadata_test_files = [
]
regions_test_files = [
]
