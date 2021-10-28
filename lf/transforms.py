"""The Transform class and some of its children. """
import ast
import re
from copy import copy
from collections import Counter, namedtuple
import contextlib
import inspect
from itertools import chain
from pathlib import Path
import types
from typing import Iterable, List, Literal, Optional, Set, Tuple, Union, Iterator
from warnings import warn

import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from lf.data import SimpleIterator
from lf.dumptools import var2mod, thingfinder, inspector
from lf.exceptions import WrongDeviceError
from lf.print_utils import combine_multi_line_strings, create_reverse_arrow, make_bold, make_green, \
    create_arrow


class _Notset:
    # pylint: disable=too-few-public-methods
    pass


_notset = _Notset()


def _isinstance_of_namedtuple(arg):
    """Check if input *arg* is instance of namedtuple"""
    typ = type(arg)
    base = typ.__bases__
    if len(base) != 1 or base[0] != tuple:
        return False
    fields = getattr(typ, '_fields', None)
    if not isinstance(fields, tuple):
        return False
    return all(isinstance(field, str) for field in fields)


Stage = Literal['infer', 'eval', 'train']
Component = Literal['preprocess', 'forward', 'postprocess']


class Transform:
    """Transform base class.

    :param call_info:
    :param lf_name: name of the transform
    """
    lf_stage = None

    def __init__(self, call_info: Optional[inspector.CallInfo] = None,
                 lf_name: Optional[str] = None):
        if call_info is None:
            call_info = inspector.CallInfo()
        self._lf_call_info = call_info
        self._lf_varname = _notset
        self._lf_name = lf_name
        self._lf_component = {'forward'}
        self._lf_device = 'cpu'
        self._lf_layers = None

    @property
    def lf_name(self) -> Optional[str]:
        """The "name" of the transform.

        A transform can have a name. This is optional, but helps when inspecting complex transforms.
        Good transform names indicate what the transform does.

        If a transform does not have an explicitly set name, the name will default to the name of
        the *last variable the transforms was assigned to*.
        """
        if self._lf_name is None:
            return self.lf_varname()
        return self._lf_name

    def __rshift__(self, other: "Transform") -> "Compose":
        """Compose with *other*.

        Example:
            t = a >> b >> c
        """
        return Compose([self, other])

    @property
    def n_display_inputs(self):
        return len(self.lf_get_signature())

    @property
    def n_display_outputs(self):
        return 1

    @property
    def display_width(self):
        return len(self.lf_shortname())

    @property
    def children_widths(self):
        return [self.display_width]

    def __add__(self, other: "Transform") -> "Rollout":
        """ Rollout with *other*.

        Example:
            t = a + b + c
        """
        return Rollout([self, other])

    def __truediv__(self, other: "Transform") -> "Parallel":
        """ Parallel with *other*.

        Example:
            t = a / b / c
        """
        return Parallel([self, other])

    def __sub__(self, name: str) -> "Transform":
        """Create a named clone of the transform.

        Example:
            named_t = t - 'rescale image'
        """
        named_copy = copy(self)
        named_copy._lf_name = name
        return named_copy

    def lf_pre_save(self, path: Path, i: int):
        """Method that is called on each transform before saving.

        :param path: The save path.
        :param i: Subtransform index.
        """

    def lf_post_load(self, path: Path, i: int):
        """Method that is called on each transform after loading.

        :param path: The load path.
        :param i: Subtransform index.
        """

    def lf_save(self, path: Union[Path, str]):
        """Save the transform to *path*. """
        path = Path(path)
        path.mkdir(exist_ok=True)
        for i, subtrans in enumerate(self.lf_all_transforms()):
            subtrans.lf_pre_save(path, i)
        with open(path / 'transform.py', 'w') as f:
            f.write(self.lf_dumps())

    def _lf_codegraph_startnode(self, name: str) -> var2mod.CodeNode:
        """Build the start-code-node - the node with the source needed to create *self* as "name".
        (in the scope where *self* was originally created). """
        start_source = f'{name or "_lf_dummy"} = {self.lf_evaluable_repr()}'
        start_node = ast.parse(start_source).body[0]
        start_globals = {
            (var, self._lf_call_info.scope)  # this should be the current scope ...?
            for var in var2mod.find_globals(start_node)
        }
        return var2mod.CodeNode(
            source=start_source,
            ast_node=start_node,
            globals_=start_globals
        )

    @property
    def _lf_closurevars(self) -> Tuple[dict, dict]:
        """Return the closurevars (globals and nonlocals) the transform depends on. """
        return {}, {}

    def _lf_build_codegraph(self, graph: Optional[dict] = None,
                            scopemap: Optional[dict] = None,
                            name: Optional[str] = None,
                            scope: Optional[thingfinder.Scope] = None) -> Tuple[dict, dict]:
        if graph is None:
            graph = {}
        if scopemap is None:
            scopemap = {}

        if scope is None:
            scope = self._lf_call_info.scope

        if name is not None:
            name_scope_here = name, scope
        else:
            name_scope_here = None

        given_name = name

        try:
            if self._lf_call == name:
                name = None
        except AttributeError:
            pass

        # build the start node ->
        start = self._lf_codegraph_startnode(name)
        # <-

        globals_dict, nonlocals_dict = self._lf_closurevars
        all_vars_dict = {**globals_dict, **nonlocals_dict}

        # find dependencies
        todo = {*start.globals_}
        while todo and (next_ := todo.pop()):
            # we know this already - go on
            if next_ in scopemap:
                continue

            next_var, next_scope = next_

            # see if the object itself knows how to generate its codegraph
            try:
                if len(next_scope) > 0:
                    next_obj = all_vars_dict[next_var]
                else:
                    next_obj = globals_dict[next_var]
                next_obj._lf_build_codegraph(graph, scopemap, next_var)
            except (KeyError, AttributeError):
                pass
            else:
                print(next_var, 'can deal with itself')
                continue

            # find how next_var came into being
            (source, node), scope_of_next_var = thingfinder.find_in_scope(next_var, next_scope)
            scopemap[next_var, next_scope] = scope_of_next_var

            # find dependencies
            globals_ = {
                (var, scope_of_next_var)  # TODO: this
                for var in var2mod.find_globals(node)
            }
            graph[next_var, scope_of_next_var] = var2mod.CodeNode(source=source, globals_=globals_,
                                                                  ast_node=node)
            todo.update(globals_)
        # find dependencies done

        if name is not None:
            assert scope is not None
            graph[name, scope] = start

        if given_name is not None:
            scopemap[given_name, scope] = scope

        return graph, scopemap

    def lf_evaluable_repr(self, indent: int = 0, var_transforms: Optional[dict] = None) -> str:  # TODO: var_transforms needed?
        # pylint: disable=unused-argument,no-self-use
        """Return a string that if evaluated *in the same scope where the transform was created*
        creates the transform. """
        return NotImplemented

    def lf_all_transforms(self, result=None):
        """Return a list of all transforms needed for executing the transform.

        This includes the transform itself, the subtransforms of a compount transform or
        transforms a function-transform depends on as a global. """
        if result is None:
            result = []
        if self in result:
            return result
        result.append(self)
        for transform in self.lf_direct_subtransforms:
            transform.lf_all_transforms(result)
        return result

    @property
    def lf_direct_subtransforms(self):
        """Iterate over the direct subtransforms of this. """
        # pylint: disable=no-self-use
        raise NotImplementedError

    def lf_dumps(self) -> str:
        """Dump the transform as python code. """
        scope = thingfinder.Scope.toplevel(inspector.caller_module())
        graph, scopemap = self._lf_build_codegraph(name='_lf_main', scope=scope)
        unscoped = var2mod.unscope_graph(graph, scopemap)
        return var2mod.dumps_graph(unscoped)

    def _lf_shortname(self):
        title = self._lf_title()
        if self._lf_name is not None:
            return title + f'[{self._lf_name}]'
        varname = self.lf_varname()
        if varname is None or varname == title:
            return title
        return title + f'[{varname}]'

    @staticmethod
    def _add_parentheses_if_needed(name):
        return name

    @staticmethod
    def _lf_add_format_to_str(name):
        """
        Create formatted output based on "name" input lines.

        :param name: line or lines of input
        """
        res = '    ' + '\n    '.join([make_bold(x) for x in name.split('\n')]) + '\n'
        return res

    def _lf_bodystr(self):
        return NotImplemented

    def lf_repr(self, indent: int = 0) -> str:
        # pylint: disable=unused-argument
        varname = self.lf_varname()
        evaluable_repr = self.lf_evaluable_repr()
        if varname is None or varname == evaluable_repr:
            return f'{evaluable_repr}'
        return f'{evaluable_repr} [{varname}]'

    def __repr__(self) -> str:
        top_message = '\33[1m' + Transform._lf_shortname(self) + ':\33[0m\n\n'
        bottom_message = self._lf_bodystr()
        return top_message + self._lf_add_format_to_str(bottom_message)

    def _lf_find_varname(self, scopedict: dict) -> Optional[str]:
        """Find the name of the variable name the transform was last assigned to.

        :returns: A string with the variable name or *None* if the transform has not been assigned
            to any variable.
        """
        try:
            return [
                k for k, v in scopedict.items()
                if v is self and not k.startswith('_')
            ][0]
        except IndexError:
            return None

    def lf_varname(self) -> Optional[str]:
        """The name of the variable name the transform was last assigned to.

        Example:

        >>> foo = MyTransform()
        >>> foo._lf_varname
        "foo"

        :returns: A string with the variable name or *None* if the transform has not been assigned
            to any variable.
        """
        if self._lf_varname is _notset:
            self._lf_varname = self._lf_find_varname(self._lf_call_info.module.__dict__)
        return self._lf_varname

    def _lf_set_varname(self, val):  # TODO: needed (used in wrap, but can be done without "set" method potentially)
        self._lf_varname = val

    def _lf_forward_device_check(self):
        """Check all transform in forward are in correct device

        All transforms in forward need to be in same device as specified for
        the whole CompoundTransform.

        :return: Bool
        """
        for layer in self.lf_forward.lf_layers:
            for parameters in layer.parameters():
                if parameters.device.type != self.lf_device:
                    raise WrongDeviceError(self, layer)
        return True

    def _lf_unpack_argument(self, arg):
        """Returns True if to unpack argument else False"""
        signature_count = 0
        if not isinstance(arg, (list, tuple)):
            return False

        if hasattr(self, '_lf_number_of_inputs') and self._lf_number_of_inputs is not None:
            return self._lf_number_of_inputs > 1

        try:
            parameters = self.lf_get_signature().values()
        except ValueError:
            return False
        for param in parameters:
            if param.kind in (
                    param.POSITIONAL_OR_KEYWORD,
                    param.POSITIONAL_ONLY):
                signature_count += 1
            if param.kind == param.VAR_POSITIONAL:
                return True
        if signature_count > 1:
            return True
        return False

    def _lf_call_transform(self, arg, stage: Optional[Stage] = None):
        """Call transform with possibility to pass multiple arguments"""

        if stage in ('eval', 'infer'):
            torch_context = torch.no_grad()
        else:
            torch_context = contextlib.suppress()

        with self.lf_set_stage(stage), torch_context:
            if self._lf_unpack_argument(arg):
                return self(*arg)
            return self(arg)

    def lf_get_signature(self):
        return inspect.signature(self).parameters

    def _lf_callyield(self, args, stage: Stage, loader_kwargs: Optional[dict] = None,
                      verbose: bool = False, flatten: bool = False):  # TODO: different name?
        """Create a data loader and run preprocessing, forward, and postprocessing steps.

        :param args: Arguments to call with.
        :param stage: Stage to call in ("eval", "train" or "infer")
        :param loader_kwargs: Data loader keyword arguments.
        :param verbose: If *True*, print progress bar.
        :param flatten: If *True*, flatten the output.

        :returns: A generator that allows iterating over the output.
        """
        assert stage in ('eval', 'train'), '_lf_callyield can only be used with stage eval or train'

        self._lf_forward_device_check()

        preprocess = self.lf_preprocess
        forward = self.lf_forward
        post = self.lf_postprocess

        use_preprocess = not preprocess.lf_is_identity
        use_forward = not forward.lf_is_identity
        use_post = not post.lf_is_identity

        if use_preprocess:
            iterator = SimpleIterator(
                args,
                lambda *args: self.lf_preprocess._lf_call_transform(*args, stage)
            )
            if loader_kwargs is None:
                loader_kwargs = {}
            loader = self._lf_get_loader(iterator=iterator, loader_kwargs=loader_kwargs)
        else:
            loader = args

        pbar = None
        if verbose:
            if flatten:
                pbar = tqdm(total=len(args))
            else:
                loader = tqdm(loader, total=len(loader))

        for batch in loader:
            if use_forward:
                output = forward._lf_call_transform(batch, stage)
            else:
                output = batch

            if use_post:
                output = post._lf_call_transform(output, stage)

            if flatten:
                pbar.update()
                if not use_post:
                    output = Unbatchify()(batch)
                yield from output
                continue

            yield output

    @property
    def lf_device(self) -> str:  # TODO: remove?
        """Return the device the transform is on."""
        return self._lf_device

    @property
    def lf_component(self) -> Set[Component]:
        """Return the component (preprocess, forward or postprocess)."""
        return self._lf_component

    @property
    def lf_preprocess(self) -> "Transform":
        """The preprocessing part. """
        if 'preprocess' in self.lf_component:
            return self
        return Identity()

    def _lf_forward_part(self) -> "Transform":
        """The forward part of the transform """
        if 'forward' in self.lf_component:
            return self
        return Identity()

    @property
    def lf_forward(self) -> "Transform":
        """The forward part of the transform and send to GPU"""
        f = self._lf_forward_part()
        return f

    @property
    def lf_postprocess(self) -> "Transform":
        """The postprocessing part of the transform. """
        if 'postprocess' in self.lf_component:
            return self
        return Identity()

    def lf_to(self, device: str):  # TODO: change
        """Set the transform's device to *device*.

        :param device: device on which to map {'cpu', 'cuda', 'cuda:N'}
        """
        self._lf_device = device
        for layer in self.lf_layers:
            layer.to(device)
        return self

    @property
    def lf_is_identity(self):  # TODO: keep?
        """Return *True* iff the transform is the identity transform. """
        return False

    @property
    def lf_layers(self) -> List[torch.nn.Module]:
        """Get a dict with all layers in the transform (including layers in sub-transforms)."""
        layers = []
        for subtrans in self.lf_all_transforms():
            if isinstance(subtrans, torch.nn.Module):
                layers.append(subtrans)
        return layers

    def lf_parameters(self) -> Iterator:
        """ Iterate over parameters. """
        for layer in self.lf_layers:
            yield from layer.parameters()

    @contextlib.contextmanager
    def lf_set_stage(self, stage: Optional[str]=None):
        """Set of stage of Transform

        :param stage: stage ('train', 'eval', 'infer')
        """
        assert stage in ('train', 'eval', 'infer', None)

        if stage is None:
            yield
            return

        layers = self.lf_layers  # TODO: set back?
        try:
            for layer in layers:
                if stage == 'train':
                    layer.train()
                else:
                    layer.eval()
            Transform.lf_stage = stage
            yield
        # TODO: Should we put layers in eval mode by default?
        finally:
            for layer in layers:
                layer.eval()
            Transform.lf_stage = None

    @staticmethod
    def _lf_get_loader(iterator, loader_kwargs=None):
        """Get the data loader

        :param iterator: Iterator
        :param loader_kwargs: key word arguments for the data loader
        """
        loader = DataLoader(
            iterator,
            worker_init_fn=lambda _: np.random.seed(),
            **loader_kwargs
        )
        return loader

    def infer_apply(self, input):
        """Call transform within the infer context.

        This expects a single argument and returns a single output.
        """
        return self._lf_call_transform(input, stage='infer')

    def eval_apply(self, inputs: Iterable,
                   verbose: bool = False, flatten: bool = False, **kwargs):
        """Call transform within the eval context.

        This expects an iterable input and returns a generator.

        :param inputs: The arguments - an iterable (e.g. list) of inputs.
        :param kwargs: Keyword arguments to be passed on to the dataloader. These can be
            any that a `torch.data.utils.DataLoader` accepts.
        :param verbose: If *True*, print progress bar.
        :param flatten: If *True*, flatten the output.
        """
        return self._lf_callyield(inputs, 'eval', loader_kwargs=kwargs,
                                  verbose=verbose, flatten=flatten)

    def train_apply(self, inputs: Iterable,
                    verbose: bool = False, flatten: bool = False, **kwargs):
        """Call transform within the train context.

        This expects an iterable input and returns a generator.

        :param inputs: The arguments - an iterable (e.g. list) of inputs.
        :param kwargs: Keyword arguments to be passed on to the dataloader. These can be
            any that a `torch.data.utils.DataLoader` accepts.
        :param verbose: If *True*, print progress bar.
        :param flatten: If *True*, flatten the output.
        """
        return self._lf_callyield(inputs, 'train', loader_kwargs=kwargs,
                                  verbose=verbose, flatten=flatten)


