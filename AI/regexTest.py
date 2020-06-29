import re 

mystring=[
"RT @DadePhelan: @MHATPolicy @GovAbbott @MHATexas Proud to Joint Author! Thank you @NicoleCollier95. Great mental health legislation\u2026 ",
"RT @AmyJRomine: How \qtDaily Uplifts\qt Can Counter Depression ~ 4 Key Findings From a New Study on Mood https:\/\/t.co\/zP7mypsRse\u2026 ",
"Anxiety leads to tears.",
"RT @creaturecharlie: ur mcm is cute but in an ugly way and uses memes and irony to hide his burdening depression from everyone, it's me, i'\u2026",
"Hmm pie charts might work better for me \ud83d \udc4c \ud83c \udffd https:\/\/t.co\/YgvoGBOgNb",
"Imagine living with the constant fear that your clothing could spontaneously combust off your body any second\nhttps:\/\/t.co\/3gWtcKLO53",
"RT @ArtFeeIing: what anxiety feels like https:\/\/t.co\/tGJwlXvtC8",
"The Truth About Manic Depression, from One Who\u2019s Been There https:\/\/t.co\/YP0Hg530Dh",
"I had so much anxiety walking this https:\/\/t.co\/KV9lyjR59P",
"Paramount Pictures Mental Health Break. https:\/\/t.co\/8hM0tFYSVz",
"RT @Lina1nyc: @AlfredoJalifeR_ @marvinicio @norma22flores @Saucedina https:\/\/t.co\/Wod1fo3U8U",
"RT @literallymeg: I wouldn't wish severe anxiety on even my worst enemy",
"RT @jedigrumps: Going outside after a couple of days after a long episode of depression https:\/\/t.co\/yzyM9keixs",
"RT @directorLACDMH: Thanks for supporting the #LACDMH #MentalHealth efforts in Long Beach! @SupJaniceHahn @211LACounty https:\/\/t.co\/897IjKs\u2026",
"RT @traciethoms: But seriously, why aren't Presidental candidates required to take a mental health exam?",
"Always get scared when Zoo randomly calls me. Gets me anxiety idk what this shit could be about",
"RT @Griffith_Uni: #GriffithUni research has found being active increases the mental health and wellbeing of Australian uni students \ud83c\udfc3 https\u2026",
"Like you motherfuckers are the picture of mental health. \ud83d\ude02",
"RT @Kustomz_: @rodcub @janet_rice @Greens @lanesainty https:\/\/t.co\/tiHmUOv9hu",
"The Ultimate Guide To Social Anxiety and Bipolar Disorder https:\/\/t.co\/UWamxKNM9y",
"RT @fireball_beto: Y'all don't know anxiety until you're trapped at the bottom of this https:\/\/t.co\/Buy42JMHu3",
"RT @dolly_ste: \ud83d\udcaa\ud83d\udcaa\ud83d\ude00\ud83d\udc4a\ud83c\udffb\ud83d\udc4a\ud83c\udffb\ud83d\udc4a\ud83c\udffb\ud83d\udc4a\ud83c\udffb\ud83d\ude43\ud83e\udd1banother one with mental health issues \ud83d\ude00\ud83d\ude00 https:\/\/t.co\/p4Qb42GRnK",
"Do you have lived experience of depression [incl. family, carers, health professionals]? Please complete this survey https:\/\/t.co\/rolXqygLRk",
"Awww \ud83d\ude1e https:\/\/t.co\/cT0RYsoGTZ",
"RT @kourtneykardash: Great way to calm anxiety. https:\/\/t.co\/Wxr4PNkg8m",
"Going to bed so goodnight everyone and sweet dreams http://twitpic.com/2y2e0",
"www.twitter.com/Go0seEgg .. add our baby!!!",
"Watching funny TV show clips on Hulu.com",
"@deecho  can't wait. &amp; I'll cook something for ya.",
"Depression........  pic.twitter.com/hkM67Dbys0"
"@MikeStuchbery_ m.youtube.com/watch?feature=youtu.be&v=DQUgd9GQtoQÃ‚Â Ã¢Â€Â¦ this was excellent talk on depression.  <Emoji: Moyai>"


]

emoji_pattern = re.compile("["
   u"\U0001F600-\U0001F64F"  # emoticons
   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
   u"\U0001F680-\U0001F6FF"  # transport & map symbols
   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
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
   "]+", flags=re.UNICODE)


mystring1 = list(map(lambda x:emoji_pattern.sub(r'',x),mystring)) #remove emoticons
print('**************************')

# for item in mystring1:
#     print(item)

# print(mystring1[1])

mystring2 = list(map(lambda x: re.sub("RT"," ",x),mystring1)) #remove RT 
mystring2 = list(map(lambda x: re.sub("(@\S+)"," ",x),mystring2)) #remove @handles
#mystring2 = list(map(lambda x: re.sub("(https\S+)"," ",x),mystring2)) #remove @handles
mystring2 = list(map(lambda x: re.sub("((https|http|www)\S*)|([a-z]+.[a-z]+\.com/[a-zA-z0-9=?/.&]*)|([a-z]+.[a-z]+\.com)|(\S+\.com)"," ",x),mystring2)) #remove @handles



for item in mystring2: 
	print(item)

print('*************************')
string15 = 'This is \qtis the\qt'
print(string15)
print('\"')
print('\qt')
string15 = string15.replace('\qt','\"')
print(string15)


