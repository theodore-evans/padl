from padl.build import build
from tests.material.example_config.mystuff import create_transform, combine_transforms


t = build(
    create_transform,
    'create_1',
    a=1,
    b=2,
)

s = build(
    create_transform,
    'create_2',
    a=3,
    b=4
)

pl = build(
    combine_transforms,
    t1=t,
    t2=s,
)