class AtomicTransform(Transform):
    """Base class for "atomic" transforms (transforms that are not made by combining
    other transforms - in contrast to `CompoundTransform`s).

    Examples of `AtomicTransform`s are `ClassTransform`s and `FunctionTransform`s.

    :param call:
    :param call_info:
    :param lf_name: name of the transform
    """

    def __init__(self, call: str, call_info: Optional[inspector.CallInfo] = None,
                 lf_name: Optional[str] = None):
        super().__init__(call_info, lf_name)
        self._lf_call = call

    def lf_evaluable_repr(self, indent=0, var_transforms=None):
        if var_transforms is None:
            var_transforms = {}
        return var_transforms.get(self, self._lf_call)

    def _lf_title(self):
        return self._lf_call

    @property
    def lf_direct_subtransforms(self):
        # pylint: disable=no-self-use
        globals_dict, nonlocals_dict = self._lf_closurevars
        for v in chain(self.__dict__.values(), globals_dict.values(), nonlocals_dict.values()):
            if isinstance(v, Transform):
                yield v


class FunctionTransform(AtomicTransform):
    """Function Transform

    :param function: function to call
    :param call_info:
    :param lf_name: name of the transform
    :param call:
    """
    def __init__(self, function, call_info, lf_name=None, call=None):
        if call is None:
            call = function.__name__
        super().__init__(call=call, call_info=call_info, lf_name=lf_name)
        self.function = function
        self._lf_number_of_inputs = None

    @property
    def source(self, length=20):
        try:
            body_msg = inspect.getsource(self.function)
            body_msg = ''.join(re.split('(def )', body_msg, 1)[1:])
            lines = re.split('(\n)', body_msg)
            lines = ''.join(lines[:length]) + ('  ...' if len(lines) > length else '')
            if len(lines) == 0:
                body_msg = ''.join(re.split('(lambda)', self._lf_call, 1)[1:])[:-1]
                return body_msg[:100]
            return lines
        except TypeError:
            return self._lf_call

    def _lf_bodystr(self, length=20):
        return self.source

    def _lf_title(self):
        title = self._lf_call
        if '(' in title:
            return re.split('\(', title)[-1][:-1]
        return title

    @property
    def _lf_closurevars(self) -> inspect.ClosureVars:
        try:
            closurevars = inspect.getclosurevars(self.function)
        except TypeError as exc:
            warn(f"Couln't get closurevars ({exc}). This is usually fine.")
            return {}, {}
        return closurevars.globals, closurevars.nonlocals

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class ClassTransform(AtomicTransform):
    """Class Transform.

    :param lf_name: Name of the transform.
    """

    def __init__(self, lf_name=None, ignore_scope=False):
        caller_frameinfo = inspector.non_init_caller_frameinfo()
        call_info = inspector.CallInfo(caller_frameinfo, ignore_scope=ignore_scope)
        call = inspector.get_segment_from_frame(caller_frameinfo.frame, 'call')
        AtomicTransform.__init__(
            self,
            call=call,
            call_info=call_info,
            lf_name=lf_name
        )

    @property
    def source(self, length=40):
        try:
            body_msg = thingfinder.find(self.__class__.__name__)[0]
            body_msg = ''.join(re.split('(class )', body_msg, 1)[1:])
            lines = re.split('(\n)', body_msg)
            return ''.join(lines[:length]) + ('  ...' if len(lines) > length else '')
        except thingfinder.ThingNotFound:
            return self._lf_call

    def _lf_title(self):
        title = self._lf_call
        if title.count('(') == 2:
            title = re.split('\(', title)
            title = re.split('\)', ''.join(title[1:]))[:-1]
            return '('.join(title) + ')'
        return title

    def _lf_bodystr(self):
        return self.source


