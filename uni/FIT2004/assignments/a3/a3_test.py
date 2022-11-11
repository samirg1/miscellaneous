import unittest
from assignment3 import compare_subs


class TestMethods(unittest.TestCase):

    def test_1(self):
        # Example 1
        submission1 = "the quick brown fox jumped over the lazy dog"
        submission2 = "my lazy dog has eaten my homework"
        self.assertEqual(compare_subs(submission1, submission2), [" lazy dog", 20, 27])

    def test_2(self):
        # Example 1
        submission1 = "radix sort and counting sort are both non comparison sorting algorithms"
        submission2 = "counting sort and radix sort are both non comparison sorting algorithms"
        self.assertEqual(compare_subs(submission1, submission2), [" sort are both non comparison sorting algorithms", 68, 68])

    def test_3(self):
        # Example 1
        submission1 = "safsa fs afs afs afs afsafsafiosafbanana asfophsafopsafopsafopsafpa"
        submission2 = "safsifaha asdoisaosans banana iosfqwpfwqpoanvsavm"
        self.assertEqual(compare_subs(submission1, submission2), ["banana ", 10, 14])

    def test_4(self):
        # Example 1
        submission1 = "banana"
        submission2 = "banana"
        self.assertEqual(compare_subs(submission1, submission2), ["banana", 100, 100])

    def test_5(self):
        # Example 1
        submission1 = "abcde"
        submission2 = "fghij"
        self.assertEqual(compare_subs(submission1, submission2), ["", 0, 0])

    def test_6(self):
        # Example 1
        submission1 = "abcdefghijklmnopqrstuvwxyzb"
        submission2 = "abcdefghijklmnopqrstuvwxyza"
        self.assertEqual(compare_subs(submission1, submission2), ["abcdefghijklmnopqrstuvwxyz", 96, 96])

    def test_7(self):
        # Example 1
        submission1 = "abcdefghijklmnopqrstuvwxyzb" * 200
        submission2 = "abcdefghijklmnopqrstuvwxyza" * 200
        self.assertEqual(compare_subs(submission1, submission2), ["abcdefghijklmnopqrstuvwxyz", 0, 0])

    def testQ2CatDog(self):
        testList = [("cat","dog",['',0,0]),
                     ("cat","catdog",["cat",100,50]),
                     ("catdog","dog",["dog",50,100]),
                     ("catdog","catdog",["catdog",100,100]),
                     ("catcatcatdogcatdogcat","catdogcatcat",["catdogcat",43,75]),
                     ("catcatdogdogcatdog","dogdogcatcatdogdogdogcatcatdog",["catcatdogdog",67,40]),
                     ("dogdogdogcatcatdogdogdogcatdog","catcatcatcatcatcat",["catcat",20,33])]
        for (str1,str2,output) in testList:
            with self.subTest(i=(str1,str2,output)):
                self.assertEqual(compare_subs(str1,str2),output) 
    def testQ2ABC(self):
        testList = [("abcbacbcbcba","bacacbcbcaba",["acbcbc",50,50]),
                    ("dcaaabdcaabbddcaaaaab","ecaeedcaabdedcaabbcd",["dcaabb",29,30]),
                    ("abcdef","fghijklm",["f",17,13]),
                    ("aabcdef","fedcbaa",["aa",29,29])]
        for (str1,str2,output) in testList:
            with self.subTest(i=(str1,str2,output)):
                self.assertEqual(compare_subs(str1,str2),output) 
    def testQ2EdgeCases(self):
        testList = [('','',['',0,0]),
                    ('','blue',['',0,0]),
                    ('red','',['',0,0]),
                    ('baroque','icy',['',0,0])]
        for (str1,str2,output) in testList:
            with self.subTest(i=(str1,str2,output)):
                self.assertEqual(compare_subs(str1,str2),output) 
    def testQ2E(self):
        testList = [("e","e",["e",100,100]),
                    ("eeeeeeee","e",["e",13,100]),
                    ("e","eeeeeeeeee",["e",100,10]),
                    ("eeeeeeeeeeeeeee","eeeee",["eeeee",33,100])]
        for (str1,str2,output) in testList:
            with self.subTest(i=(str1,str2,output)):
                self.assertEqual(compare_subs(str1,str2),output) 
    """
    Not sure about this test case
    def test_8(self): 
        # Example 1
        submission1 = ""
        submission2 = ""
        self.assertEqual(compare_subs(submission1, submission2), ["", 100, 100])
    """


if __name__ == '__main__':
    unittest.main()