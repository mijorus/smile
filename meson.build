project('smile',
    version: '1.5.1',
    meson_version: '>= 0.50.0',
    default_options: [ 'warning_level=2', ],
)

i18n = import('i18n')

subdir('data')
subdir('src')

meson.add_install_script('build-aux/meson/emoji_list/generate_emoji_dict.py')
meson.add_install_script('build-aux/meson/postinstall.py')
