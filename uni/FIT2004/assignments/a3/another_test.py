# type: ignore

import unittest
from assignment3 import allocate
import math

def validate(results,availability,cannotBeNone=False):
    if(results==None and cannotBeNone):
        raise Exception("results should not be None when parameter cannotBeNone=True")
    if(results==None or results == ([],[])):
        return 
    breakfast = results[0]
    dinner = results[1]
    dayCount = len(availability)
    if(len(dinner)!=len(breakfast)):
        raise Exception("breakfast and dinner lists not the same length")
    if(len(dinner)!=dayCount):
        raise Exception("breakfast and dinner should have the same number of days as availability")
    mealCount = [0] * 6
    for i in range(dayCount):
        b = breakfast[i]
        d = dinner[i]
        if(not b in [0,1,2,3,4,5]):
            raise Exception("invalid value of breakfast at day %s: %s" % (i,b))
        if(not d in [0,1,2,3,4,5]):
            raise Exception("invalid value of dinner at day %s: %s" % (i,d))
        if(b==d and b!=5):
            raise Exception("day %s: breakfast and dinner can't be prepared by the same person (%s)" % (i,b))
        mealCount[b] += 1
        mealCount[d] += 1
    totalMeals = dayCount*2
    if(sum(mealCount)!=totalMeals):
        raise Exception("incorrect total number of meals (%s instead of %s)" % (sum(mealCount),totalMeals))
    minMeals = math.floor(0.36 * dayCount)
    maxMeals = math.ceil(0.44 * dayCount)
    for i in range(5):
        meals = mealCount[i]
        if(meals < minMeals or meals > maxMeals):
            raise Exception("invalid number of meals for housemate %s: %s (must be between %s and %s inclusive)" % (i,meals,minMeals,maxMeals))
    meals = mealCount[-1]
    maxMealsResto = math.floor(0.1 * dayCount)
    if(meals > maxMealsResto):
        raise Exception("too many restaurant meals: %s (must be less than or equal to %s)" % (meals,maxMealsResto))
def genRandominput():
    days = random.randint(0,10)
    availability = []
    for i in range(days):
        availability.append([random.randint(0,3) for i in range(5)])
    return availability

