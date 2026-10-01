class ParcelAssessment:
    def __init__(self, parcel, rules):
        if not rules:
            raise ValueError("At least one rule is required")
        self._parcel = parcel
        self._rules = list(rules)

    def evaluate(self):
        results = []
        for rule in self._rules:
            result = rule.evaluate(self._parcel)
            results.append(result)
        return results

    def passed(self):
        for result in self.evaluate():
            if not result.passed:
                return False
        return True