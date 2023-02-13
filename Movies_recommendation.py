# Librabry
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import string
import numpy as np
from flask import Flask, request, jsonify,render_template,redirect
import flask
from werkzeug.wrappers import response


app = Flask(__name__)
# Questionaires

colours = pd.read_excel("data/Questionaires.xlsx",sheet_name = "Colours")
zodiacs = pd.read_excel("data/Questionaires.xlsx",sheet_name = "Western_Zodiacs")
numbers = pd.read_excel("data/Questionaires.xlsx",sheet_name = "Numbers")
musical_instruments = pd.read_excel("data/Questionaires.xlsx",sheet_name = "Musical_instruments")
social_media = pd.read_excel("data/Questionaires.xlsx",sheet_name = "Social_media")
music_genres = pd.read_excel("data/Questionaires.xlsx",sheet_name = "Music_genres")
seasons = pd.read_excel("data/Questionaires.xlsx",sheet_name = "Seasons")
alignments = pd.read_excel("data/Questionaires.xlsx",sheet_name = "Alignment")
zodiacs = zodiacs.set_index('Name_Vi')
numbers = numbers.set_index('Name_Vi')
colours = colours.set_index('Name_Vi')
musical_instruments = musical_instruments.set_index('Name_Vi')
music_genres = music_genres.set_index('Name_Vi')
seasons = seasons.set_index('Name_Vi')
alignments = alignments.set_index('Name_Vi')
social_media = social_media.set_index('Name_Vi')
train = pd.read_csv('data/cold_start_train.csv')
train = train.set_index('ID')
train_sim = train.iloc[:,21:]

mvs = pd.read_excel("data/Questionaires.xlsx",sheet_name = "Movies").set_index('Movie_ID')

data = {'zodiac':zodiacs,
        "colour":colours,
        "number":numbers,
        "season":seasons,
        "music":music_genres,
        "musical_instrument":musical_instruments,
        "social_media":social_media,
        "alignment":alignments
        }

#Function for calculating user MBTI
def count(asr):
  c = []
  c.append(str(len(asr[asr.MBTI_E > 60])) + '|' + str(len(asr[asr.MBTI_I > 60])))
  c.append(str(len(asr[asr.MBTI_S > 60])) + '|' + str(len(asr[asr.MBTI_N > 60])))
  c.append(str(len(asr[asr.MBTI_T > 60])) + '|' + str(len(asr[asr.MBTI_F > 60])))
  c.append(str(len(asr[asr.MBTI_J > 60])) + '|' + str(len(asr[asr.MBTI_P > 60])))
  return c

def compare_MBTI(mbti):
    #"""Get user MBTI in text form"""
  result = []
  if mbti.MBTI_E > mbti.MBTI_I:
    result.append('E')
  elif mbti.MBTI_E < mbti.MBTI_I:
    result.append('I')
  else:
    result.append('X')

  if mbti.MBTI_S > mbti.MBTI_N:
    result.append('S')
  elif mbti.MBTI_S < mbti.MBTI_N:
    result.append('N')
  else:
    result.append('X')

  if mbti.MBTI_T > mbti.MBTI_F:
    result.append('T')
  elif mbti.MBTI_T < mbti.MBTI_F:
    result.append('F')
  else:
    result.append('X')

  if mbti.MBTI_J > mbti.MBTI_P:
    result.append('J')
  elif mbti.MBTI_J < mbti.MBTI_P:
    result.append('P')
  else:
    result.append('X')

  result = ''.join(result)
  return result

def transfer_anwrs(res):
    #""" One-hot encoding user's answers"""
    trans = [i.split('__')[-1] for i in train.columns[21:]]
    a_t = []
    mbti = trans[:11]
    zodiac = trans[11:23]
    colour = trans[23:33]
    number = trans[33:42]
    season = trans[42:46]
    music_genre = trans[46:52]
    musical_instrument = trans[52:60]
    social_media = trans[60:66]
    alignment = trans[66:]
    ans = [mbti,zodiac,colour,number,season, music_genre, musical_instrument,social_media,alignment]
    count = 0
    for r, q in zip(res,ans):
        for k in q:
            if r == k:
                a_t.append(1)
            else:
                a_t.append(0)
        count +=1
    return a_t

