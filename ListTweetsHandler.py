import re


class ListTweetsHandler:
    def analyseDataSentimental(self, listTweets):
        listRelations = []
        for tweet in listTweets:
            if not next((item for item in listRelations if item["location"] == tweet['location']), False):
                sentimentals = {
                    "POSITIVE": 0,
                    "NEGATIVE": 0,
                    "NEUTRAL": 0,
                    "MIXED": 0
                }
                sentimentals[tweet['sentimental']] += 1
                listRelations.append({'location': tweet['location'], 'sentimentals': sentimentals})
            else:
                itemExists = next((item for item in listRelations if item["location"] == tweet['location']), False)
                itemExists['sentimentals'][tweet['sentimental']] += 1

        return listRelations

    def calculatePercentage(self, listRelations):
        percentage = []
        for item in listRelations:
            print(item)
            sumValue = sum(item['sentimentals'].values())
            item['sentimentals']['POSITIVE'] = (item['sentimentals']['POSITIVE'] * 100) / sumValue
            item['sentimentals']['NEGATIVE'] = (item['sentimentals']['NEGATIVE'] * 100) / sumValue
            item['sentimentals']['NEUTRAL'] = (item['sentimentals']['NEUTRAL'] * 100) / sumValue
            item['sentimentals']['MIXED'] = (item['sentimentals']['MIXED'] * 100) / sumValue
            percentage.append(item)
        return percentage

    def onlyCharacters(self, input):
        regex = re.compile('[^a-zA-Z]')
        return regex.sub('', input)