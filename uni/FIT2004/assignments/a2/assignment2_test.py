# assignment2_test.py
# Date: 13-09-2022
# Author: Samir Gupta
from unittest import main as unittest_main, TestCase
from assignment2 import RoadGraph, optimalRoute

class TestRoadGraphExample(TestCase):
    roads = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2), (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2), (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
    cafes =  [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
    mygraph = RoadGraph(roads, cafes)
    
    def test1_0(self):
        self.assertEqual(self.mygraph.routing(1, 0), [1, 7, 8, 0])
    def test1_1(self):
        self.assertEqual(self.mygraph.routing(1, 1), [1, 7, 8, 0, 1])
    def test1_2(self):
        self.assertEqual(self.mygraph.routing(1, 2), [1, 7, 8, 0, 1, 2])
    def test1_3(self):
        self.assertEqual(self.mygraph.routing(1, 3), [1, 5, 6, 3])
    def test1_4(self):
        val = self.mygraph.routing(1, 4)
        self.assertTrue(val == [1, 5, 6, 4] or val == [1, 5, 6, 3, 4])
    def test1_5(self):
        self.assertEqual(self.mygraph.routing(1, 5), [1, 5])
    def test1_6(self):
        self.assertEqual(self.mygraph.routing(1, 6), [1, 5, 6])
    def test1_7(self):
        self.assertEqual(self.mygraph.routing(1, 7), [1, 7])
    def test1_8(self):
        self.assertEqual(self.mygraph.routing(1, 8), [1, 7, 8])
        
    def test3_0(self):
        self.assertEqual(self.mygraph.routing(3, 0), [3, 4, 8, 0])
    def test3_1(self):
        self.assertEqual(self.mygraph.routing(3, 1), [3, 4, 8, 0, 1])
    def test3_2(self):
        self.assertEqual(self.mygraph.routing(3, 2), [3, 4, 8, 0, 1, 2])
    def test3_3(self):
        self.assertEqual(self.mygraph.routing(3, 3), [3, 4, 8, 7, 3])
    def test3_4(self):
        self.assertEqual(self.mygraph.routing(3, 4), [3, 4, 8, 7, 3, 4])
    def test3_5(self):
        self.assertEqual(self.mygraph.routing(3, 5), [3, 4, 8, 0, 1, 5])
    def test3_6(self):
        self.assertEqual(self.mygraph.routing(3, 6), [3, 4, 8, 0, 1, 5, 6])
    def test3_7(self):
        self.assertEqual(self.mygraph.routing(3, 7), [3, 4, 8, 7])
    def test3_8(self):
        self.assertEqual(self.mygraph.routing(3, 8), [3, 4, 8])

class TestRoadGraphSmallLoop(TestCase):
    roads = [(0, 1, 3), (1, 2, 2), (2, 1, 2)]
    cafes = [(2, 3)]
    roadGraph = RoadGraph(roads, cafes)
    
    def test0_0(self):
        self.assertIsNone(self.roadGraph.routing(0, 0))
    def test0_1(self):
        self.assertEqual(self.roadGraph.routing(0, 1), [0, 1, 2, 1])
    def test0_2(self):
        self.assertEqual(self.roadGraph.routing(0, 2), [0, 1, 2])
    def test1_0(self):
        self.assertIsNone(self.roadGraph.routing(1, 0))
    def test1_1(self):
        self.assertEqual(self.roadGraph.routing(1, 1), [1, 2, 1])
    def test1_2(self):
        self.assertEqual(self.roadGraph.routing(1, 2), [1, 2])
    def test2_0(self):
        self.assertIsNone(self.roadGraph.routing(2, 0))
    def test2_1(self):
        self.assertEqual(self.roadGraph.routing(2, 1), [2, 1])
    def test2_2(self):
        self.assertEqual(self.roadGraph.routing(2, 2), [2])
        
class TestRoadGraphNoCafes(TestCase):
    roads = [(0, 1, 3), (1, 2, 2), (2, 1, 2)]
    roadGraph = RoadGraph(roads, [])
    
    def testAll(self):
        for i in range(0, 3):
            for j in range(0, 3):
                with self.subTest(i=i, j=j):
                    self.assertIsNone(self.roadGraph.routing(i, j))
    
    
        
class TestOptimalRouteExample(TestCase):
    downhillScores = [(0, 6, -500), (1, 4, 100), (1, 2, 300), (6, 3, -100), (6, 1, 200), (3, 4, 400), (3, 1, 400), (5, 6, 700), (5, 1, 1000), (4, 2, 100)]
    
    def test1_0(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 1, 0))
    def test1_1(self):
        self.assertEqual(optimalRoute(self.downhillScores, 1, 1), [1])
    def test1_2(self):
        self.assertEqual(optimalRoute(self.downhillScores, 1, 2), [1, 2])
    def test1_3(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 1, 3))
    def test1_4(self):
        self.assertEqual(optimalRoute(self.downhillScores, 1, 4), [1, 4])
    def test1_5(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 1, 5))
    def test1_6(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 1, 6))
        
    def test2(self):
        for i in range(7):
            with self.subTest(f'2_{i}', i=i):
                val = optimalRoute(self.downhillScores, 2, i)
                if i == 2:
                    self.assertEqual(val, [2])
                else:
                    self.assertIsNone(val)
        
    def test3_0(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 3, 0))
    def test3_1(self):
        self.assertEqual(optimalRoute(self.downhillScores, 3, 1), [3, 1])
    def test3_2(self):
        self.assertEqual(optimalRoute(self.downhillScores, 3, 2), [3, 1, 2])
    def test3_3(self):
        self.assertEqual(optimalRoute(self.downhillScores, 3, 3), [3])
    def test3_4(self):
        self.assertEqual(optimalRoute(self.downhillScores, 3, 4), [3, 1, 4])
    def test3_5(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 3, 5))
    def test3_6(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 3, 6))
    
    def test4_0(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 4, 0))
    def test4_1(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 4, 1))
    def test4_2(self):
        self.assertEqual(optimalRoute(self.downhillScores, 4, 2), [4, 2])
    def test4_3(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 4, 3))
    def test4_4(self):
        self.assertEqual(optimalRoute(self.downhillScores, 4, 4), [4])
    def test4_5(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 4, 5))
    def test4_6(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 4, 6))
        
    def test5_0(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 5, 0))
    def test5_1(self):
        val = optimalRoute(self.downhillScores, 5, 1)
        self.assertTrue(val == [5, 1] or val == [5, 6, 3, 1], val)
    def test5_2(self):
        val = optimalRoute(self.downhillScores, 5, 2)
        self.assertTrue(val == [5, 1, 2] or val == [5, 6, 3, 1, 2], val)
    def test5_3(self):
        self.assertEqual(optimalRoute(self.downhillScores, 5, 3), [5, 6, 3])
    def test5_4(self):
        val = optimalRoute(self.downhillScores, 5, 4)
        self.assertTrue(val == [5, 1, 4] or val == [5, 6, 3, 1, 4], val)
    def test5_5(self):
        self.assertEqual(optimalRoute(self.downhillScores, 5, 5), [5])
    def test5_6(self):
        self.assertEqual(optimalRoute(self.downhillScores, 5, 6), [5, 6])
    
    def test6_0(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 6, 0))
    def test6_1(self):
        self.assertEqual(optimalRoute(self.downhillScores, 6, 1), [6, 3, 1])
    def test6_2(self):
        self.assertEqual(optimalRoute(self.downhillScores, 6, 2), [6, 3, 1, 2])
    def test6_3(self):
        self.assertEqual(optimalRoute(self.downhillScores, 6, 3), [6, 3])
    def test6_4(self):
        self.assertEqual(optimalRoute(self.downhillScores, 6, 4), [6, 3, 1, 4])
    def test6_5(self):
        self.assertIsNone(optimalRoute(self.downhillScores, 6, 5))
    def test6_6(self):
        self.assertEqual(optimalRoute(self.downhillScores, 6, 6), [6])
        
class TestOptimalRoute1Child(TestCase):
    downhill_routes = [(1, 0, 100), (2, 0, 200), (3, 0, 300), (4, 0, 400), (5, 0, 500), (6, 0, 600)]
    def test0(self):
        for i in range(7):
            with self.subTest(i=i):
                val = optimalRoute(self.downhill_routes, 0, i)
                if i == 0:
                    self.assertEqual(val, [0])
                else:
                    self.assertIsNone(val)
    def testNones(self):
        for i in range(1, 7):
            for j in range(1, 7):
                with self.subTest(i=i, j=j):
                    val = optimalRoute(self.downhill_routes, i, j)
                    if i == j:
                        self.assertEqual(val, [i])
                    else:
                        self.assertIsNone(val)
    def testRoutes(self):
        for i in range(1, 7):
            with self.subTest(i=i):
                self.assertEqual(optimalRoute(self.downhill_routes, i, 0), [i, 0])
                
                
def main(): unittest_main(verbosity=0)    
if __name__ == '__main__': main()