class TorchModuleTransform(ClassTransform):
    """Torch Module Transform"""
    def lf_get_signature(self):
        return inspect.signature(self.forward).parameters

    def lf_pre_save(self, path, i):
        """
        :param path: The save path.
        :param i: Sublayer index.
        """
        path = Path(path)
        checkpoint_path = path / f'{path.stem}_{i}.pt'
        print('saving torch module to', checkpoint_path)
        torch.save(self.state_dict(), checkpoint_path)

    def lf_post_load(self, path, i):
        """
        :param path: The load path.
        :param i: Sublayer index.
        """
        path = Path(path)
        checkpoint_path = path / f'{path.stem}_{i}.pt'
        print('loading torch module from', checkpoint_path)
        self.load_state_dict(torch.load(checkpoint_path))


class CompoundTransform(Transform):
    """Abstract base class for compound-transforms (transforms combining other transforms).

    :param transforms: list of transforms
    :param call_info:
    :param lf_name: name of CompoundTransform
    :param lf_group:
    """
    op = NotImplemented

    def __init__(self, transforms, call_info=None, lf_name=None, lf_group=False):
        super().__init__(call_info, lf_name)

        self._lf_group = True if lf_name is not None else lf_group
        self._lf_preprocess = None
        self._lf_forward = None
        self._lf_postprocess = None

        transforms = self._flatten_list(transforms)
        self.transforms = transforms

        self._lf_component_list = [t.lf_component for t in self.transforms]
        try:
            self._lf_component = set.union(*self._lf_component_list)
        except (AttributeError, TypeError):
            self._lf_component = None

    def __sub__(self, name: str) -> "Transform":
        """Create a named clone of the transform.

        Example:
            named_t = t - 'rescale image'
        """
        named_copy = copy(self)
        named_copy._lf_name = name
        named_copy._lf_group = True
        return named_copy

    def __getitem__(self, item : Union[int, slice, str]) -> Transform:
        """Get item

        If int, gets item'th transform in this CompoundTransform.
        If slice, gets sliced transform of same type
        If str, gets first transform with name item

        :param item: Should be of type {int, slice, str}
        """
        if isinstance(item, int):
            return self.transforms[item]
        if isinstance(item, slice):
            return type(self)(self.transforms[item])
        if isinstance(item, str):
            for transform_ in self.transforms:
                if transform_.lf_name == item:
                    return transform_
            raise ValueError(f"{item}: Transform with lf_name '{item}' not found")
        raise TypeError('Unknown type for get item: expected type {int, slice, str}')

    def lf_evaluable_repr(self, indent=0, var_transforms=None):
        sub_reprs = [
            x.lf_varname() or x.lf_evaluable_repr(indent + 4, var_transforms)
            for x in self.transforms
        ]
        result = (
            '(\n    ' + ' ' * indent
            + ('\n' + ' ' * indent + f'    {self.op} ').join(sub_reprs)
            + '\n' + ' ' * indent + ')'
        )
        if self._lf_group:
            result = 'lf.group' + result
        return result

    def _lf_build_codegraph(self, graph=None, scopemap=None, name=None, scope=None):
        if graph is None:
            graph = {}
        if scopemap is None:
            scopemap = {}

        start = self._lf_codegraph_startnode(name)

        if self._lf_group and 'lf' not in graph:
            graph['lf', scope] = var2mod.CodeNode.from_source('import lf', scope)
            scopemap['lf', scope] = scope

        if name is not None:
            assert scope is not None
            graph[name, scope] = start
            scopemap[name, scope] = scope

        for transform in self.transforms:
            varname = transform.lf_varname()
            transform._lf_build_codegraph(graph, scopemap, varname,
                                          self._lf_call_info.scope)
        return graph, scopemap

    def lf_repr(self, indent=0):
        sub_reprs = [
            x.lf_repr(indent + 4)
            for x in self.transforms
        ]
        res = (
            '(\n    ' + ' ' * indent
            + ('\n' + ' ' * indent + f'    {self.op} ').join(sub_reprs)
            + '\n' + ' ' * indent + ')'
        )
        if self.lf_varname() is not None and self.lf_varname() is not _notset:
            res += f' [{self.lf_varname()}]'
        return res

    def _add_parentheses_if_needed(self, name):
        if self._lf_name is None:
            return '(' + name + ')'
        return name

    def _lf_shortname(self):
        if self._lf_name is None:
            return self._lf_bodystr(is_child=True)
        else:
            return super()._lf_shortname()

    def _lf_title(self):
        return self.__class__.__name__

    def _lf_bodystr(self, is_child=False):
        sep = f' {self.op} ' if is_child else '\n'
        if is_child:
            return sep.join(t._add_parentheses_if_needed(t._lf_shortname()) for t in self.transforms)
        return sep.join(t._lf_shortname() for t in self.transforms)

    def _lf_add_format_to_str(self, name):
        """
        Create formatted output based on "name" input lines. For multi-line inputs
        the lines are infixed with *self.display_op*

        :param name: line or lines of input
        """
        res = f'\n        {make_green(self.display_op)}  \n'.join(
            [make_bold(f'{i}: ' + x) for i, x in enumerate(name.split('\n'))]) + '\n'
        return res

    def lf_to(self, device: str):
        """Set the transform's device to *device*

        :param device: device on which to send {'cpu', cuda', 'cuda:N'}
        """
        self._lf_device = device
        for transform_ in self.transforms:
            transform_.lf_to(device)
        return self

    def _lf_forward_device_check(self):
        """Check all transform in forward are in correct device

        All transforms in forward need to be in same device as specified for
        the whole CompoundTransform.

        :return: Bool
        """
        return_val = True

        if isinstance(self.lf_forward, type(self)):
            for transform_ in self.lf_forward.transforms:
                if self.lf_device != transform_.lf_device:
                    raise WrongDeviceError(self, transform_)
                return_val = transform_._lf_forward_device_check()
            return return_val

        if self.lf_device != self.lf_forward.lf_device:
            raise WrongDeviceError(self, self.lf_forward)

        return self.lf_forward._lf_forward_device_check()

    @classmethod
    def _flatten_list(cls, transform_list: List[Transform]):
        """Flatten *list_* such that members of *cls* are not nested.

        :param transform_list: List of transforms.
        """
        list_flat = []

        for transform in transform_list:
            if isinstance(transform, cls):
                if transform._lf_group:
                    list_flat.append(transform)
                else:
                    list_flat += transform.transforms
            else:
                list_flat.append(transform)

        return list_flat

    @property
    def lf_direct_subtransforms(self):
        yield from self.transforms

    def grouped(self):
        """Return a grouped version of *self*. """
        return type(self)(self.transforms, self._lf_call_info, lf_name=self.lf_name, lf_group=True)

    @staticmethod
    def _lf_get_keys(transforms):
        """Get deduplicated keys from list of transforms

        Names are updated as below.
        [None, None, 'a', 'a', 'b', None] -> ['out_0', 'out_1', 'a_0', 'a_1', 'b', 'out_5']

        :param transforms: list of transforms
        :return: list of keys
        """
        names = []
        for ind, transform_ in enumerate(transforms):
            if transform_.lf_name is None:
                name = 'out_'+str(ind)
            else:
                name = transform_.lf_name
            names.append(name)

        counter = Counter(names)
        updated_counter = Counter()
        deduped_keys = []

        for name in names:
            new_name = name + '_' + str(updated_counter[name]) if counter[name] > 1 else name
            updated_counter.update({name: 1})
            deduped_keys.append(new_name)
        return deduped_keys


