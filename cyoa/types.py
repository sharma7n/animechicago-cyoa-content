import enum

import attr


@attr.s
class MockModel(object):
    id: int = attr.ib(init=False)
    
    def __attrs_post_init__(self):
        self.id = id(self)

@attr.s
class Question(MockModel):
    """ A question with one or more possible answers. """
    
    root: bool = attr.ib()
    text: str = attr.ib()

@attr.s
class Source(MockModel):
    """ A place where the recommendation can be accessed or obtained. """
    
    name: str = attr.ib()
    url: str = attr.ib()

@attr.s
class Recommendation(MockModel):
    """ A media item recommended by the app. """
    
    title: str = attr.ib()
    description: str = attr.ib()
    available_on: list = attr.ib()
    
    def available_on_iter(self):
        return self.available_on

@attr.s
class Choice(MockModel):
    """ Question answer that may lead to another question or a recommendation. """
    
    question: Question = attr.ib()
    text: str = attr.ib()
    result_type: str = attr.ib()
    
    result_question: Question = attr.ib(default=None)
    result_recommendation = attr.ib(default=None)
    
    @property
    def result(self):
        return {
            "Question": self.result_question,
            "Recommendation": self.result_recommendation,
        }.get(self.result_type)