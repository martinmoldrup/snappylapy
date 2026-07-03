# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_snapshot_snapshottest test_snapshot_dict'] = '''{
    "key": "value",
    "key2": "value2"
}'''

snapshots['test_snapshot_snapshottest_obj test_snapshot_dict'] = GenericRepr('<test_try_out_other_snapshot_packages.ObjectToSnapshot object at 0x0000020C2F097400>')
