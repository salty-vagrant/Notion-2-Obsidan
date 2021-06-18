from knox.model import base as model


class TestLink:
    def test_link_equality(self):
        l1 = model.Link(name="l1", uri="http://example.com")
        l2 = model.Link(name="l2", uri="http://example.com")
        l3 = model.Link(name="l3", uri="http://www.example.com")
        assert l1 == l2
        assert l1 != l3
