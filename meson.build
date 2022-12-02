project(
  'theora',
  'c',
  'cpp',
  version: '1.2.0',
  meson_version: '>= 0.49.0',
  license: 'BSD-3-Clause',
  default_options: ['c_std=c11'],
)

conf = configuration_data()

valgrind_testing = get_option('valgrind-testing')

valgrind_exe = find_program('valgrind', required: valgrind_testing)

if valgrind_exe.found()
  add_test_setup(
    'valgrind',
    exe_wrapper: [
      valgrind_exe,
      '-q',
      '--leak-check=yes',
      '--show-reachable=yes',
      '--num-callers=100',
    ],
  )
endif

compile_args = []

cc = meson.get_compiler('c')

if cc.get_argument_syntax() != 'msvc'
  compile_args += cc.get_supported_arguments(
    '-Wno-parentheses',
    '-Wno-shift-op-parentheses',
    '-Wno-shift-negative-value',
  )
endif

m_dep = cc.find_library('m', required: false)

if get_option('collect-metrics')
  add_project_arguments('-DOC_COLLECT_METRICS', language: 'c')
endif

ogg_dep = dependency('ogg', version: '>= 1.1', required: true)

vorbis_dep = dependency(
  'vorbis',
  version: '>= 1.0.1',
  required: false,
  disabler: true,
)

vorbisenc_dep = dependency(
  'vorbisenc',
  version: '>= 1.0.1',
  required: false,
  disabler: true,
)

sdl_dep = dependency('sdl', required: false, disabler: true)

if not sdl_dep.found()
  message('*** Unable to find SDL -- Not compiling example players ***')
endif

if (
  cc.has_header('sys/soundcard.h')
  or cc.has_header('soundcard.h')
  or cc.has_header('machine/soundcard.h')
)
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

if cc.has_header('unistd.h')
  unistd_dep = declare_dependency()
else
  unistd_dep = disabler()
endif

tiff_dep = dependency('tiff', required: false, disabler: true)

if tiff_dep.found() and not cc.has_header_symbol(
    'tiffio.h',
    'TIFFReadRGBAImage',
    dependencies: tiff_dep
  )
  tiff_dep = disabler()
endif

telemetry = get_option('telemetry')

cairo_dep = dependency('cairo', required: telemetry)

if cairo_dep.found()
  conf.set('HAVE_CAIRO', true)
endif

mem_constraint = get_option('mem-constraint')

if mem_constraint.enabled()
  conf.set('HAVE_MEMORY_CONSTRAINT', language: 'c')
endif

asm = not get_option('asm').disabled()
if asm
  if host_machine.cpu_family() == 'x86_64'
    conf.set('CPU_x86_64', true)
    if cc.get_id() != 'msvc'
      conf.set('OC_X86_ASM', true)
      conf.set('OC_X86_64_ASM', true)
    endif
  elif host_machine.cpu_family() == 'x86'
    conf.set('OC_X86_ASM', true)
  endif
endif

config_h = configure_file(configuration: conf, output: 'config.h')

config_dep = declare_dependency(sources: config_h)

add_project_arguments('-DHAVE_CONFIG_H', language: 'c')

pkg = import('pkgconfig')
windows = import('windows')

subdir('include')

subdir('lib')

examples = get_option('examples')

if examples.auto() or examples.enabled()
  subdir('examples')
endif

subdir('tests')

doc = get_option('doc')

doc_root_dir = meson.current_source_dir()

doxygen_exe = find_program(
  'doxygen',
  required: doc,
  disabler: true,
)

subdir('doc')

spec = get_option('spec')

if spec.auto() or spec.enabled()
  # Note: unlike the original autotools script, here we use
  # latexmk to do the dependency management for us.
  # This implicates that we've got to copy spec.{tex,bib}
  # to the build folder in /doc/spec/ to make all files
  # live in the same folder.
  latexmk_exe = find_program('latexmk', required: spec)
  transfig_exe = find_program('fig2dev', required: spec)
  # used indirectly by latexmk
  pdflatex = find_program('pdflatex', required: spec)
  bibtex = find_program('bibtex', required: spec)

  if (
    latexmk_exe.found()
    and pdflatex.found()
    and bibtex.found()
    and transfig_exe.found()
  )
    check_needed_tex_packages = find_program(
      'doc/spec/check-needed-tex-packages.py',
      required: true,
    )
    test_tex_packages = find_program(
      'doc/spec/test-tex-packages.py',
      required: true,
    )

    message(
      'Checking for packages in @0@...'.format(
        meson.current_source_dir() / 'doc/spec/spec.tex',
      ),
    )

    packages = run_command(
      check_needed_tex_packages,
      capture: true,
      check: true,
    ).stdout().split()

    tex_pkg_ok = true

    foreach pkg : packages
      message('for Tex package @0@'.format(pkg))

      pkg_test = run_command(test_tex_packages, '--pdflatex', pdflatex, pkg)
      if pkg_test.returncode() != 0
        message = 'The \'@0@\' TeX package is missing or broken'.format(pkg)

        if spec.enabled()
          error(message)
        else
          warning(message)
          tex_pkg_ok = false
        endif
        break
      endif
    endforeach
  else
    tex_pkg_ok = false
  endif

  if tex_pkg_ok
    subdir('doc/spec')
  else
    message('*** Format Specification will not be built.')
  endif
endif
