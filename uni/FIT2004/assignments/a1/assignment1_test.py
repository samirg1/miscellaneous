from assignment1 import analyze, unique_sorted_list, get_top_results, find_matches
from unittest import TestCase

class TestUniqueSorted(TestCase):
    def test_general(self):
        self.assertEqual(unique_sorted_list([1, 1, 1, 2, 2, 3, 4, 4, 4, 4, 5, 6, 7, 7, 7, 8, 9, 9]), [1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_objects(self):
        self.assertEqual(unique_sorted_list([[1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3]]), [[1, 2], [1, 3]])
    def test_more_objects(self):
         self.assertEqual(unique_sorted_list([[1, 'a'], [1, 'b'], [1, 'b'], [2, 'a'], [2, 'a'], [2, 'b'], [3, 'a']]),  [[1, 'a'], [1, 'b'], [2, 'a'], [2, 'b'], [3, 'a']])
    
class TestTopResults(TestCase):
    def test_general(self):
        res = get_top_results([9, 8, 7, 6, 5], 3)
        self.assertEqual(res, [9, 8, 7])
    def test_change(self):
        res = get_top_results([9, 8, 7, 6, 6, 6, 6, 5], 5, 3)
        self.assertEqual(res, [9, 8, 7])
    def test_duplicates(self):
        res = get_top_results([9, 8, 7, 6, 6, 6, 6, 5], 5)
        self.assertEqual(res, [9, 8, 7, 6, 6])
    def test_objects(self):
        res = get_top_results([[9, 9], [9, 8], [9, 7], [8, 6], [8, 5]], 3, 0, 5)
        self.assertEqual(res, [[9, 9], [9, 8], [9, 7]])

class TestFindMatches(TestCase):
    def test_general(self):
        self.assertEqual(find_matches([5, 4, 3, 2, 1], 3) ,[3])
    def test_duplicate(self):
        self.assertEqual(find_matches([5, 4, 3, 3, 2, 1], 3),[3, 3])
    def test_no_direct_match(self):
        self.assertEqual(find_matches([5, 4, 4, 2, 1, 1], 3),[4, 4])
    def test_objects(self):
        self.assertEqual(find_matches([[2, 3], [2, 3], [2, 2], [3, 2], [1, 1]], 2, lambda a: a[1]),[[2, 2], [3, 2]])

class TestAnalyze(TestCase):
    GEN_RESULTS = [['AAB', 'AAB', 35], ['AAB', 'BBA', 49], ['BAB', 'BAB', 42], ['AAA', 'AAA', 38], ['BAB', 'BAB', 36], ['BAB', 'BAB', 36], ['ABA', 'BBA', 57], ['BBB', 'BBA', 32], ['BBA', 'BBB', 49], ['BBA', 'ABB', 55], ['AAB', 'AAA', 58], ['ABA', 'AAA', 46], ['ABA', 'ABB', 44], ['BBB', 'BAB', 32], ['AAA', 'AAB', 36], ['ABA', 'BBB', 48], ['BBB', 'ABA', 33], ['AAB', 'BBA', 30], ['ABB', 'BBB', 68], ['BAB', 'BBB', 52]]
    ALL_SAME_RES = [['BCB', 'CAB', 55], ['ACB', 'CAB', 55], ['ACB', 'BBA', 55], ['AAA', 'ACA', 55], ['CAB', 'BAB', 55]]
    BIGGER_RES = [['DABCFA', 'DFCAEB', 90]]
    BIGGER_EQUAL_RES = [['DABCFA', 'DECAEB', 90], ['CFDAEB', 'DACABF', 10]]
    FIFTY_100_RES = [['BAC', 'AAB', 50], ['AAA', 'BAB', 50], ['ABB', 'ACA', 50], ['CAC', 'ABC', 0], ['ACA', 'BBA', 100], ['ABB', 'AAB', 50]]

    def test_general1(self):
        self.assertEqual(analyze(self.GEN_RESULTS, 2, 64), [[['ABB', 'AAB', 70], ['ABB', 'BBB', 68], ['AAB', 'BBB', 67], ['AAB', 'AAB', 65], ['AAB', 'AAA', 64], ['ABB', 'ABB', 64], ['AAA', 'AAA', 62], ['AAB', 'AAA', 58], ['ABB', 'ABB', 58], ['AAB', 'ABB', 57]], [['AAB', 'AAA', 64], ['ABB', 'ABB', 64]]])      
    def test_general2(self):    
        self.assertEqual(analyze(self.GEN_RESULTS, 2, 63), [[['ABB', 'AAB', 70], ['ABB', 'BBB', 68], ['AAB', 'BBB', 67], ['AAB', 'AAB', 65], ['AAB', 'AAA', 64], ['ABB', 'ABB', 64], ['AAA', 'AAA', 62], ['AAB', 'AAA', 58], ['ABB', 'ABB', 58], ['AAB', 'ABB', 57]], [['AAB', 'AAA', 64], ['ABB', 'ABB', 64]]]) 
    def test_general3(self):    
        self.assertEqual(analyze(self.GEN_RESULTS, 2, 71),  [[['ABB', 'AAB', 70], ['ABB', 'BBB', 68], ['AAB', 'BBB', 67], ['AAB', 'AAB', 65], ['AAB', 'AAA', 64], ['ABB', 'ABB', 64], ['AAA', 'AAA', 62], ['AAB', 'AAA', 58], ['ABB', 'ABB', 58], ['AAB', 'ABB', 57]], []])
    def test_general4(self):    
        self.assertEqual(analyze(self.GEN_RESULTS, 2, 0), [[['ABB', 'AAB', 70], ['ABB', 'BBB', 68], ['AAB', 'BBB', 67], ['AAB', 'AAB', 65], ['AAB', 'AAA', 64], ['ABB', 'ABB', 64], ['AAA', 'AAA', 62], ['AAB', 'AAA', 58], ['ABB', 'ABB', 58], ['AAB', 'ABB', 57]], [['AAB', 'ABB', 30]]]) 
    
    def test_all_same1(self):
        self.assertEqual(analyze(self.ALL_SAME_RES, 3, 60), [[['AAA', 'AAC', 55], ['ABC', 'ABB', 55], ['ABC', 'ABC', 55], ['BBC', 'ABC', 55], ['AAC', 'AAA', 45], ['ABB', 'ABC', 45], ['ABC', 'ABC', 45], ['ABC', 'BBC', 45]], []])
    def test_all_same2(self):    
        self.assertEqual(analyze(self.ALL_SAME_RES, 3, 46), [[['AAA', 'AAC', 55], ['ABC', 'ABB', 55], ['ABC', 'ABC', 55], ['BBC', 'ABC', 55], ['AAC', 'AAA', 45], ['ABB', 'ABC', 45], ['ABC', 'ABC', 45], ['ABC', 'BBC', 45]], [['AAA', 'AAC', 55], ['ABC', 'ABB', 55], ['ABC', 'ABC', 55], ['BBC', 'ABC', 55]]])
    def test_all_same3(self):    
        self.assertEqual(analyze(self.ALL_SAME_RES, 3, 10), [[['AAA', 'AAC', 55], ['ABC', 'ABB', 55], ['ABC', 'ABC', 55], ['BBC', 'ABC', 55], ['AAC', 'AAA', 45], ['ABB', 'ABC', 45], ['ABC', 'ABC', 45], ['ABC', 'BBC', 45]], [['AAC', 'AAA', 45], ['ABB', 'ABC', 45], ['ABC', 'ABC', 45], ['ABC', 'BBC', 45]]])        
    
    def test_bigger_roster1(self):
        self.assertEqual(analyze(self.BIGGER_RES, 6, 10), [[['AABCDF', 'ABCDEF', 90], ['ABCDEF', 'AABCDF', 10]], [['ABCDEF', 'AABCDF', 10]]])        
    def test_bigger_roster2(self):    
        self.assertEqual(analyze(self.BIGGER_RES, 6, 11), [[['AABCDF', 'ABCDEF', 90], ['ABCDEF', 'AABCDF', 10]], [['AABCDF', 'ABCDEF', 90]]])
    def test_bigger_roster3(self):    
        self.assertEqual(analyze(self.BIGGER_RES, 6, 91),  [[['AABCDF', 'ABCDEF', 90], ['ABCDEF', 'AABCDF', 10]], []])

    def test_bigger_equal_on_swap1(self):
        self.assertEqual(analyze(self.BIGGER_EQUAL_RES, 6, 10), [[['AABCDF', 'ABCDEE', 90], ['AABCDF', 'ABCDEF', 90], ['ABCDEE', 'AABCDF', 10], ['ABCDEF', 'AABCDF', 10]], [['ABCDEE', 'AABCDF', 10], ['ABCDEF', 'AABCDF', 10]]])
    def test_bigger_equal_on_swap2(self):    
        self.assertEqual(analyze(self.BIGGER_EQUAL_RES, 6, 40), [[['AABCDF', 'ABCDEE', 90], ['AABCDF', 'ABCDEF', 90], ['ABCDEE', 'AABCDF', 10], ['ABCDEF', 'AABCDF', 10]], [['AABCDF', 'ABCDEE', 90], ['AABCDF', 'ABCDEF', 90]]])
    def test_bigger_equal_on_swap3(self):    
        self.assertEqual(analyze(self.BIGGER_EQUAL_RES, 6, 91), [[['AABCDF', 'ABCDEE', 90], ['AABCDF', 'ABCDEF', 90], ['ABCDEE', 'AABCDF', 10], ['ABCDEF', 'AABCDF', 10]], []])

    def test_50s_100s1(self):
        self.assertEqual(analyze(self.FIFTY_100_RES, 3, 100), [[['AAC', 'ABB', 100], ['ABC', 'ACC', 100], ['AAA', 'ABB', 50], ['AAB', 'ABB', 50], ['AAB', 'ABC', 50], ['AAC', 'ABB', 50], ['ABB', 'AAA', 50], ['ABB', 'AAB', 50], ['ABB', 'AAC', 50], ['ABC', 'AAB', 50]], [['AAC', 'ABB', 100], ['ABC', 'ACC', 100]]])
    def test_50s_100s2(self):    
        self.assertEqual(analyze(self.FIFTY_100_RES, 3, 0), [[['AAC', 'ABB', 100], ['ABC', 'ACC', 100], ['AAA', 'ABB', 50], ['AAB', 'ABB', 50], ['AAB', 'ABC', 50], ['AAC', 'ABB', 50], ['ABB', 'AAA', 50], ['ABB', 'AAB', 50], ['ABB', 'AAC', 50], ['ABC', 'AAB', 50]], [['ABB', 'AAC', 0], ['ACC', 'ABC', 0]]])
    def test_50s_100s3(self):    
        self.assertEqual(analyze(self.FIFTY_100_RES, 3, 1), [[['AAC', 'ABB', 100], ['ABC', 'ACC', 100], ['AAA', 'ABB', 50], ['AAB', 'ABB', 50], ['AAB', 'ABC', 50], ['AAC', 'ABB', 50], ['ABB', 'AAA', 50], ['ABB', 'AAB', 50], ['ABB', 'AAC', 50], ['ABC', 'AAB', 50]], [['AAA', 'ABB', 50], ['AAB', 'ABB', 50], ['AAB', 'ABC', 50], ['AAC', 'ABB', 50], ['ABB', 'AAA', 50], ['ABB', 'AAB', 50], ['ABB', 'AAC', 50], ['ABC', 'AAB', 50]]])
class TestMethods(TestCase):
    # a roster of 2 characters
    roster = 2
    # results with 20 matches
    results = [
        ['AAB', 'AAB', 35], ['AAB', 'BBA', 49], ['BAB', 'BAB', 42],
        ['AAA', 'AAA', 38], ['BAB', 'BAB', 36], ['BAB', 'BAB', 36],
        ['ABA', 'BBA', 57], ['BBB', 'BBA', 32], ['BBA', 'BBB', 49],
        ['BBA', 'ABB', 55], ['AAB', 'AAA', 58], ['ABA', 'AAA', 46],
        ['ABA', 'ABB', 44], ['BBB', 'BAB', 32], ['AAA', 'AAB', 36],
        ['ABA', 'BBB', 48], ['BBB', 'ABA', 33], ['AAB', 'BBA', 30],
        ['ABB', 'BBB', 68], ['BAB', 'BBB', 52]
    ]

    def test_1(self):
        # looking for a score of 64
        score = 64

        result = [
            [['ABB', 'AAB', 70],
             ['ABB', 'BBB', 68],
             ['AAB', 'BBB', 67],
             ['AAB', 'AAB', 65],
             ['AAB', 'AAA', 64],
             ['ABB', 'ABB', 64],
             ['AAA', 'AAA', 62],
             ['AAB', 'AAA', 58],
             ['ABB', 'ABB', 58],
             ['AAB', 'ABB', 57]],
            [['AAB', 'AAA', 64], ['ABB', 'ABB', 64]]
        ]
        self.assertEqual(analyze(self.results, self.roster, score), result)

    def test_2(self):
        # looking for a score of 63
        score = 63

        result = [
            [['ABB', 'AAB', 70],
             ['ABB', 'BBB', 68],
             ['AAB', 'BBB', 67],
             ['AAB', 'AAB', 65],
             ['AAB', 'AAA', 64],
             ['ABB', 'ABB', 64],
             ['AAA', 'AAA', 62],
             ['AAB', 'AAA', 58],
             ['ABB', 'ABB', 58],
             ['AAB', 'ABB', 57]],
            [['AAB', 'AAA', 64], ['ABB', 'ABB', 64]]
        ]

        self.assertEqual(analyze(self.results, self.roster, score), result)

    def test_3(self):
        # looking for a score of 71
        score = 71

        result = [
            [['ABB', 'AAB', 70],
             ['ABB', 'BBB', 68],
             ['AAB', 'BBB', 67],
             ['AAB', 'AAB', 65],
             ['AAB', 'AAA', 64],
             ['ABB', 'ABB', 64],
             ['AAA', 'AAA', 62],
             ['AAB', 'AAA', 58],
             ['ABB', 'ABB', 58],
             ['AAB', 'ABB', 57]],
            []
        ]

        self.assertEqual(analyze(self.results, self.roster, score), result)

    def test_4(self):
        # looking for a score of 0
        score = 0

        result = [
            [['ABB', 'AAB', 70],
             ['ABB', 'BBB', 68],
             ['AAB', 'BBB', 67],
             ['AAB', 'AAB', 65],
             ['AAB', 'AAA', 64],
             ['ABB', 'ABB', 64],
             ['AAA', 'AAA', 62],
             ['AAB', 'AAA', 58],
             ['ABB', 'ABB', 58],
             ['AAB', 'ABB', 57]],
            [['AAB', 'ABB', 30]]
        ]

        self.assertEqual(analyze(self.results, self.roster, score), result)

    def test_5(self):
        results = [
            ['ABC', 'ADE', 30],
            ['AAC', 'ACE', 30],
            ['AAC', 'AAE', 30]
        ]

        result = [
            [['AAE', 'AAC', 70],
             ['ACE', 'AAC', 70],
             ['ADE', 'ABC', 70],
             ['AAC', 'AAE', 30],
             ['AAC', 'ACE', 30],
             ['ABC', 'ADE', 30]],
            [['AAE', 'AAC', 70], ['ACE', 'AAC', 70], ['ADE', 'ABC', 70]]
        ]

        self.assertEqual(analyze(results, 5, 40), result)

    def test_6(self):
        results = [
            ['AB', 'BB', 30],
            ['BA', 'AA', 30]
        ]

        result = [
            [['AA', 'AB', 70],
             ['BB', 'AB', 70],
             ['AB', 'AA', 30],
             ['AB', 'BB', 30]],
            [['AA', 'AB', 70], ['BB', 'AB', 70]]
        ]

        self.assertEqual(analyze(results, 2, 40), result)

    def test_7(self):
        results = [
            ['A', 'B', 30],
            ['C', 'A', 40]
        ]

        result = [
            [['B', 'A', 70],
             ['A', 'C', 60],
             ['C', 'A', 40],
             ['A', 'B', 30]],
            [['B', 'A', 70]]
        ]

        self.assertEqual(analyze(results, 3, 70), result)

    def test_8(self):
        results = [
            ['A', 'A', 30],
            ['A', 'A', 70],
            ['A', 'A', 40]
        ]

        result = [
            [['A', 'A', 70],
             ['A', 'A', 60],
             ['A', 'A', 40],
             ['A', 'A', 30]],
            [['A', 'A', 70]]
        ]

        self.assertEqual(analyze(results, 1, 70), result)

    def test_9(self):
        results = [
            ['A', 'B', 50],
        ]

        result = [
            [['A', 'B', 50],
             ['B', 'A', 50]],
            []
        ]

        self.assertEqual(analyze(results, 2, 70), result)

    def test_10(self):
        results = [
            ['A', 'A', 50],
        ]

        result = [
            [['A', 'A', 50]],
            [['A', 'A', 50]]
        ]

        self.assertEqual(analyze(results, 1, 50), result)

    def test_11(self):
        results = [
            ['A', 'B', 50],
        ]

        result = [
            [['A', 'B', 50],
             ['B', 'A', 50]],
            [['A', 'B', 50], ['B', 'A', 50]]
        ]

        self.assertEqual(analyze(results, 2, 50), result)

    def test_12(self):
        results = [
            ['A', 'B', 100],
        ]

        result = [
            [['A', 'B', 100],
             ['B', 'A', 0]],
            [['A', 'B', 100]]
        ]

        self.assertEqual(analyze(results, 2, 50), result)

    def test_13(self):
        results = [
            ['A', 'B', 100],
        ]

        result = [
            [['A', 'B', 100],
             ['B', 'A', 0]],
            [['B', 'A', 0]]
        ]

        self.assertEqual(analyze(results, 2, 0), result)

    def test_14(self):
        results = [
            ['A', 'A', 100],
        ]

        result = [
            [['A', 'A', 100],
             ['A', 'A', 0]],
            [['A', 'A', 0]]
        ]

        self.assertEqual(analyze(results, 1, 0), result)

    def test_15(self):
        results = [
            ['A', 'A', 100],
        ]

        result = [
            [['A', 'A', 100],
             ['A', 'A', 0]],
            [['A', 'A', 100]]
        ]

        self.assertEqual(analyze(results, 1, 1), result)

    def test_16(self):
        results = [
            ['AACDEFGHIJKLMNOPQRSTUVWXYZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 35],
            ['ABCDEFGHIJKLMNOPQRSTUVWXYZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 35]
        ]

        result = [
            [['ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 'AACDEFGHIJKLMNOPQRSTUVWXYZZ', 65],
             ['ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZZ', 65],
             ['AACDEFGHIJKLMNOPQRSTUVWXYZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 35],
             ['ABCDEFGHIJKLMNOPQRSTUVWXYZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 35]],
            [['ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 'AACDEFGHIJKLMNOPQRSTUVWXYZZ', 65],
             ['ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZZ', 65]]
        ]

        self.assertEqual(analyze(results, 26, 65), result)