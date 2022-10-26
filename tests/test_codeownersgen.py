import unittest

from codeowners_backstage.codeowners_file import preprocess_codeowners_inlining_group_members


class CodeOwnersGenerationTestCase(unittest.TestCase):
    def test_should_substitute_group_name_with_members(self):
        # given
        template = """
        file.md @my-team
        """

        def get_team_members(name):
            assert name == "my-team"
            return ['adam@example.com', 'monika@example.com']

        # when
        actual = preprocess_codeowners_inlining_group_members(template, get_team_members)

        # then
        expected = """
        file.md adam@example.com monika@example.com
        """
        self.assertEqual(actual, expected)

    def test_should_not_touch_emails_in_the_template(self):
        # given
        template = """
        file.md adam@example.com
        """

        def get_team_members(name):
            raise AssertionError("should not be called!")

        # when
        actual = preprocess_codeowners_inlining_group_members(template, get_team_members)

        # then
        expected = """
        file.md adam@example.com
        """
        self.assertEqual(actual, expected)

    def test_should_leave_group_names_as_is_if_they_are_not_found(self):
        # given
        template = """
        file.md @my-team
        """

        def get_team_members(name):
            assert name == "my-team"
            return None  # not found

        # when
        actual = preprocess_codeowners_inlining_group_members(template, get_team_members)

        # then
        expected = """
        file.md @my-team
        """
        self.assertEqual(actual, expected)