class Compose(CompoundTransform):
    """Apply series of transforms on input.

    Compose([t1, t2, t3])(x) = t3(t1(t2(x)))

    :param transforms: List of transforms to compose.
    :param call_info:
    :param lf_name: name of the Compose transform
    :param lf_group:
    :return: output from series of transforms
    """
    op = '>>'
    display_op = '↓'

    def __init__(self, transforms, call_info=None, lf_name=None, lf_group=False):
        super().__init__(transforms, call_info=call_info, lf_name=lf_name, lf_group=lf_group)

        preprocess_end = 0
        postprocess_start = len(self.transforms)
        set_postprocess = True
        for i, transform_ in enumerate(self.transforms):
            if 'preprocess' in transform_.lf_component:
                preprocess_end = i
            if 'postprocess' in transform_.lf_component and set_postprocess:
                postprocess_start = i
                set_postprocess = False
        for i in range(preprocess_end):
            self._lf_component_list[i] = {'preprocess'}
        for i in range(postprocess_start+1, len(self.transforms)):
            self._lf_component_list[i] = {'postprocess'}

    @property
    def n_display_inputs(self):
        return self.transforms[0].n_display_inputs

    @property
    def n_display_outputs(self):
        return self.transforms[-1].n_display_outputs

    def __repr__(self) -> str:
        top_message = '\33[1m' + Transform.lf_shortname(self) + ':\33[0m\n\n'
        return top_message + self._lf_write_arrows_to_rows()

    def _lf_write_arrows_to_rows(self):
        """
        Create formatted output based on "name" input lines. For multi-line inputs
        the lines are infixed with *self.display_op*

        :param name: line or lines of input
        """
        # output = [make_bold('0: ' + rows[0])]

        # pad the components of rows which are shorter than other parts in same column
        # rows = [re.split(r'\/|\+', x) for x in rows]
        rows = [
            [s.lf_shortname().strip() for s in t.transforms]
            if isinstance(t, CompoundTransform)
            else [t.lf_shortname()]
            for t in self.transforms
        ]

        children_widths = [[len(x) for x in row] for row in rows]
        # get maximum widths in "columns"
        children_widths_matrix = np.zeros((len(self.transforms),
                                           max([len(x) for x in children_widths])))
        for i, cw in enumerate(children_widths):
            children_widths_matrix[i, :len(cw)] = cw
        max_widths = np.max(children_widths_matrix, 0)

        for i, r in enumerate(rows):
            for j in range(len(rows[i])):
                if len(rows[i][j]) < max_widths[j]:
                    rows[i][j] += ' ' * (int(max_widths[j]) - len(rows[i][j]))

        for i, r in enumerate(rows):
            if len(r) > 1:
                rows[i] = f' {self.transforms[i].display_op} '.join(r)
            else:
                rows[i] = r[0]
        output = []
        # iterate through rows and create arrows depending on numbers of components
        for i, (r, t) in enumerate(zip(rows, self.transforms)):
            widths = [0]
            subarrows = []

            # if subsequent rows have the same number of "children" transforms
            if i > 0 and len(children_widths[i]) == len(children_widths[i - 1]):
                for j, w in enumerate(children_widths[i]):
                    subarrows.append(create_arrow(sum(widths) - j + j * 4, 0, 0, 0))
                    widths.append(int(max_widths[j]))

            # if previous row has multiple outputs and current row just one input
            elif i > 0 and len(children_widths[i]) == 1 \
                    and len(children_widths[i - 1]) > 1:
                for j, w in enumerate(children_widths[i - 1]):
                    subarrows.append(create_reverse_arrow(
                        j, sum(widths) - j + j * 3,
                        len(children_widths[i - 1]) - j + 1, j + 1
                    ))
                    widths.append(int(max_widths[j]))

            # if previous row has one output and current row has multiple inputs
            else:
                for j, w in enumerate(children_widths[i]):
                    subarrows.append(create_arrow(j, sum(widths) - j + j * 3,
                                                  len(children_widths[i]) - j, j + 1))
                    widths.append(int(max_widths[j]))

            # add signature names to the arrows
            tuple_to_str = lambda x: '(' + ', '.join([str(y) for y in x]) + ')'
            if isinstance(t, Rollout) or isinstance(t, Parallel):
                all_params = []
                for tt in t.transforms:
                    all_params.append(list(tt.lf_get_signature().keys()))
                to_combine = [
                    ' ' * (sum(widths[:k + 1]) + 3 * k + 2) + tuple_to_str(params)
                    if len(params) > 1
                    else ' ' * (sum(widths[:k + 1]) + 3 * k + 2) + params[0]
                    for k, params in enumerate(all_params)
                ]
                to_format = combine_multi_line_strings(to_combine)
            else:
                padder = (len(subarrows) + 1) * ' '
                params = [x for x in t.lf_get_signature()]
                to_format = padder + tuple_to_str(params) if len(params) > 1 else padder + params[0]
            to_format_pad_length = max([len(x.split('\n')) for x in subarrows]) - 1
            to_format = ''.join(['\n' for _ in range(to_format_pad_length)] + [to_format])

            # combine the arrows
            mark = combine_multi_line_strings(subarrows + [to_format])
            mark = '\n'.join(['   ' + x for x in mark.split('\n')])
            output.append(make_green(mark))
            output.append(make_bold(f'{i + 1}: {r}'))
        return '\n'.join(output)

    def __call__(self, arg):
        """Call method for Compose

        :param arg: arguments to call with
        :return: output from series of transforms
        """
        for transform_ in self.transforms:
            arg = transform_._lf_call_transform(arg)
        return arg

    def _lf_forward_part(self):
        """Forward part of transforms"""
        if self._lf_forward is None:
            t_list = []
            for transform_, component_set in zip(self.transforms, self._lf_component_list):
                if 'forward' in component_set:
                    if len(component_set) == 1:
                        t_list.append(transform_)
                    else:
                        t_list.append(transform_.lf_forward)

            if len(t_list) == 1:
                self._lf_forward = t_list[0]
            elif t_list:
                self._lf_forward = Compose(t_list, call_info=self._lf_call_info)
            else:
                self._lf_forward = Identity()

        return self._lf_forward

    @property
    def lf_preprocess(self):
        if self._lf_preprocess is None:
            t_list = []
            for transform_, component_set in zip(self.transforms, self._lf_component_list):
                if 'preprocess' in component_set:
                    if len(component_set) == 1:
                        t_list.append(transform_)
                    else:
                        t_list.append(transform_.lf_preprocess)

            if len(t_list) == 1:
                self._lf_preprocess = t_list[0]
            elif t_list:
                self._lf_preprocess = Compose(t_list, call_info=self._lf_call_info)
            else:
                self._lf_preprocess = Identity()

        return self._lf_preprocess

    @property
    def lf_postprocess(self):
        if self._lf_postprocess is None:
            t_list = []
            for transform_, component_set in zip(self.transforms, self._lf_component_list):
                if 'postprocess' in component_set:
                    if len(component_set) == 1:
                        t_list.append(transform_)
                    else:
                        t_list.append(transform_.lf_postprocess)

            if len(t_list) == 1:
                self._lf_postprocess = t_list[0]
            elif t_list:
                self._lf_postprocess = Compose(t_list, call_info=self._lf_call_info)
            else:
                self._lf_postprocess = Identity()
        return self._lf_postprocess


