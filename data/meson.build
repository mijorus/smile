desktop_file = configure_file(
        input: 'it.mijorus.smile.desktop.in',
       output: 'it.mijorus.smile.desktop',
      install: true,
         copy: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = configure_file(
        input: 'it.mijorus.smile.appdata.xml.in',
       output: 'it.mijorus.smile.appdata.xml',
      install: true,
         copy: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)


appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('it.mijorus.smile.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

subdir('icons')
subdir('assets')
