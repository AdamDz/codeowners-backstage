import unittest
import json
from os.path import dirname, join

from codeowners_backstage.backstage_user_groups import BackstageUserGroups


class BackstageUserGroupsTestCase(unittest.TestCase):
    def test_return_leaf_group_members(self):
        # given
        with open(join(dirname(__file__), 'data', 'backstage-group-and-users.json')) as f:
            response_json = json.load(f)

        # when
        backstage_user_groups = BackstageUserGroups(response_json)
        actual = backstage_user_groups.get_group_members('a-team')

        # then
        expected = ['john.doe@example.com']
        self.assertEqual(expected, actual)

    def test_return_none_if_group_not_found(self):
        # given
        with open(join(dirname(__file__), 'data', 'backstage-group-and-users.json')) as f:
            response_json = json.load(f)

        # when
        backstage_user_groups = BackstageUserGroups(response_json)
        actual = backstage_user_groups.get_group_members('b-team')

        # then
        self.assertEqual(None, actual)

    def test_return_parent_group_members_including_leaf_group_members(self):
        # given
        with open(join(dirname(__file__), 'data', 'backstage-group-and-users.json')) as f:
            response_json = json.load(f)

        # when
        backstage_user_groups = BackstageUserGroups(response_json)
        actual = backstage_user_groups.get_group_members('parent-team')

        # then
        expected = ['d.rector@example.com', 'john.doe@example.com']
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
