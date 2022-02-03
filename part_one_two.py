############################## Part1 ####################################
# Python 3.8.5

import json
from pathlib import Path
import re
import os
import csv
txtpath=os.path.join('output','Clean_reviews_JZ.json')
csvpath=os.path.join('output','Clean_reviews_JZ.csv')
with open(Path('raw_reviews.json'), 'r') as f:
    data=json.load(f)
    
class Solution:
    
    def data_cleansing (self, data):
        app_type={'airbnb':'Personalization','experian':'Financial','duolingo':'gamification', 'nike':'Personalization'}
        # create a list of final columns
        pat1=re.compile(u"(\u2018|\u2019)") # single quote
        pat2=re.compile(u"(\u201c|\u201d)") # double quote
        pat3=re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pic
        u"\U0001F680-\U0001F6FF"  # transport & map 
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
        for record in data:
            try:
                if bool(record['user_nickname'])==False:
                    record['user_nickname']='User name unavailable'
            except:
                pass
            try:
                record['review_rating']=int(record['review_rating'])
            except:
                pass
            try:
                record['app_name']=''.join(record['app_name'].lower().split()).title() # remove all space
            except:
                pass
            try: 
                record['syndication_flag']=record['syndication_flag'].lower() in ("yes", "true", "t", "1")
            except:
                pass
            record['review_text']=re.sub(pat1, "'", record['review_text'])
            record['review_text']=re.sub(pat2, '"', record['review_text'])
            record['review_text']=re.sub(pat3, ' ', record['review_text'])

            record['review_text_len']=len(record['review_text'])
            record['processed_flag']=True # indicate the completion of data transformation
            record.pop('developer_response_text', None)
            record.pop('developer_response_date', None)
            record['app_type']= app_type[''.join(record['app_name'].lower().split())]
        return data
Solution().data_cleansing(data)

with open(txtpath,'w') as jsonfile:
    json.dump(data, jsonfile)
###################################### part2####################################
# identify column headers
columns=[]
for r in data:
    for k, v in r.items():
        columns.append(k)
columns=list(set(columns))

with open(csvpath,'w') as out_file:
    csv_w=csv.writer(out_file)
    csv_w.writerow(columns)
    for i_r in data:
        csv_w.writerow(map(lambda x: i_r.get(x, ""), columns))