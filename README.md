# prefetch_generator

Simple package that makes your generator work in background thread.


[Quick usage example (ipython notebook)](https://github.com/justheuristic/prefetch_generator/blob/master/example.ipynb)


### Install:
 *  ```pip install prefetch_generator```
 *  No dependencies apart from standard libraries
 *  Works with both python2 and python3 (pip3 install)


### Description:

This is a single-function package that transforms arbitrary generator into a background-thead generator that prefetches several batches of data in a parallel background thead.

This is useful if you have a computationally heavy process (CPU or GPU) that iteratively processes minibatches from the generator while the generator consumes some other resource (disk IO / loading from database / more CPU if you have unused cores). 

By default these two processes will constantly wait for one another to finish. If you make generator work in prefetch mode (see examples below), they will work in parallel, potentially saving you your GPU time.

We personally use the prefetch generator when iterating minibatches of data for deep learning with tensorflow and theano ( lasagne, blocks, raw, etc.).

`based on http://stackoverflow.com/questions/7323664/python-generator-pre-fetch`

### Usage:

This package contains two objects
 - BackgroundGenerator(any_other_generator[,max_prefetch = something])
 - @background([max_prefetch=somethind]) decorator

the usage is either

```
for batch in BackgroundGenerator(my_minibatch_iterator):
    doit()
```

or

```
@background()
def iterate_minibatches(some_param):
    while True:
        X = read_heavy_file()
        X = do_helluva_math(X)
        y = wget_from_pornhub()
        do_pretty_much_anything()
        yield X_batch, y_batch
```

More details are written in the BackgroundGenerator doc
help(BackgroundGenerator)
