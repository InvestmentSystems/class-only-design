# class_only_design
[![Build Status](https://travis-ci.com/InvestmentSystems/class_only_design.svg?branch=master)](https://travis-ci.com/InvestmentSystems/class_only_design) [![codecov](https://codecov.io/gh/ForeverWintr/class_only/branch/master/graph/badge.svg)](https://codecov.io/gh/ForeverWintr/class_only)

## Tools for class only design. 

A 'Class Only Design' is an attempt to merge some aspects of Object Oriented and Functional programming. Specifically, it:

* allows you to group like functions and attributes in a common namespace,  
* lets you use inheritance to override certain functions, e.g., to implement the [template pattern](https://en.wikipedia.org/wiki/Template_method_pattern),
* embraces the functional concept of immutability over changing state.

A *class only* class is, in other words, an approach for creating an immutable singleton object.

### Installation

```bash
pip install class_only_design
```
________

The `class_only` decorator enforces class only design:

```python

from class_only_design import ClassOnly

class VeryFunctional(ClassOnly):
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

class AwesomeClass(ClassOnly):

    def __init__(self):
        "Create an awesome instance!"
        
Traceback (most recent call last):
    ...
TypeError: ('Class Only classes cannot define __init__', <class '__main__.AwesomeClass'>)
```
_________

Conceptually, a *class_only* class can have only one state. However, creating that initial state may be expensive, and you may not want to incur that expense at class creation time. For example, consider the following example:

```python
class Methodology(ClassOnly):
    config = read_large_config_file()
    
    @classmethod
    def process(cls):
        for setting in cls.config:
            # do work
```

The time cost of calling `read_large_config_file` is incurred when `Methodology` is created, which for most classes means module load time. To address this issue, class_only provides the `constant` decorator. Decorating a method with `@constant` creates a class property that is called at most once. Using `constant`, the above example becomes:

```python
from class_only_design import constant

class Methodology(ClassOnly):

    @constant
    def config(cls)
        return read_large_config_file()
    
    @classmethod
    def process(cls):
        for setting in cls.config:
            # do work
```

In the second example, `read_large_config_file` isn't called until `Methodology.process` is. Note that `@constant` ensures that the `config` method is only ever executed once, even if `Methodology.process` is called multiple times. 
