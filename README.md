# Android Interface Definition Language (AIDL) Parser

[![python](https://img.shields.io/badge/python-3.8+-blue.svg?logo=python&labelColor=grey)](https://www.python.org/downloads/)
![Codestyle](https://img.shields.io:/static/v1?label=Codestyle&message=black&color=black)
![License](https://img.shields.io:/static/v1?label=License&message=MIT&color=blue)
[![Parent Repository](https://img.shields.io:/static/v1?label=Parent&message=c2nes/javalang&color=lightgrey)](https://github.com/c2nes/javalang)

> [!Warning]
> This repository aims to provide an implementation of an AIDL parser in Python. For information about the original repository, visit [c2nes/javalang](https://github.com/c2nes/javalang).

`aidl-parser` is a small Python library that can be used to lex and parse Android Interface Definition Language (AIDL) files as well as default Java files.

## Installation

First, clone the repository and change the working directory. Next, install the python library to your local site-packages.

```bash
git clone https://github.com/MatrixEditor/aidl-parser.git
cd aidl-parser && pip install .
```


## Getting Started

```python
>>> import aidl
>>> unit = aidl.fromstring("package com.example; parcelable Foo;")
```

The call above will return an instance of `CompilationUnit`. This particular object serves as the root of a tree structure that can be navigated to retrieve various pieces of information regarding the compilation unit.

```python
>>> unit.package.name
'com.example'
>>> unit.types[0]
ParcelableDeclaration
>>> unit.types[0].name
'Foo'
```

The string provided to `aidl.fromstring` must represent a complete unit, indicating that it should represent a valid AIDL or Java source file in its entirety. However, other functions within the `aidl.parse` module enable the parsing of smaller code snippets without the need to supply a complete compilation unit.

## AIDL Types

### `Parcelable`

As a simple parcelable defintion can be just a reference to the Java implementation file, there will be a special attribute named `is_ref`. It will indicate the presence of a Java implementation file. The `cpp_header` stores an optional C++ file reference.

    ParcelableDeclaration(
        is_ref: bool
        name: str
        cpp_header: str
    )

An example AIDL file with a parcelable would look like this:
```aidl
package com.example;

parcelable Foo cpp_header "native/include/Foo.h";
```

### `Binder`

Binder declarations will be treated as `InterfaceDeclaration` objects internally. As the AIDL specification contains new keywords, the following example tries to illustrates their use case:

```aidl
package com.example;

import com.example.Foo; // all types must be imported

// 'oneway' indicates we don't get a result
oneway interface FooListener {
    // all non-primitive types except String, IBinder and AIDL-generated
    // interfaces must be defined with a directional tag: in, out, inout
    void onActionPerformed(in @nullable Foo foo) = 2; // manually defined transaction code
}
```

For more information about how to write AIDL files, use the [Android Developer](https://developer.android.com/guide/components/aidl?hl=en) reference on AIDL.