class Tests(unittest.TestCase):
    def testQ1ProvidedCase(self):
        availability = [[2, 0, 2, 1, 2], [3, 3, 1, 0, 0],
            [0, 1, 0, 3, 0], [0, 0, 2, 0, 3],
            [1, 0, 0, 2, 1], [0, 0, 3, 0, 2],
            [0, 2, 0, 1, 0], [1, 3, 3, 2, 0],
            [0, 0, 1, 2, 1], [2, 0, 0, 3, 0]]
        validate(allocate(availability),availability)
    def testQ1Set1(self):
        # [2,3,1,4,3],[1,0,0,2,4] # 1 to 3 per roommate
        # see if the sparsest case works
        availability = [[0,2,1,0,0],[2,0,0,1,0],[2,1,0,0,0],[0,0,2,0,1],[0,0,0,1,2]]
        self.assertEqual(allocate(availability),([2,3,1,4,3],[1,0,0,2,4]))
        testList = [
            [[0,2,1,0,1],[2,1,0,1,0],[2,1,0,0,1],[0,0,2,1,1],[1,0,0,1,2]],
            [[0,3,3,0,0],[3,0,0,3,0],[3,3,0,0,0],[0,0,3,0,3],[0,0,0,3,3]],
            [[2,2,1,0,1],[2,1,2,1,0],[2,1,1,2,0],[1,2,2,0,1],[0,2,1,1,2]],
            [[1,2,1,2,3],[2,3,2,1,1],[2,1,2,3,1],[1,3,2,2,1],[3,1,2,1,2]],
            [[1,2,1,1,1],[2,2,2,1,2],[2,1,3,3,3],[3,3,2,3,1],[1,1,1,1,2]]
        ]
        for availability in testList:
            with self.subTest(i=availability):
                results = allocate(availability)
                validate(results,availability,cannotBeNone=True)
    def testQ1Set2(self):
        # [0,1,2,2,0,3,0,1,0,4,4],[1,2,4,0,2,4,3,5,2,3,1] # 3 to 5 per roommate
        # see if the sparsest case works
        availability = [[1,2,0,0,0],[0,1,2,0,0],[0,0,1,0,2],[2,0,1,0,0],[1,0,2,0,0],
                        [0,0,0,1,2],[1,0,0,2,0],[0,1,0,0,0],[1,0,2,0,0],[0,0,0,2,1],[0,2,0,0,1]]
        self.assertEqual(allocate(availability),([0,1,2,2,0,3,0,1,0,4,4],[1,2,4,0,2,4,3,5,2,3,1])) 
        testList = [
            [[1,2,1,0,0],[1,1,2,0,0],[1,0,1,0,2],[2,0,1,0,1],[1,1,2,0,0],[1,0,0,1,2],[1,0,1,2,0],[0,1,0,0,1],[1,1,2,0,0],[0,1,0,2,1],[1,2,0,0,1]],
            [[1,2,2,2,0],[2,1,2,0,2],[2,0,1,0,2],[2,0,1,0,2],[1,2,2,0,0],[2,0,0,1,2],[1,2,0,2,0],[2,1,0,0,0],[1,2,2,0,0],[0,2,0,2,1],[0,2,0,2,1]],
            [[3,3,0,0,0],[0,3,3,0,0],[0,0,3,0,3],[3,0,3,0,0],[3,0,3,0,0],[0,0,0,3,3],[3,0,0,3,0],[0,3,0,0,0],[3,0,3,0,0],[0,0,0,3,3],[0,3,0,0,3]],
            [[1,2,3,1,2],[3,1,2,2,1],[3,1,1,2,2],[2,2,1,3,1],[1,0,2,0,0],[2,1,3,1,2],[1,1,2,2,3],[2,1,3,1,0],[1,2,2,1,3],[0,0,0,2,1],[3,2,2,1,1]]
        ]
        for availability in testList:
            with self.subTest(i=availability):
                results = allocate(availability)
                validate(results,availability,cannotBeNone=True)
    def testQ1Set3(self):
        # 0 to 1 per teammate
        testList = [
            [[3,0,0,0,3],[0,3,0,3,0]],
            [[2,2,2,1,1],[2,2,1,2,1]],
            [[3,0,0,2,2],[1,0,1,0,3]],
            [[3,0,3,0,3],[0,3,0,3,0]],
            [[1,1,1,2,2],[2,1,1,1,1]],
            [[0,2,0,1,0],[0,0,1,0,2]],
       ]
        for availability in testList:
            with self.subTest(i=availability):
                results = allocate(availability)
                validate(results,availability,cannotBeNone=True)
    def testQ1Impossible(self):
        testList = [
            [[3,0,0,0,3],[3,0,0,0,3]],
            [[3,3,3,3,3],[3,3,3,3,3],[0,0,0,0,3],[3,3,3,3,3],[3,3,3,3,3]],
            [[0,0,0,0,0]],
            [[0,0,1,0,2],[2,0,0,0,1],[2,1,0,0,0],[0,0,2,0,1],[0,0,0,1,2]],
            [[0,1,0,0,2],[2,0,0,0,1],[2,1,0,0,0],[2,0,0,0,1],[0,0,0,1,2]],
            [[0,0,2,0,1],[0,2,1,0,0],[0,0,0,1,2],[2,0,0,1,0],[2,1,0,0,0],[3,3,3,3,3],[3,3,3,3,3],[3,3,3,3,3],[0,0,0,0,3]]
       ]
        for availability in testList:
            with self.subTest(i=availability):
                results = allocate(availability)
                self.assertIsNone(results)
    def testQ1EdgeCases(self):
        testList = [
            [],
            [[3,3,3,3,3]],
       ]
        for availability in testList:
            with self.subTest(i=availability):
                results = allocate(availability)
                validate(results,availability,cannotBeNone=True)
    def testQ1DoubleRestaurant(self):
        availability = [] 
        for _ in range(4):
            availability += [[0,0,2,0,1],[0,2,1,0,0],[0,0,0,1,2],[2,0,0,1,0],[2,1,0,0,0]]
        results = allocate(availability)
        validate(results,availability,cannotBeNone=True)
        availability.append([0,0,0,0,0])
        results = allocate(availability)
        validate(results,availability,cannotBeNone=True)
        
unittest.main()