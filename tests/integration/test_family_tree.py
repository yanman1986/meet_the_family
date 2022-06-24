from unittest import TestCase

from family_tree.family_tree import FamilyTree
from family_tree.member import Member, Gender


class TestFamilyTree(TestCase):

    def setUp(self):
        self.ftree = FamilyTree()

    def test_add_child(self):
        result = self.ftree.add_child("Father", "Male")
        self.assertEqual(result, "CHILD_ADDITION_SUCCEDED")
        self.assertEqual(self.ftree.family_tree.get("Father", None) is not None, True)

        self.assertEqual(self.ftree.add_child("Zim", "Male", "Mother"), "PERSON_NOT_FOUND")
        self.assertEqual(self.ftree.add_child("Zim", "Male", "Father"), "CHILD_ADDITION_FAILED")

        mother = Member(2, "Mother", "Female")
        mother.spouse = self.ftree.family_tree["Father"]
        self.ftree.family_tree["Father"].set_spouse(mother)
        self.ftree.family_tree["Mother"] = mother

        self.assertEqual(self.ftree.add_child("Zim", "Male", "Mother"), "CHILD_ADDITION_SUCCEDED")
        self.assertEqual(self.ftree.add_child("Zim", "Male", "Mother"), "CHILD_ADDITION_FAILED")
        self.assertEqual(self.ftree.family_tree.get("Zim", None) is not None, True)

    def test_add_spouse(self):
        self.assertEqual(self.ftree.add_spouse("Wife", "Female", "Zim"), "SPOUSE_ADDITION_FAILED")
        dummy_member = Member(1, "DummyMember", "Male")
        self.ftree.family_tree['DummyMember'] = dummy_member
        self.assertEqual(self.ftree.add_spouse("Wife", "Female", "Zim"), "PERSON_NOT_FOUND")
        spouse_a = Member(1, "FakeMember", "Female")
        spouse_b = Member(2, "AlreadyMarriedMember", "Male")
        spouse_b.set_spouse(spouse_a)
        spouse_c = Member(1, "Zim", "Male")
        self.ftree.family_tree["FakeMember"] = spouse_a
        self.ftree.family_tree["AlreadyMarriedMember"] = spouse_b
        self.ftree.family_tree["Zim"] = spouse_c
        self.assertEqual(self.ftree.add_spouse("Wife", "Female", "FakeMember"), "SPOUSE_ADDITION_FAILED")
        self.assertEqual(self.ftree.add_spouse("Wife", "Female", "AlreadyMarriedMember"), "SPOUSE_ADDITION_FAILED")
        self.assertEqual(self.ftree.add_spouse("Wife", "Female", "Zim"), "SPOUSE_ADDITION_SUCCEDED")
        self.assertEqual(self.ftree.add_spouse("Wife", "Female", "Zim"), "SPOUSE_ADDITION_FAILED")

    def test_get_relationship(self):
        self.assertEqual(self.ftree.get_relationship("Zim", "brother_in_law"), "PERSON_NOT_FOUND")
        member = Member(1, "Zim", "Male")
        son_a = Member(2, "SonA", "Male")
        son_b = Member(3, "SonB", "Male")
        member.add_child(son_a)
        member.add_child(son_b)
        son_a.set_father(member)
        son_b.set_father(member)
        self.ftree.family_tree["Zim"] = member
        self.ftree.family_tree["SonA"] = son_a
        self.ftree.family_tree["SonB"] = son_b
        self.assertEqual(self.ftree.get_relationship("Zim", "daughter"), "NONE")
        self.assertEqual(self.ftree.get_relationship("Zim", "son"), ["SonA", "SonB"])

