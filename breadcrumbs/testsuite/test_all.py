import breadcrumbs as bc


def test_context():

    c = bc.Crumb("start")

    bc.update_info(value_info=41)
    bc.update_extra(value=41)
    bc.put(bc.Crumb("_inner_c1"))

    with bc.context(c):
        bc.update_info(value_info=41)
        bc.update_extra(value=42)
        bc.put(bc.Crumb("_inner_c"))

    bc.update_info(value_info=41)
    bc.update_extra(value=43)
    bc.put(bc.Crumb("_inner_c2"))

    assert c.info == dict(value_info=41)
    assert c.extra == dict(value=42)
    assert len(c.entries) == 1
    assert c.entries[0].title == "_inner_c"


def test_nested_context():

    c1 = bc.Crumb("c1")
    c2 = bc.Crumb("c2")

    bc.update_extra(value=41)

    with bc.context(c1):
        bc.update_extra(value=-42)

        with bc.context(c2):
            bc.update_extra(value=42)

        bc.update_extra(another_value=0)

    bc.update_extra(value=43)

    assert c2.extra == dict(value=42)
    assert c1.extra == dict(value=-42, another_value=0)


def test_func():

    c = bc.Crumb("start")

    @bc.aware(trail_param="c")
    def sum(c, a, b=1):
        bc.update_extra(yes=True)
        return a + b

    assert sum(c, 1, 3) == 4
    t = c.entries
    assert len(t) == 1
    assert t[0].title == "test_func.<locals>.sum"
    assert t[0].info == dict(a=1, b=3)
    assert t[0].extra == dict(yes=True)


def test_func_defaults():

    c = bc.Crumb("start")

    @bc.aware(trail_param="c")
    def sum(c, a, b=1):
        bc.update_extra(yes=True)
        return a + b

    assert sum(c, 1) == 2
    t = c.entries
    assert len(t) == 1
    assert t[0].title == "test_func_defaults.<locals>.sum"
    assert t[0].info == dict(a=1, b=1)
    assert t[0].extra == dict(yes=True)


def test_func_redact():

    c = bc.Crumb("start")

    @bc.aware(trail_param="c", redact_params=("a",))
    def sum(c, a, b=1):
        bc.update_extra(yes=True)
        return a + b

    assert sum(c, 1, 3) == 4
    t = c.entries
    assert len(t) == 1
    assert t[0].title == "test_func_redact.<locals>.sum"
    assert t[0].info == dict(a=bc.REDACTED, b=3)
    assert t[0].extra == dict(yes=True)


def test_func_redact_str():

    c = bc.Crumb("start")

    @bc.aware(trail_param="c", redact_params="a")
    def sum(c, a, b=1):
        bc.update_extra(yes=True)
        return a + b

    assert sum(c, 1, 3) == 4
    t = c.entries
    assert len(t) == 1
    assert t[0].title == "test_func_redact_str.<locals>.sum"
    assert t[0].info == dict(a=bc.REDACTED, b=3)
    assert t[0].extra == dict(yes=True)
