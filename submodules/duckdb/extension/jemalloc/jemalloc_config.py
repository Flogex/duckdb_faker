import os
import platform

# list all include directories
include_directories = [
    os.path.sep.join(x.split('/')) for x in ['extension/jemalloc/include', 'extension/jemalloc/jemalloc/include']
]
# source files
source_files = [
    os.path.sep.join(x.split('/'))
    for x in [
        'extension/jemalloc/jemalloc_extension.cpp',
        'extension/jemalloc/jemalloc/src/jemalloc.c',
        'extension/jemalloc/jemalloc/src/arena.c',
        'extension/jemalloc/jemalloc/src/background_thread.c',
        'extension/jemalloc/jemalloc/src/base.c',
        'extension/jemalloc/jemalloc/src/batcher.c',
        'extension/jemalloc/jemalloc/src/bin.c',
        'extension/jemalloc/jemalloc/src/bin_info.c',
        'extension/jemalloc/jemalloc/src/bitmap.c',
        'extension/jemalloc/jemalloc/src/buf_writer.c',
        'extension/jemalloc/jemalloc/src/cache_bin.c',
        'extension/jemalloc/jemalloc/src/ckh.c',
        'extension/jemalloc/jemalloc/src/counter.c',
        'extension/jemalloc/jemalloc/src/ctl.c',
        'extension/jemalloc/jemalloc/src/decay.c',
        'extension/jemalloc/jemalloc/src/div.c',
        'extension/jemalloc/jemalloc/src/ecache.c',
        'extension/jemalloc/jemalloc/src/edata.c',
        'extension/jemalloc/jemalloc/src/edata_cache.c',
        'extension/jemalloc/jemalloc/src/ehooks.c',
        'extension/jemalloc/jemalloc/src/emap.c',
        'extension/jemalloc/jemalloc/src/eset.c',
        'extension/jemalloc/jemalloc/src/exp_grow.c',
        'extension/jemalloc/jemalloc/src/extent.c',
        'extension/jemalloc/jemalloc/src/extent_dss.c',
        'extension/jemalloc/jemalloc/src/extent_mmap.c',
        'extension/jemalloc/jemalloc/src/fxp.c',
        'extension/jemalloc/jemalloc/src/san.c',
        'extension/jemalloc/jemalloc/src/san_bump.c',
        'extension/jemalloc/jemalloc/src/hook.c',
        'extension/jemalloc/jemalloc/src/hpa.c',
        'extension/jemalloc/jemalloc/src/hpa_hooks.c',
        'extension/jemalloc/jemalloc/src/hpdata.c',
        'extension/jemalloc/jemalloc/src/inspect.c',
        'extension/jemalloc/jemalloc/src/large.c',
        'extension/jemalloc/jemalloc/src/log.c',
        'extension/jemalloc/jemalloc/src/malloc_io.c',
        'extension/jemalloc/jemalloc/src/mutex.c',
        'extension/jemalloc/jemalloc/src/nstime.c',
        'extension/jemalloc/jemalloc/src/pa.c',
        'extension/jemalloc/jemalloc/src/pa_extra.c',
        'extension/jemalloc/jemalloc/src/pai.c',
        'extension/jemalloc/jemalloc/src/pac.c',
        'extension/jemalloc/jemalloc/src/pages.c',
        'extension/jemalloc/jemalloc/src/peak_event.c',
        'extension/jemalloc/jemalloc/src/prof.c',
        'extension/jemalloc/jemalloc/src/prof_data.c',
        'extension/jemalloc/jemalloc/src/prof_log.c',
        'extension/jemalloc/jemalloc/src/prof_recent.c',
        'extension/jemalloc/jemalloc/src/prof_stats.c',
        'extension/jemalloc/jemalloc/src/prof_sys.c',
        'extension/jemalloc/jemalloc/src/psset.c',
        'extension/jemalloc/jemalloc/src/rtree.c',
        'extension/jemalloc/jemalloc/src/safety_check.c',
        'extension/jemalloc/jemalloc/src/sc.c',
        'extension/jemalloc/jemalloc/src/sec.c',
        'extension/jemalloc/jemalloc/src/stats.c',
        'extension/jemalloc/jemalloc/src/sz.c',
        'extension/jemalloc/jemalloc/src/tcache.c',
        'extension/jemalloc/jemalloc/src/test_hooks.c',
        'extension/jemalloc/jemalloc/src/thread_event.c',
        'extension/jemalloc/jemalloc/src/ticker.c',
        'extension/jemalloc/jemalloc/src/tsd.c',
        'extension/jemalloc/jemalloc/src/util.c',
        'extension/jemalloc/jemalloc/src/witness.c',
        'extension/jemalloc/jemalloc/src/zone.c',
    ]
]