class Rollout(CompoundTransform):
    """Apply a list of transform to same input and get tuple output

    Rollout([t1, t2, ...])(x) := (t1(x), t2(x), ...)

    :param transforms: List of transforms to rollout.
    :param call_info:
    :param lf_name: name of the Rollout transform
    :param lf_group:
    :return: namedtuple of outputs
    """
    op = '+'
    display_op = '+'

    def __init__(self, transforms, call_info=None, lf_name=None, lf_group=False):
        super().__init__(transforms, call_info=call_info, lf_name=lf_name, lf_group=lf_group)
        self.lf_keys = self._lf_get_keys(self.transforms)
        self._lf_output_format = namedtuple('namedtuple', self.lf_keys)

    @property
    def n_display_inputs(self):
        return len(self.transforms)

    @property
    def n_display_outputs(self):
        return len(self.transforms)

    @property
    def children_widths(self):
        return [t.display_width for t in self.transforms]

    def __call__(self, arg):
        """Call method for Rollout

        :param arg: Argument to call with
        :return: namedtuple of outputs
        """
        out = []
        for transform_ in self.transforms:
            out.append(transform_._lf_call_transform(arg))
        out = self._lf_output_format(*out)
        return out

    @property
    def lf_preprocess(self):
        if self._lf_preprocess is None:
            t_list = [x.lf_preprocess for x in self.transforms]
            if all([isinstance(t, Identity) for t in t_list]):
                self._lf_preprocess = Identity()
            else:
                self._lf_preprocess = Rollout(t_list, call_info=self._lf_call_info)
        return self._lf_preprocess

    def _lf_forward_part(self):
        if self._lf_forward is None:
            t_list = [x.lf_forward for x in self.transforms]
            if all([isinstance(t, Identity) for t in t_list]):
                self._lf_forward = Identity()
            elif 'preprocess' in self._lf_component and 'forward' in self._lf_component:
                self._lf_forward = Parallel(t_list, call_info=self._lf_call_info)
            else:
                self._lf_forward = Rollout(t_list, call_info=self._lf_call_info)
        return self._lf_forward

    @property
    def lf_postprocess(self):
        if self._lf_postprocess is None:
            t_list = [x.lf_postprocess for x in self.transforms]
            if all([isinstance(t, Identity) for t in t_list]):
                self._lf_postprocess = Identity()
            elif len(list(self._lf_component)) >= 2 and 'postprocess' in self._lf_component:
                self._lf_postprocess = Parallel(t_list, call_info=self._lf_call_info)
            else:
                self._lf_postprocess = Rollout(t_list, call_info=self._lf_call_info)
        return self._lf_postprocess


