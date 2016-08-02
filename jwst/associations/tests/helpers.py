"""Helpers for tests."""
from collections import namedtuple
from glob import iglob
import os
import pytest
import re

from astropy.table import (Table, vstack)

from .. import (AssociationRegistry, AssociationPool, generate)
from ..association import is_iterable


# Define how to setup initial conditions with pools.
class PoolParams(
        namedtuple('PoolParams',
                   [
                       'path',
                       'n_asns',
                       'n_orphaned',
                       'candidates',
                       'kwargs'
                   ]
        )
):
    def __new__(cls, path='',
                n_asns=0,
                n_orphaned=0,
                candidates=None,
                kwargs=None):
        if not kwargs:
            kwargs = {}
        if candidates is None:
            candidates = []
        return super(PoolParams, cls).__new__(
            cls,
            path,
            n_asns,
            n_orphaned,
            candidates,
            kwargs
        )


# Basic Pool/Rule test class
class BasePoolRule(object):

    # Define the pools and testing parameters related to them.
    # Each entry is a tuple starting with the path of the pool.
    pools = []

    # Define the rules that SHOULD be present.
    # Each entry is the class name of the rule.
    valid_rules = []

    def setup(self):
        """You set me up...."""

    def tearDown(self):
        """You tear me down..."""

    def test_rules_exist(self):
        rules = AssociationRegistry()
        assert len(rules) >= len(self.valid_rules)
        for rule in self.valid_rules:
            yield check_in_list, rule, rules

    def test_run_generate(self):
        rules = AssociationRegistry()
        for ppars in self.pools:
            pool = combine_pools(ppars.path, **ppars.kwargs)
            (asns, orphaned) = generate(pool, rules)
            yield check_equal, len(asns), ppars.n_asns
            yield check_equal, len(orphaned), ppars.n_orphaned
            for asn, candidates in zip(asns, ppars.candidates):
                yield check_equal, set(asn.candidates), set(candidates)


@pytest.fixture(scope='session')
def full_pool_rules():
    pool_files = iglob(t_path('data/pool_*.csv'))
    pool = combine_pools(pool_files)
    rules = AssociationRegistry()
    return (pool, rules)


# Basic utilities.
class Counter(object):
    """Like itertools.count but access to the current value"""
    def __init__(self, start=0, step=1, end=None):
        self.value = start
        self.step = step
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.end is not None and \
           abs(self.value) > abs(self.end):
            raise StopIteration
        self.value += self.step
        return self.value

    def next(self):
        """python2 compatibility"""
        return self.__next__()


def check_in_list(element, alist):
    assert element in alist


def check_not_in_list(element, alist):
    assert element not in alist


def check_equal(left, right):
    assert left == right


def not_none(value):
    assert value is not None


def t_path(partial_path):
    """Construction the full path for test files"""
    test_dir = os.path.dirname(__file__)
    return os.path.join(test_dir, partial_path)


def combine_pools(pools, **pool_kwargs):
    """Combine pools into a single pool

    Parameters
    ----------
    pools: str, astropy.table.Table, [str|Table, ...]
        The pools to combine. Either a singleton is
        passed or and iterable can be passed.
        The entries themselves can be either a file path
        or an astropy.table.Table-like object.

    pool_kwargs: dict
        Other keywoard arguments to pass to AssociationPool.read

    Returns
    -------
    AssociationPool|astropy.table.Table
        The combined pool
    """
    if not is_iterable(pools):
        pools = [pools]
    just_pools = []
    for pool in pools:
        if not isinstance(pool, Table):
            pool = AssociationPool.read(pool, **pool_kwargs)
        just_pools.append(pool)
    if len(just_pools) > 1:
        mega_pool = vstack(just_pools, metadata_conflicts='silent')
    else:
        mega_pool = just_pools[0].copy(copy_data=True)

    # Replace OBS_NUM and ASN_CANDIDATE_ID with actual numbers, if
    # necessary
    obsnum = Counter(start=0)
    acid = Counter(start=0)
    local_env = locals()
    for row in mega_pool:
        mega_pool[row.index] = [
            parse_value(v, local_env)
            for v in row
        ]

    return mega_pool


def parse_value(v, local_env):
    """Evaluate if indicated"""
    result = v
    try:
        m = re.match('#!(.+)', v)
    except TypeError:
        pass
    else:
        if m:
            result = eval(m.group(1), local_env)
    return result
