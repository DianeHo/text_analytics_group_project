import textblob
from afinn import Afinn
from nltk.corpus import sentiwordnet as swn
import spacy
nlp = spacy.load('en_core_web_sm')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# textblob
def analyze_sentiment_textblob(review, threshold=1.0):
    # sentiment_polarity = [textblob.TextBlob(review).sentiment.polarity for review in src02.test_reviews]
    # predicted_sentiments = ['positive' if score >= 0.1 else 'negative' for score in sentiment_polarity]
    score = textblob.TextBlob(review).sentiment.polarity 
    final_sentiment = 'positive' if score >= threshold else 'negative'
    return final_sentiment

# afinn
def analyze_sentiment_afinn(review, threshold=1.0):
    afn = Afinn(emoticons=True)
    score = afn.score(review) 
    final_sentiment = 'positive' if score >= threshold else 'negative'
    return final_sentiment


def analyze_sentiment_sentiwordnet_lexicon(review, verbose=False):

    # tokenize and POS tag text tokens
    tagged_text = [(token.text, token.tag_) for token in nlp(review)]
    pos_score = neg_score = token_count = obj_score = 0
    # get wordnet synsets based on POS tags
    # get sentiment scores if synsets are found
    for word, tag in tagged_text:

        ss_set = None
        if 'NN' in tag and list(swn.senti_synsets(word, 'n')):
            ss_set = list(swn.senti_synsets(word, 'n'))[0]
        elif 'VB' in tag and list(swn.senti_synsets(word, 'v')):
            ss_set = list(swn.senti_synsets(word, 'v'))[0]
        elif 'JJ' in tag and list(swn.senti_synsets(word, 'a')):
            ss_set = list(swn.senti_synsets(word, 'a'))[0]
        elif 'RB' in tag and list(swn.senti_synsets(word, 'r')):
            ss_set = list(swn.senti_synsets(word, 'r'))[0]

        # if senti-synset is found
        if ss_set:

            # add scores for all found synsets
            pos_score += ss_set.pos_score()
            neg_score += ss_set.neg_score()
            obj_score += ss_set.obj_score()
            token_count += 1

    # aggregate final scores
    final_score = pos_score - neg_score
    norm_final_score = round(float(final_score) / token_count, 2)
    final_sentiment = 'positive' if norm_final_score >= 0 else 'negative'

    if verbose:

        norm_obj_score = round(float(obj_score) / token_count, 2)
        norm_pos_score = round(float(pos_score) / token_count, 2)
        norm_neg_score = round(float(neg_score) / token_count, 2)

        print('SENTIMENT STATS:')
        print('Predicted Sentiment', final_sentiment)
        print('Objectivity', norm_obj_score)
        print('Positive', norm_pos_score)
        print('Negative', norm_neg_score)
        print('Overall', norm_final_score)

    return final_sentiment

def analyze_sentiment_vader_lexicon(review, threshold=1.0, verbose=False):

    # analyze the sentiment for review
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(review)

    # get aggregate scores and final sentiment
    agg_score = scores['compound']
    final_sentiment = 'positive' if agg_score >= threshold else 'negative'
    
    if verbose:

        # display detailed sentiment statistics
        positive = str(round(scores['pos'], 2)*100)+'%'
        final = round(agg_score, 2)
        negative = str(round(scores['neg'], 2)*100)+'%'
        neutral = str(round(scores['neu'], 2)*100)+'%'

        print('SENTIMENT STATS:')
        print('Predicted Sentiment', final_sentiment)
        print('Polarity Score', final)
        print('Positive', positive)
        print('Negative', negative)
        print('Neutral', neutral)

    return final_sentiment

if __name__ == "__main__":
    new_corpus = ['The Lord of the Rings is an Excellent movie',
                'I did not like the recent movie on TV It was NOT good and a waste of time']
    
    for review in new_corpus:
        print(review)
        sentiment = analyze_sentiment_textblob(review)
        print(sentiment)
        sentiment = analyze_sentiment_afinn(review)
        print(sentiment)
        sentiment = analyze_sentiment_sentiwordnet_lexicon(review)
        print(sentiment)
        sentiment = analyze_sentiment_vader_lexicon(review)
        print(sentiment)