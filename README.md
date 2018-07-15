# class_only
[![Build Status](https://travis-ci.com/ForeverWintr/class_only.svg?branch=master)](https://travis-ci.com/ForeverWintr/class_only) [![codecov](https://codecov.io/gh/ForeverWintr/class_only/branch/master/graph/badge.svg)](https://codecov.io/gh/ForeverWintr/class_only)

## Tools for class only design. 

The `class_only` decorator enforces class only design:

```python

from class_only import class_only

@class_only
class VeryFunctional:
    attribute = 5
    
    @classmethod
    def method(cls):
        return a_big_computation(cls.attribute)
```
    
It makes the class uninstantiable:

```python
instance = VeryFunctional()

Traceback (most recent call last):
    ...
TypeError: Class Only classes cannot be instantiated
```

And also immutable:

```python
VeryFunctional.attribute = 6

Traceback (most recent call last):
    ...
TypeError: Class Only classes are immutable
```

It'll also prevent you from adding methods that are used to instantiate classes:

```python

@class_only
class AwesomeClass:

    def __init__(self):
        "Create an awesome instance!"
        
Traceback (most recent call last):
    ...
TypeError: ('Class Only classes cannot define __init__', <class '__main__.AwesomeClass'>)
```

