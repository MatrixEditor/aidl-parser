# Copyright (c) 2013 Christopher Thunes
# Modified 2023 by MatrixEditor

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import pickle
import six


class MetaNode(type):
    """
    A metaclass for creating nodes with attribute inheritance.

    This metaclass allows child classes to inherit attributes from their base classes.
    It collects all the ``'attrs'`` attributes defined in the base classes and merges
    them with the ``'attrs'`` attribute defined in the child class.

    Example usage:

    .. code-block:: python

        class Declaration(Node):
            attrs = ("modifiers", "annotations")

    In this example, the ``Declaration`` class inherits attributes from the ``Node`` class,
    including "modifiers" and "annotations".
    """

    def __new__(mcs, name, bases, dict):
        """
        Create a new class using the metaclass.

        This method is called when a new class is defined, and it is responsible for
        modifying the class dictionary to inherit attributes from the base classes.

        :param name: Name of the class being created.
        :param bases: Tuple of base classes.
        :param dict: Dictionary of attributes and methods of the new class.
        :return: Newly created class object.
        """

        attrs = list(dict["attrs"])
        dict["attrs"] = list()

        # Collect attributes from base classes
        for base in bases:
            if hasattr(base, "attrs"):
                dict["attrs"].extend(base.attrs)

        # Merge attributes from the child class
        dict["attrs"].extend(attrs)

        return type.__new__(mcs, name, bases, dict)


@six.add_metaclass(MetaNode)
class Node(object):
    """Base class for nodes with attribute inheritance.

    This class defines a base node that can be used as a building block for creating
    a tree-like structure of nodes. It provides functionality for attribute inheritance,
    equality comparison, representation, iteration, filtering, and access to children
    and position properties.

    Attributes:
        attrs (tuple): A tuple of attribute names to be inherited by child classes.

    Example usage:

    .. code-block:: python

        class Declaration(Node):
            attrs = ("modifiers", "annotations")

        node = Declaration(modifiers=["public"], annotations=["deprecated"])
        print(node.children)  # Output: [['public'], ['deprecated']]

    """

    attrs = ()

    def __init__(self, **kwargs):
        """
        Initializes a new instance of the Node class.

        This method initializes a new Node instance with optional keyword arguments.
        It processes the provided keyword arguments and assigns them to the corresponding
        attributes defined in the `attrs` attribute.

        :param kwargs: Keyword arguments representing attribute-value pairs.
        :raises ValueError: If any extraneous arguments are provided.
        """

        values = kwargs.copy()

        # Assign attribute values from keyword arguments
        for attr_name in self.attrs:
            value = values.pop(attr_name, None)
            setattr(self, attr_name, value)

        # Check for extraneous arguments
        if values:
            raise ValueError(f"Extraneous arguments: {list(values.keys())}")

    def __equals__(self, other):
        """
        Compares two Node instances for equality.

        This method compares the current Node instance with another instance for equality.
        Two instances are considered equal if they are of the same type and their attribute
        values match.

        :param other: Another Node instance to compare.
        :return: True if the instances are equal, False otherwise.
        """

        if type(other) is not type(self):
            return False

        for attr in self.attrs:
            if getattr(other, attr) != getattr(self, attr):
                return False

        return True

    def __repr__(self) -> str:
        """
        Returns a string representation of the Node instance.

        This method returns a string representation of the Node instance, including its
        class name and attribute-value pairs.

        :return: String representation of the Node instance.
        """

        attr_values = []
        for attr in sorted(self.attrs):
            attr_values.append("%s=%s" % (attr, getattr(self, attr)))
        return "%s(%s)" % (type(self).__name__, ", ".join(attr_values))

    def __iter__(self):
        """
        Provides an iterator over the Node instance and its descendants.

        This method returns an iterator that traverses the Node instance and its descendants
        in a depth-first manner. Each iteration yields a tuple containing a path and the node
        at that path.

        :return: An iterator over the Node instance and its descendants.
        """

        return walk_tree(self)

    def filter(self, pattern: type):
        """
        Filters the Node instance and its descendants based on a pattern.

        This method filters the Node instance and its descendants based on a provided pattern.
        The pattern can be a type or an exact match to the nodes. It yields tuples containing
        the path and the matching nodes.

        :param pattern: A type or exact match to filter the nodes.
        :yield: Tuples containing the path and the matching nodes.
        """

        for path, node in self:
            if (isinstance(pattern, type) and isinstance(node, pattern)) or (
                node == pattern
            ):
                yield path, node

    @property
    def children(self):
        """
        Returns a list of child nodes.

        This property returns a list of child nodes by retrieving the attribute values
        corresponding to the attribute names defined in the `attrs` attribute.

        :return: A list of child nodes.
        """

        return [getattr(self, attr_name) for attr_name in self.attrs]

    @property
    def position(self):
        """
        Returns the position of the Node instance.

        This property returns the position of the Node instance if it has a '_position'
        attribute defined.

        :return: The position of the Node instance, or None if not available.
        """

        if hasattr(self, "_position"):
            return self._position


def walk_tree(root):
    children = None

    if isinstance(root, Node):
        yield (), root
        children = root.children
    else:
        children = root

    for child in children:
        if isinstance(child, (Node, list, tuple)):
            for path, node in walk_tree(child):
                yield (root,) + path, node


def dump(ast, file):
    pickle.dump(ast, file)


def load(file):
    return pickle.load(file)