# Run quiz

def run_quiz(list_answers, data):
  answers = pd.DataFrame(columns = ['MBTI_E', 'MBTI_I', 'MBTI_S', 'MBTI_N', 'MBTI_T', 'MBTI_F','MBTI_J', 'MBTI_P'])
  references = []
  for (answr,context) in zip(list_answers,data.keys()):
    obj = data[context]
    references.append(answr)
    awsr = data[context].loc[answr,['MBTI_E', 'MBTI_I', 'MBTI_S', 'MBTI_N', 'MBTI_T', 'MBTI_F','MBTI_J', 'MBTI_P']]
    answers.loc[answers.shape[0]] = awsr.values

  #ratio = count(answers)
  answers = answers.sum()/8
  answers = answers.round()
  _MBTI = compare_MBTI(answers)
  res = [_MBTI] + references
  res = transfer_anwrs(res)
  return res, _MBTI

# Recommendation
# Cosine similarity
def cs_cos_sim(user_, user2_id):
  user1_in4 = np.array(user_[0]).reshape(1, -1)
  user2 = train_sim.loc[user2_id,:].values.reshape(1, -1)
  sim = cosine_similarity(user1_in4,user2)[0][0]
  return sim

#Không lấy topN do dữ liệu nhỏ
def cs_get_topN_user(user):
  # Ignore ratings == 0
  mbti_user = user[1]
  sim = train_sim[(train.off_mbti == mbti_user)]
  urs = sim.index.to_list()
  scores = [(cs_cos_sim(user, userID),userID) for userID in urs ] 
  return scores

def cs_get_rating(userid, movieid):
  return(train.loc[userid,str(movieid)])


def cs_predict_rating(user):
  ratings = []
  mvid = []
  df = train.copy()
  sim_users = cs_get_topN_user(user)
  if len(sim_users) != 0:
    for mvID in df.columns[1:21]:
      sum_ = 0
      sum_sim = 0
      for score,userID in sim_users:
        if cs_get_rating(userID, mvID) != 0 :
          sum_ += score
          sum_sim += score*cs_get_rating(userID, mvID)
      if sum_ == 0:
        ratings.append(0)
      else:
        rate = (1/sum_)*sum_sim
        ratings.append(rate)
      mvid.append(mvID)
  else:
    ratings = [0 for i in range(20)]
  rtgs = [(r,id) for r, id in zip(ratings,mvid)]
  rtgs.sort(reverse=True)
  return rtgs

def list_mv(rating_pred):
    return [mvs.loc[int(id[1]),'Title'] for id in rating_pred]
#%app

@app.route("/", methods=["GET"])
def get_index():
    return redirect("/survey")

@app.route("/survey", methods=["GET"])
def home():
   return render_template("survey.html")

@app.route("/survey", methods=["POST"])
def survey():
    if flask.request.method == "POST":
        zodiac = str(request.form.get('Zodiac'))
        colour = str(request.form.get('Colour'))
        number = int(str((request.form.get('Number') )))
        season = str(request.form.get('Season') )
        msc_genres = str(request.form.get('Music_genre') )
        muscl_instrument = str(request.form.get('Musical_instrument') )
        sm = str(request.form.get('Social_media') )
        algmnt = str(request.form.get('Alignment') )
        response_ = [zodiac,colour,number,season,msc_genres,muscl_instrument,sm, algmnt]
        user = run_quiz(response_,data)
        in4 = {}
        in4['MBTI type'] = user[1]

        # Recommend movies
        mv_list = list_mv(cs_predict_rating(user))
        order = [i+1 for i in range(len(mv_list))]
        recommendation = [[o,r] for o,r in zip(order,mv_list)]
        return render_template("output.html", surveys=recommendation)


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=5183)
