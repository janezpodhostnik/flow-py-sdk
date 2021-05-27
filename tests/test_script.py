from unittest import TestCase

from flow_py_sdk import Script, cadence, exceptions


class TestScript(TestCase):
    def test_init(self):
        with self.subTest(msg="With code"):
            code = "some code"
            s = Script(code=code)

            self.assertEqual(0, len(s.arguments))
            self.assertEqual(code, s.code)

        with self.subTest(msg="With arguments"):
            s = Script(code="some code", arguments=[cadence.Bool(True)])

            self.assertEqual(1, len(s.arguments))
            self.assertEqual(cadence.Bool(True), s.arguments[0])
            self.assertEqual(code, s.code)

    def test_add_arguments(self):
        with self.subTest(msg="No arguments"):
            s = Script(code="")
            s.add_arguments()

            self.assertEqual(0, len(s.arguments))

        with self.subTest(msg="One argument"):
            s = Script(code="")
            s.add_arguments(cadence.Bool(True))

            self.assertEqual(1, len(s.arguments))
            self.assertEqual(cadence.Bool(True), s.arguments[0])

        with self.subTest(msg="One argument + one argument"):
            s = Script(code="")
            s.add_arguments(cadence.Bool(True))
            s.add_arguments(cadence.String("42"))

            self.assertEqual(2, len(s.arguments))
            self.assertEqual(cadence.Bool(True), s.arguments[0])
            self.assertEqual(cadence.String("42"), s.arguments[1])

        with self.subTest(msg="Multiple arguments"):
            s = Script(code="")
            s.add_arguments(cadence.Bool(True), cadence.String("42"))

            self.assertEqual(2, len(s.arguments))
            self.assertEqual(cadence.Bool(True), s.arguments[0])
            self.assertEqual(cadence.String("42"), s.arguments[1])

        with self.subTest(msg="None Argument; should fail"):
            s = Script(code="")

            with self.assertRaises(exceptions.NotCadenceValueError):
                # noinspection PyTypeChecker
                s.add_arguments(None)

        with self.subTest(msg="Non-cadence Argument; should fail"):
            s = Script(code="")

            with self.assertRaises(exceptions.NotCadenceValueError):
                # noinspection PyTypeChecker
                s.add_arguments("42")
