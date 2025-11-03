import unittest
import contribute
from subprocess import check_output


class TestContribute(unittest.TestCase):

    def test_arguments(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(args.no_weekends)
        self.assertEqual(args.max_commits, 10)
        self.assertTrue(1 <= contribute.contributions_per_day(args) <= 20)

    def test_contributions_per_day(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(1 <= contribute.contributions_per_day(args) <= 20)

    def test_commits(self):
        contribute.NUM = 11   # limiting the number only for unittesting
        contribute.main(['-nw',
                         '--user_name=sampleusername',
                         '--user_email=your-username@users.noreply.github.com',
                         '-mc=12',
                         '-fr=82',
                         '-db=10',
                         '-da=15'])
        self.assertTrue(1 <= int(check_output(
            ['git',
             'rev-list',
             '--count',
             'HEAD']
        ).decode('utf-8')) <= 20*(10 + 15))

    def test_get_first_sunday(self):
        from datetime import datetime
        self.assertEqual(contribute.get_first_sunday(2026), datetime(2026, 1, 4))
        self.assertEqual(contribute.get_first_sunday(2025), datetime(2025, 1, 5))

    def test_arguments_drawing(self):
        args = contribute.arguments(['--draw', '--year=2026', '--commits_per_pixel=5'])
        self.assertTrue(args.draw)
        self.assertEqual(args.year, 2026)
        self.assertEqual(args.commits_per_pixel, 5)

    def test_arguments_drawing_defaults(self):
        args = contribute.arguments(['--draw'])
        self.assertTrue(args.draw)
        self.assertEqual(args.year, 2025)
        self.assertEqual(args.commits_per_pixel, 25)

    def test_commits_drawing(self):
        import os
        orig_dir = os.getcwd()
        try:
            contribute.main(['--draw',
                             '--year=2026',
                             '--commits_per_pixel=2',
                             '--user_name=testdraw',
                             '--user_email=testdraw@example.com'])
            count = int(check_output(['git', 'rev-list', '--count', 'HEAD']).decode('utf-8').strip())
            # USMAN has 57 pixels. With 2 commits per pixel, we expect 57 * 2 = 114 commits.
            self.assertEqual(count, 114)
        finally:
            os.chdir(orig_dir)

