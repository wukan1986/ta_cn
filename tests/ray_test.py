import numpy as np
import polars as pl
import ray

ray.init()

frames = [pl.DataFrame({'a': np.random.rand(1000),
                        'b': np.random.rand(1000),
                        'c': np.random.rand(1000)}) for i in range(10)]


def process_a_frame(f: pl.DataFrame):
    # return f.a.max() + f.b.min() + f.c.mean()
    return f.select([
        pl.col('a').max(),
        pl.col('b').min(),
        pl.col('c').mean()
    ]).sum(axis=1)[0]


MP_STYLES = [None,  # No parallelism.
             'ray']  # Ray parallelism
MP_STYLE = None


def pxmap(f, xs, mp_style):
    """Parallel map, implemented with different python parallel execution libraries."""
    if mp_style not in MP_STYLES:
        print(f"Unrecognized mp_style {mp_style}")
    elif mp_style == 'ray':
        @ray.remote
        def g(x):
            return f(x)

        return ray.get([g.remote(x) for x in xs])
    return [f(x) for x in xs]


# https://github.com/pola-rs/polars/issues/1109

_ = pxmap(process_a_frame, frames, 'ray')
print(_)
