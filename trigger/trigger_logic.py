class FakeTrigger(object):
    def __init__(self) -> None:
        super().__init__()
    def process(self, action_name):
        print("fake processing: {}".format(action_name))