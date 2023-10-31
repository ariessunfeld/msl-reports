from .constants import TOPIC_URL_TO_FUNC_NAME

class Report:
    def __init__(self, sol, role, topics):
        self.sol = sol
        self.role = role
        self._topics = topics
        self.topics = []
        
        # Create attributes for each topic based on the mapping
        for topic_key, topic_content in self._topics.items():
            pythonic_name = TOPIC_URL_TO_FUNC_NAME.get(topic_key, None)
            if pythonic_name:
                setattr(self, pythonic_name, topic_content)
                self.topics.append(pythonic_name)

    def init_defaults(self):
        self.summary = None
        self.contacts = None
    