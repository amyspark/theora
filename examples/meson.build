theora_libs = [libtheora]
theoradec_libs = [libtheoradec]
theoraenc_libs = [libtheoraenc, libtheoradec]

compat_dep = dependency('compat', required: host_machine.system() == 'openbsd')

if cc.has_header_symbol('unistd.h', 'getopt_long')
  getopt_dep = disabler()
else
  if cc.get_id() == 'msvc'
    getopt_sources = files(
      '../win32/getopt.c',
      '../win32/getopt1.c',
    ),
    getopt_incdir = include_directories('../win32/')
  else
    getopt_sources = files(
      'getopt.c',
      'getopt1.c',
    )
    getopt_incdir = include_directories('.')
  endif


  getopt_dep = declare_dependency(
    sources: getopt_sources,
    dependencies: config_dep,
    include_directories: getopt_incdir
  )
endif

dump_video_sources = files(
  'dump_video.c',
)

dump_video = executable(
  'dump_video',
  dump_video_sources,
  link_with: theoradec_libs,
  dependencies: [compat_dep, getopt_dep],
)

dump_psnr_sources = files(
  'dump_psnr.c',
)

dump_psnr = executable(
  'dump_psnr',
  dump_psnr_sources,
  link_with: theoradec_libs,
  dependencies: [m_dep, getopt_dep],
)

libtheora_info_sources = files(
  'libtheora_info.c',
)

libtheora_info = executable(
  'libtheora_info',
  libtheora_info_sources,
  link_with: theoradec_libs,
  dependencies: [config_dep],
)

player_example_sources = files(
  'player_example.c',
)

player_example = executable(
  'player_example',
  player_example_sources,
  link_with: theoradec_libs,
  dependencies: [sdl_dep, vorbis_dep, oss_dep, m_dep, getopt_dep, config_dep],
)

encoder_example_sources = files(
  'encoder_example.c',
)

encoder_example = executable(
  'encoder_example',
  encoder_example_sources,
  link_with: theoraenc_libs,
  dependencies: [ogg_dep, vorbis_dep, vorbisenc_dep, m_dep, getopt_dep],
)

if png_dep.found()
  png2theora_sources = files(
    'png2theora.c',
  )

  png2theora = executable(
    'png2theora',
    png2theora_sources,
    link_with: theoraenc_libs,
    dependencies: [ogg_dep, png_dep, m_dep, getopt_dep, config_dep],
  )
endif

tiff2theora_sources = files(
  'tiff2theora.c',
)

tiff2theora = executable(
  'tiff2theora',
  tiff2theora_sources,
  link_with: theoraenc_libs,
  dependencies: [ogg_dep, tiff_dep, m_dep, getopt_dep, config_dep],
)
