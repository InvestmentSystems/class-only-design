# class_only
[![Build Status](https://travis-ci.com/ForeverWintr/class_only.svg?branch=master)](https://travis-ci.com/ForeverWintr/class_only) [![codecov](https://codecov.io/gh/ForeverWintr/class_only/branch/master/graph/badge.svg)](https://codecov.io/gh/ForeverWintr/class_only)

## Tools for class only design. 

A 'Class Only' design is an attempt to merge some aspects of Object Oriented Programming with a Functional programming paradigm. Specifically, it:

* allows you to group like functions and attributes in a common namespace,  
* lets you use inheritance to override certain functions, e.g., to implement the [template pattern](https://en.wikipedia.org/wiki/Template_method_pattern)
* embraces the functional concept of immutability over changing state.

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

