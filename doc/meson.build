static_docs = files(
  'vp3-format.txt',
  'color.html',
  'draft-ietf-avt-rtp-theora-00.xml',
  'draft-ietf-avt-rtp-theora-00.txt',
)

install_data(static_docs)

if doc.allowed()
  doxygen_conf = configuration_data()

  doxygen_conf.set('PACKAGE', meson.project_name())
  doxygen_conf.set('VERSION', meson.project_version())
  doxygen_conf.set('top_srcdir', meson.project_source_root())

  doxyfile_tmp = configure_file(
    input: 'Doxyfile.in',
    configuration: doxygen_conf,
    output: 'Doxyfile.in',
    install: false,
  )

  doxyfile_patcher = find_program('doxyfile-patcher.py')

  doxyfile = custom_target('doxyfile-patcher',
    command: [doxyfile_patcher, '@INPUT@', '@OUTPUT@', meson.current_build_dir()],
    input: doxyfile_tmp,
    output: 'Doxyfile',
  )

  custom_target('libtheora-docs',
    input: doxyfile,
    output: 'html',
    command: [doxygen_exe, doxyfile],
    console: true,
    install: true,
    install_dir: get_option('datadir') / 'doc' / meson.project_name()
  )
endif