class Parallel(CompoundTransform):
    """Apply transforms in parallel to a tuple of inputs and get tuple output

    Parallel([f1, f2, ...])((x1, x2, ..)) := (f1(x1), f2(x2), ...)

    :param transforms: List of transforms to parallelize.
    :param call_info:
    :param lf_name: name of the Parallel transform
    :param lf_group:
    :return: namedtuple of outputs
    """
    op = '/'
    display_op = '/'

    def __init__(self, transforms, call_info=None, lf_name=None, lf_group=False):
        super().__init__(transforms, call_info=call_info, lf_name=lf_name, lf_group=lf_group)
        self.lf_keys = self._lf_get_keys(self.transforms)
        self._lf_output_format = namedtuple('namedtuple', self.lf_keys)

    @property
    def n_display_inputs(self):
        return len(self.transforms)

    @property
    def n_display_inputs(self):
        return len(self.transforms)

    @property
    def children_widths(self):
        return [t.display_width for t in self.transforms]

    def __call__(self, arg):
        """Call method for Parallel

        :param arg: Argument to call with.
        :return: Namedtuple of output.
        """
        out = []
        for ind, transform_ in enumerate(self.transforms):
            out.append(transform_._lf_call_transform(arg[ind]))
        out = self._lf_output_format(*out)
        return out

    @property
    def lf_preprocess(self):
        if self._lf_preprocess is None:
            t_list = [x.lf_preprocess for x in self.transforms]
            if all([isinstance(t, Identity) for t in t_list]):
                self._lf_preprocess = Identity()
            else:
                self._lf_preprocess = Parallel(t_list, call_info=self._lf_call_info)
        return self._lf_preprocess

    def _lf_forward_part(self):
        if self._lf_forward is None:
            t_list = [x.lf_forward for x in self.transforms]
            if all([isinstance(t, Identity) for t in t_list]):
                self._lf_forward = Identity()
            else:
                self._lf_forward = Parallel(t_list, call_info=self._lf_call_info)
        return self._lf_forward

    @property
    def lf_postprocess(self):
        if self._lf_postprocess is None:
            t_list = [x.lf_postprocess for x in self.transforms]
            if all([isinstance(t, Identity) for t in t_list]):
                self._lf_postprocess = Identity()
            else:
                self._lf_postprocess = Parallel(t_list, call_info=self._lf_call_info)
        return self._lf_postprocess


