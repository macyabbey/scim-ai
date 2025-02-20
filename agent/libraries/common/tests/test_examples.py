from scimaicommon.scimexampleobjects import full_enterprise_user, full_user, group, minimal_user


def test_objects_exist() -> None:
    """Test that the required objects exist.

    This test checks the existence of the following objects:
    - minimal_user
    - full_user
    - full_enterprise_user
    - group
    """
    assert minimal_user
    assert full_user
    assert full_enterprise_user
    assert group
