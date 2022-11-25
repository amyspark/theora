encoder_sources = files(
  'apiwrapper.c',
  'bitpack.c',
  'dequant.c',
  'fragment.c',
  'idct.c',
  'internal.c',
  'state.c',
  'quant.c',
  'analyze.c',
  'fdct.c',
  'encfrag.c',
  'encapiwrapper.c',
  'encinfo.c',
  'info.c', # not in SConstruct or Makefile.am
  'encode.c',
  'enquant.c',
  'huffenc.c',
  'mathops.c',
  'mcenc.c',
  'rate.c',
  'tokenize.c',
)

decoder_sources = files(
  'apiwrapper.c',
  'bitpack.c',
  'decapiwrapper.c',
  'decinfo.c',
  'decode.c',
  'dequant.c',
  'fragment.c',
  'huffdec.c',
  'idct.c',
  'info.c',
  'internal.c',
  'quant.c',
  'state.c',
)

if asm
  if conf.get('CPU_x86_64', false)
    if cc.get_id() != 'msvc'
      encoder_sources += files(
        'x86/mmxencfrag.c',
        'x86/mmxfdct.c',
        'x86/sse2encfrag.c',
        'x86/x86enquant.c',
        'x86/x86enc.c',

        'x86/sse2fdct.c',

        'x86/x86cpu.c',
        'x86/mmxfrag.c',
        'x86/mmxidct.c',
        'x86/mmxstate.c',
        'x86/sse2idct.c',
        'x86/x86state.c',
      )
      decoder_sources += files(
        'x86/x86cpu.c',
        'x86/mmxidct.c',
        'x86/mmxfrag.c',
        'x86/mmxstate.c',
        'x86/sse2idct.c',
        'x86/x86state.c',
      )
    endif
  elif conf.get('CPU_x86_32', false)
    if cc.get_id() != 'msvc'
      decoder_sources += files(
        'x86/x86cpu.c',
        'x86/mmxidct.c',
        'x86/mmxfrag.c',
        'x86/mmxstate.c',
        'x86/sse2idct.c',
        'x86/x86state.c',
      )
      encoder_sources += files(
        'x86/mmxencfrag.c',
        'x86/mmxfdct.c',
        'x86/sse2encfrag.c',
        'x86/x86enquant.c',
        'x86/x86enc.c',

        'x86/x86cpu.c',
        'x86/mmxfrag.c',
        'x86/mmxidct.c',
        'x86/mmxstate.c',
        'x86/sse2idct.c',
        'x86/x86state.c',
      )
    else
      encoder_sources += files(
        'x86_vc/x86cpu.c',
        'x86_vc/mmxencfrag.c',
        'x86_vc/mmxfdct.c',
        'x86_vc/x86enc.c',
        'x86_vc/mmxfrag.c',
        'x86_vc/mmxidct.c',
        'x86_vc/mmxstate.c',
        'x86_vc/x86state.c',
      )
      decoder_sources += files(
        'x86_vc/x86cpu.c',
        'x86_vc/mmxidct.c',
        'x86_vc/mmxfrag.c',
        'x86_vc/mmxstate.c',
        'x86_vc/x86state.c',
      )
    endif
  endif
endif

decoder_res = files()
encoder_res = files()

if host_machine.system() == 'windows'
  if get_option('buildtype') == 'debug'
    decoder_rc = '../win32/xmingw32/libtheoradecd.rc'
    encoder_rc = '../win32/xmingw32/libtheoraencd.rc'
  else
    decoder_rc = '../win32/xmingw32/libtheoradec.rc'
    encoder_rc = '../win32/xmingw32/libtheoraenc.rc'
  endif

  patcher_py = find_program(
    '../win32/xmingw32/generate_windows_rc.py',
    required: true,
    native: true,
  )

  libtheoradec_rc = custom_target(
    'libtheoradec.rc',
    command: [patcher_py, '@INPUT@', '@OUTPUT@', meson.project_version()],
    input: [decoder_rc, '../win32/xmingw32/libtheoradec-all.rc'],
    output: ['libtheoradec.rc']
  )

  decoder_res += windows.compile_resources(libtheoradec_rc)

  libtheoraenc_rc = custom_target(
    'libtheoraenc.rc',
    command: [patcher_py, '@INPUT@', '@OUTPUT@', meson.project_version()],
    input: [encoder_rc, '../win32/xmingw32/libtheoraenc-all.rc'],
    output: ['libtheoraenc.rc']
  )

  encoder_res += windows.compile_resources(libtheoraenc_rc)
endif

if host_machine.system() == 'darwin'
  version_flag = '-Wl,-exported_symbols_list,@0@'
  theoradec_version_arg = meson.current_source_dir() / 'theoradec.exp'
  theoraenc_version_arg = meson.current_source_dir() / 'theoraenc.exp'
  theora_version_arg = meson.current_source_dir() / 'theora.exp'
else
  version_flag = '-Wl,--version-script,@0@'
  theoradec_version_arg = meson.current_source_dir() / 'Version_script-dec'.format()
  theoraenc_version_arg = meson.current_source_dir() / 'Version_script-enc'
  theora_version_arg = meson.current_source_dir() / 'Version_script'
endif

libtheoradec = library(
  'theoradec',
  decoder_sources + decoder_res,
  dependencies: [m_dep, libpng_dep, ogg_dep, config_dep],
  include_directories: incdir,
  vs_module_defs: '../win32/xmingw32/libtheoradec-all.def',
  link_args: cc.get_supported_link_arguments(
    version_flag.format(theoradec_version_arg)
  ),
  install: true,
)

pkg.generate(
  libtheoradec,
  description: 'Theora video codec (decoder)',
  version: meson.project_version()
)

libtheoraenc = library(
  'theoraenc',
  encoder_sources + encoder_res,
  dependencies: [m_dep, ogg_dep, config_dep],
  include_directories: incdir,
  vs_module_defs: '../win32/xmingw32/libtheoraenc-all.def',
  link_args: cc.get_supported_link_arguments(
    version_flag.format(theoraenc_version_arg)
  ),
  install: true,
)

pkg.generate(
  libtheoraenc,
  description: 'Theora video codec (encoder)',
  version: meson.project_version()
)

libtheora = library(
  'theora',
  encoder_sources + decoder_sources,
  dependencies: [m_dep, ogg_dep, config_dep],
  include_directories: incdir,
  link_args: cc.get_supported_link_arguments(
    version_flag.format(theora_version_arg)
  ),
  vs_module_defs: 'theora.def',
  install: true,
)

pkg.generate(
  libtheora,
  description: 'Theora video codec',
  version: meson.project_version()
)