class BuiltinTransform(AtomicTransform):
    def __init__(self, call):
        super().__init__(call)

    def _lf_build_codegraph(self, graph: Optional[dict] = None,
                            scopemap: Optional[dict] = None,
                            name: Optional[str] = None,
                            scope: Optional[thingfinder.Scope] = None) -> Tuple[dict, dict]:  # TODO: refactor
        if graph is None:
            graph = {}
        if scopemap is None:
            scopemap = {}

        if scope is None:
            scope = thingfinder.Scope.empty()
        if ('lf', scope) not in graph:
            graph['lf', scope] = var2mod.CodeNode.from_source('import lf', scope)
            scopemap['lf', scope] = scope

        start_source = f'{name or "_lf_dummy"} = {self._lf_call}'

        graph[self.__class__.__name__, scope] = \
            var2mod.CodeNode.from_source(start_source, scope)

        scopemap[self.__class__.__name__, scope] = scope

        return graph, scopemap

    def _lf_bodystr(self):
        return self._lf_call.split('lf.')[-1]

    def _lf_title(self):
        return self._lf_call.split('lf.')[-1].split('(')[0]


class Identity(BuiltinTransform):
    """Do nothing.

    :param lf_name: name of the transform
    """

    def __init__(self):
        super().__init__('lf.Identity()')

    @property
    def lf_is_identity(self):
        return True

    def __call__(self, args):
        return args


