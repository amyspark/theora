project(
  'theora',
  'c', 'cpp',
  version: '1.2.0',
  meson_version: '>= 0.59.0',
  license: 'BSD-3-Clause',
  default_options: ['c_std=c11']
)

conf = configuration_data()

enable_valgrind = get_option('valgrind-testing').allowed()

test_env = []

if enable_valgrind
  valgrind_exe = find_program('valgrind')

  conf.set('HAVE_VALGRIND', valgrind_exe.found())

  if conf.get('HAVE_VALGRIND')
    test_env += ['-q', '--leak-check=yes', '--show-reachable=yes', '--num-callers=100']

    message('Tests will be run under: @0@'.format(env.get('VALGRIND_ENVIRONMENT')))
  else
    message('Valgrind not found')
  endif
else
  message('Valgrind testing not enabled')
endif

compile_args = []

cc = meson.get_compiler('c')

if cc.get_argument_syntax() != 'msvc'
  compile_args += cc.get_supported_arguments('-Wall', '-Wno-parentheses')
endif

m_dep = cc.find_library('m', required: false)

if get_option('collect-metrics').enabled()
  add_project_arguments('-DOC_COLLECT_METRICS', language: 'c')
endif

ogg_dep = dependency('ogg',
  version: '>= 1.1',
  required: true,
  not_found_message: '''
    libogg is required to build this package!
    please see http://www.xiph.org/ for how to
    obtain a copy.
  '''
)

vorbis_dep = dependency('vorbis', version: '>= 1.0.1', required: false)

sdl_dep = dependency('sdl', required: false)

if not sdl_dep.found()
  message('*** Unable to find SDL -- Not compiling example players ***')
endif

if cc.has_header('sys/soundcard.h') or cc.has_header('soundcard.h') or cc.has_header('machine/soundcard.h')
  if host_machine.system() == 'openbsd'
    oss_dep = dependency('ossaudio', required: false, disabler: true)
  else
    oss_dep = declare_dependency()
  endif
else
  oss_dep = disabler()
endif

if not oss_dep.found()
  message('OSS audio support not found -- not compiling player_example')
endif

libpng_dep = dependency('libpng', required: false)

tiff_dep = dependency('tiff', required: false, disabler: true)

if tiff_dep.found() and not cc.has_header_symbol(
    'tiffio.h',
    'TIFFReadRGBAImage',
    dependencies: tiff_dep
  )
  tiff_dep = disabler()
endif

asm = get_option('asm').allowed()
enable_asflag_probe = get_option('asflag-probe').allowed()
if asm
  if host_machine.cpu_family() == 'x86_64'
    conf.set('CPU_x86_64', true)
    if cc.get_id() != 'msvc'
      conf.set('OC_X86_ASM', true)
      conf.set('OC_X86_64_ASM', true)
    endif
  elif host_machine.cpu_family() == 'x86'
    conf.set('OC_X86_ASM', true)
  elif host_machine.cpu_family() == 'arm' or host_machine.cpu_family() == 'aarch64'
    conf.set('CPU_arm', true)
    if cc.get_id() == 'gcc'
      conf.set('OC_ARM_ASM', true)
    endif
  endif

  if cc.get_id() == 'gcc' and conf.get('CPU_arm', false)
    # The following checks were only designed for GNU AS.
    # Perl is needed for the arm2gnu reformatter.
    perl_exe = find_program('perl', required: false, disabler: true)

    if not perl_exe.found()
      warning('*** ARM assembly requires perl -- disabling optimizations')
    endif

    if enable_asflag_probe and perl_exe.found()
      assembler_checks = [
        [
          ['HAVE_ARM_ASM_NEON', 'OC_ARM_ASM_NEON'],
          '''.file "configure"
              vorr d0,d0,d0
          ''',
          ['-mfpu=neon', '-march=armv7-a'],
          'assembler supports NEON instructions on ARM'
        ],
        [
          ['HAVE_ARM_ASM_MEDIA', 'OC_ARM_ASM_MEDIA'],
          '''.file "configure"
              shadd8 r3,r3,r3
          ''',
          ['-march=armv6j'],
          'assembler supports ARMv6 media instructions on ARM'],
        [
          ['HAVE_ARM_ASM_EDSP', 'OC_ARM_ASM_EDSP'],
          '''.file "configure"
              qadd r3,r3,r3
          ''',
          ['-march=armv5e'],
          'assembler supports EDSP instructions on ARM'
        ]
      ]

      foreach check : assembler_checks
        pass = cc.compiles(check[1],
          args: ['-x', 'assembler'],
          name: check[3]
        ) or cc.compiles(check[1],
            args: ['-x', 'assembler'] + check[2],
            name: check[3]
          )

        foreach define : check[0]
          conf.set(define, pass)
          conf.set(define, pass)
        endforeach
      endforeach
    endif
  endif
endif

config_h = configure_file(
  configuration: conf,
  output: 'config.h'
)

config_dep = declare_dependency(
  sources: config_h
)

add_project_arguments('-DHAVE_CONFIG_H', language: 'c')

pkg = import('pkgconfig')
windows = import('windows')

subdir('include')

subdir('lib')

if get_option('examples').enabled()
  subdir('examples')
endif

subdir('tests')

theora_dep = declare_dependency(
  link_with : libtheora,
  include_directories : incdir,
)

theoradec_dep = declare_dependency(
  link_with : libtheoradec,
  include_directories : incdir,
)

theoraenc_dep = declare_dependency(
  link_with : libtheoradec,
  include_directories : incdir,
)

if meson.version().version_compare('>=0.54.0')
  meson.override_dependency('theora', theora_dep)
  meson.override_dependency('theoradec', theoradec_dep)
  meson.override_dependency('theoraenc', theoraenc_dep)
endif
