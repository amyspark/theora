project(
  'theora',
  'c', 'cpp',
  version: '1.2.0',
  meson_version: '>= 0.59.0',
  license: 'BSD-3-Clause',
  default_options: ['c_std=c11']
)

conf = configuration_data()

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

asm = get_option('asm').allowed()
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