class Unbatchify(ClassTransform):
    """Mark start of postprocessing

    Unbatchify removes batch dimension (inverse of Batchify) and moves the input tensors to 'cpu'.

    :param dim: batching dimension
    :param cpu: if true, moves output to cpu after unbatchify
    """

    def __init__(self, dim=0, cpu=True):
        super().__init__()
        self.dim = dim
        self._lf_component = {'postprocess'}
        self.cpu = cpu

    def _move_to_device(self, args):
        if isinstance(args, (tuple, list)):
            return tuple([self._move_to_device(x) for x in args])
        if isinstance(args, torch.Tensor):
            return args.to('cpu')
        return args

    def __call__(self, args):
        assert Transform.lf_stage is not None,\
            'Stage is not set, use infer_apply, eval_apply or train_apply'

        if Transform.lf_stage != 'infer':
            return self._move_to_device(args) if self.cpu else args
        if isinstance(args, tuple):
            return tuple([self(x) for x in args])
        if isinstance(args, torch.Tensor):
            args = args.squeeze(self.dim)
            return args.to('cpu') if self.cpu else args

        raise TypeError('only tensors and tuples of tensors recursively supported...')


class Batchify(ClassTransform):
    """Mark end of preprocessing.

    Batchify adds batch dimension at *dim*. During inference, this unsqueezes tensors and,
    recursively, tuples thereof. Batchify also moves the input tensors to device specified
    for the transform.

    :param dim: batching dimension
    """

    def __init__(self, dim=0):
        super().__init__()
        self.dim = dim
        self._lf_component = {'preprocess'}

    def _move_to_device(self, args):
        if isinstance(args, (tuple, list)):
            return tuple([self._move_to_device(x) for x in args])
        if isinstance(args, torch.Tensor):
            return args.to(self.lf_device)
        return args

    def __call__(self, args):
        assert Transform.lf_stage is not None,\
            'Stage is not set, use infer_apply, eval_apply or train_apply'

        if Transform.lf_stage != 'infer':
            return self._move_to_device(args)
        if isinstance(args, (tuple, list)):
            return tuple([self(x) for x in args])
        if isinstance(args, torch.Tensor):
            return args.unsqueeze(self.dim).to(self.lf_device)
        if isinstance(args, (float, int)):
            return torch.tensor([args]).to(self.lf_device)
        raise TypeError('only tensors and tuples of tensors recursively supported...')


def save(transform: Transform, path):
    transform.lf_save(path)


def load(path):
    """Load transform (as saved with lf.save) from *path*. """
    path = Path(path)
    with open(path / 'transform.py') as f:
        source = f.read()
    module = types.ModuleType('lfload')
    module.__dict__.update({
        '_lf_source': source,
        '_lf_module': module,
        '__file__': str(path / 'transform.py')
    })
    code = compile(source, path/'transform.py', 'exec')
    exec(code, module.__dict__)
    transform = module._lf_main
    for i, subtrans in enumerate(transform.lf_all_transforms()):
        subtrans.lf_post_load(path, i)
    return transform


def group(transform: Union[Rollout, Parallel]):
    return transform.grouped()
