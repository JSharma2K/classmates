from pydantic import BaseModel
from typing import Dict, Any,Optional

class UserNode(BaseModel):
    id: int
    full_name: str
    school: str
    graduation_year: Optional[int] = None
    major: Optional[str] = None
    age: int
    location: str

    def __repr__(self):
        return (f"Hi my name is: {self.full_name!r}, "
                f"I am age={self.age!r} years old, "
                f"I graduated from {self.school} in the year: {self.graduation_year}")

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

    def to_networkx_node(self) -> Dict[str, Any]:
        return {
            'node': self.id,
            'attributes': {
                'name': self.full_name,
                'age': self.age,
                'graduation_year': self.graduation_year,
                'major': self.major,
                'high_school': self.school,
            }
            }
