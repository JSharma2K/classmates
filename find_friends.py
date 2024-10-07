import networkx as nx
import re
from rapidfuzz import fuzz
from units import UserNode
'''
    id: int
    full_name: str
    school: str
    graduation_year: Optional[int] = None
    major: Optional[str] = None
    age: int
    location: str
'''
class ScoreCard:
    def __init__(self,user_1:UserNode,user_2:UserNode):
        self.user_1=user_1
        self.user_2=user_2
        self.school_weight=0.4
        self.graduation_weight=0.3
        self.age_weight=0.3
    def get_score(self):
        score=[self.school_match_score(),self.graduation_year_score(),self.age_score()]
        return sum(score)

    def school_match_score(self):
        score=fuzz.WRatio(self.user_1.school,self.user_2.school)
        return self.school_weight*(score/100)

    def graduation_year_score(self):
        if self.user_1.graduation_year==self.user_2.graduation_year:
            return self.graduation_weight*1
        else:
            return self.graduation_weight*0
    def age_score(self):
        buffer=2
        user_1_age_under=self.user_1.age-buffer
        user_1_age_over=self.user_1.age+buffer
        if user_1_age_under<self.user_2.age<user_1_age_over:
            return self.age_weight*1
        elif user_1_age_under==self.user_2.age:
            return self.age_weight*0.8
        elif user_1_age_over==self.user_2.age:
            return self.age_weight*0.8
