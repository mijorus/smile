project('smile',
    version: '1.7.3',
    meson_version: '>= 0.50.0',
    default_options: [ 'warning_level=2', ],
)

i18n = import('i18n')

subdir('data')
subdir('src')

meson.add_install_script('build-aux/meson/generate_emoji_dict.py', 'smile')
meson.add_install_script('build-aux/meson/postinstall.py', 'smile')
