"""
Based on http://stackoverflow.com/questions/7323664/python-generator-pre-fetch

This is a single-function package that makes it possible to transform any generator into a `BackgroundGenerator` which computes any number of elements from the generator ahead, in a background thread.

It is quite lightweight, but not entirely weightless.

The `BackgroundGenerator` is most useful when you have a GIL releasing task which might take a long time to complete (e.g. Disk I/O, Web Requests, pure C functions, GPU processing, ...), and another task which takes a similar amount of time, but is dependent on the results of the first task (e.g. Computationally intensive processing of data loaded from disk).

Normally these two tasks will constantly wait for one another to finish. If you make one of these tasks a `BackgroundGenerator` (see examples below), they will work in parallel, potentially saving up to 50% of execution time (definitely less in practice).

We personally use the `BackgroundGenerator` when iterating over minibatches of data for deep learning with tensorflow and theano ( lasagne, blocks, raw, etc.).

Quick usage example (ipython notebook) - https://github.com/justheuristic/prefetch_generator/blob/master/example.ipynb

This package contains two objects:
 - The Class     `BackgroundGenerator(generator [,max_prefetch=1])`
 - The decorator `@prefetch([max_prefetch=1])`

the usage is either

#for item in BackgroundGenerator(my_generator):
#    do_stuff(item)

or

#@prefetch()
#def my_generator(some_param):
#    while True:
#        X = read_heavy_file()
#        y = wget_from_cornhub()
#        do_pretty_much_anything(some_param)
#        yield X, y


More details are written in the `BackgroundGenerator` doc:
See `help(BackgroundGenerator)`
"""

__all__ = ['BackgroundGenerator', 'prefetch', 'background']

from sys import version_info as _py_version_info
if _py_version_info >= (3, 0):
    from queue import Queue
else:
    from Queue import Queue
from threading import Thread
from functools import update_wrapper


class BackgroundGenerator(Thread):
    """
    This Class computes the elements of a generator in a Background Thread.
    
    Since we're talking about Threading here, the usual safety and performance rules apply.
    See https://docs.python.org/3/glossary.html#term-global-interpreter-lock for more information.
    
    "One thread runs Python, while N others sleep or await I/O." (https://opensource.com/article/17/4/grok-gil)
    
    The ideal use case is when either the generator or the main thread do GIL releasing work (e.g. File I/O, Web requests, ...), and the generator has no side effects on the rest of the program (e.g. no modifying of global variables).
    """
    def __init__(self, generator, max_prefetch=1, preprocess_func=None):
        """
        Parameters
        ----------
        generator : generator or genexp or any
            The generator to compute elements from in a background thread.
        
        max_prefetch : int, optional, default: 1
            How many elements of the generator will be precomputed ahead at most.
            If `max_prefetch` is <= 0, then the queue size is infinite.
            When `max_prefetch` elements have been computed ahead, the background thread will simply wait for elements to be consumed by another thread.
        
        preprocess_func: callable, optional, deprecated
            Function to call on the output of the generator before returning the element from the background thread.
            Using this is not recommended, because using
            `BackgroundGenerator(my_generator, 1, my_preprocessor)` is exactly the same as using
            `BackgroundGenerator((my_preprocessor(item) for item in my_generator), 1)`,
            or simply calling `my_preprocessor` before returning from `my_generator`, making this argument redundant.
        
        See Also
        --------
        prefetch : Decorator for wrapping a function which returns a generator with `BackgroundGenerator`.
        background : alias for `prefetch`.
        """
        if preprocess_func is not None: # Deprecated.
            self.run = self._run_with_preprocessor
        super(BackgroundGenerator, self).__init__() # Python 2/3 compatibility
        self.queue           = Queue(max_prefetch)
        self.generator       = generator
        self.preprocess_func = preprocess_func
        self.Continue  = True
        self.daemon    = True
        self.start()
    
    def run(self):
        try:
            for item in self.generator: self.queue.put((True , item))
        except Exception as e:          self.queue.put((False, e))
        finally:                        self.queue.put((False, StopIteration))
    
    def _run_with_preprocessor(self):
        "When a `preprocess_func` is passed to `__init__` this function replaces `run`. Deprecated."
        func = self.preprocess_func
        try:
            for item in self.generator: self.queue.put((True , func(item)))
        except Exception as e:          self.queue.put((False, e))
        finally:                        self.queue.put((False, StopIteration))

    def next(self):
        if self.Continue:
            success, next_item = self.queue.get()
            if success: return next_item
            else:
                self.Continue = False
                raise next_item
        else: raise StopIteration
    __next__ = next # Python 2/3 compatibility. Watch out, order matters!
    
    def __iter__(self): return self

# Decorator
def prefetch(max_prefetch=1):
    """
    Decorator for wrapping a function which returns a generator with `BackgroundGenerator`.
    A new instance of `BackgroundGenerator` is created every time the decorated function is called.
    
    Parameters
    ----------
    max_prefetch : int, optional, default: 1
            How many elements of the generator will be precomputed ahead at most.
            If `max_prefetch` is <= 0, then the queue size is infinite.
            When `max_prefetch` elements have been computed ahead, the background thread will simply wait for elements to be consumed by another thread.
    
    See Also
    --------
    BackgroundGenerator : Class which computes the elements of a generator in a Background Thread.
    prefetch : alias for `background`.
    background : alias for `prefetch`.
    """
    def decorator(generator):
        def wrapper(*args,**kwargs):
            return BackgroundGenerator(generator(*args,**kwargs), max_prefetch=max_prefetch)
        update_wrapper(wrapper, generator)
        return wrapper
    return decorator
background = prefetch # rename without breaking backwards compatibility
