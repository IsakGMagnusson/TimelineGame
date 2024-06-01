SELECT_HUMAN_AND_BIRTHDATE = 'SELECT ?human ?humanLabel ?date WHERE{'
INSTANCE_HUMAN = '?human wdt:P31 wd:Q5;'
GENDER_MALE = 'wdt:P21 wd:Q6581097;'
GENDER_FEMALE = 'wdt:P21 wd:Q6581072;'
BORN_SWEDEN = 'wdt:P19/wdt:P131* wd:Q34;'
YEAR_BIRTH = 'wdt:P569 ?date;'

END_STRING = 'wikibase:sitelinks ?sitelinks. SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }}ORDER BY DESC(?sitelinks)LIMIT 45'