from unittest.mock import DEFAULT, MagicMock, call


class ExtendedMock(MagicMock):
    def setup(self, *args, return_value=None, raises=None, **kwargs):
        rules = self.__dict__.setdefault("_setup_rules", [])
        rules.insert(0, (call(*args, **kwargs), return_value, raises))
        self.side_effect = self._answer_setup
        return self

    def _answer_setup(self, *args, **kwargs):
        received = call(*args, **kwargs)
        for expected, return_value, raises in self._setup_rules:
            if expected == received:
                if raises is not None:
                    raise raises
                return return_value
        return DEFAULT
