from unittest import TestCase

from src import endpoint

class TestArgsVerfication(TestCase):
    def test_no_args(self):
        missing_or_wrong = endpoint.verify_args({})

        self.assertIn('letter', missing_or_wrong)
        self.assertIn('metar', missing_or_wrong)
        self.assertIn('rwy', missing_or_wrong)

    def test_no_letter(self):
        missing_or_wrong = endpoint.verify_args(
            {arg: None for arg in ['metar', 'rwy']}
        )

        self.assertIn('letter', missing_or_wrong)

    def test_no_metar(self):
        missing_or_wrong = endpoint.verify_args(
            {arg: None for arg in ['letter', 'rwy']}
        )

        self.assertIn('metar', missing_or_wrong)

    def test_no_rwy(self):
        missing_or_wrong = endpoint.verify_args(
            {arg: None for arg in ['metar', 'letter']}
        )

        self.assertIn('rwy', missing_or_wrong)

class TestArgParsing(TestCase):
    def test_parses_args(self):
        args = endpoint.parse_args({
            'letter': 'A',
            'metar': 'LPPT',
            'rwy': '03'
        })

        self.assertIn('letter', args)
        self.assertIn('metar', args)
        self.assertIn('rwy', args)
        self.assertEqual(args['letter'], 'A')
        self.assertEqual(args['metar'], 'LPPT')
        self.assertEqual(args['rwy'], '03')

    def test_parsing_returns_optionals(self):
        args = endpoint.parse_args({})
        
        # truthy options
        for arg in ['show_freqs']:
            self.assertIn(arg, args)
            self.assertEqual(args[arg], True, arg)

        # falsy options
        for arg in ['hiro', 'rwy_35_clsd', 'xpndr_startup']:
            self.assertIn(arg, args)
            self.assertEqual(args[arg], False, arg)