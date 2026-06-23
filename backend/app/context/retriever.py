class ContextRetriever:

    def retrieve(
        self,
        query: str,
        messages: list
    ):

        results = []

        for message in messages:

            if query.lower() in message.lower():

                results.append(
                    message
                )

        return results