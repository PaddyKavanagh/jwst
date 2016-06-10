from jwst_tools.associations.association import AssociationRegistry
from jwst_tools.associations.pool import AssociationPool
from jwst_tools.associations.generate import generate


class TestUtilities():
    pool_file = 'tests/data/jw82600_001_20151107T165901_pool.csv'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_filter_cross_candidates(self):
        rules = AssociationRegistry()
        pool = AssociationPool.read(self.pool_file)
        (asns, orphaned) = generate(pool, rules)
        assert len(asns) == 11
        assert len(orphaned) == 298
        filtered = rules.Utility.filter_cross_candidates(asns)
        assert len(filtered) == 5
