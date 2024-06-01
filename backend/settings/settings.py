from .constants import *
from datetime import datetime
from classes import Setting


class SettingTypes:
    BIRTHDATES = 1


all_settings = [
    Setting(
        "males_from_sweden",
        f"""
            {SELECT_HUMAN_AND_BIRTHDATE}
            {INSTANCE_HUMAN}
            {GENDER_MALE}
            {BORN_SWEDEN}
            {YEAR_BIRTH}
            {END_STRING}
    """,
        SettingTypes.BIRTHDATES,
    ),
    Setting(
        "females_from_sweden",
        f"""
            {SELECT_HUMAN_AND_BIRTHDATE}
            {INSTANCE_HUMAN}
            {GENDER_FEMALE}
            {BORN_SWEDEN}
            {YEAR_BIRTH}
            {END_STRING}
        """,
        SettingTypes.BIRTHDATES,
    ),
]


def get_question_from_setting_type(wiki_return_value, setting_type):
    match setting_type:
        case SettingTypes.BIRTHDATES:
            return (
                "What year was "
                + wiki_return_value["humanLabel"]["value"]
                + " born?"
                + str(
                    datetime.strptime(
                        wiki_return_value["date"]["value"], "%Y-%m-%dT%H:%M:%S%z"
                    ).year
                )
            )
        case _:
            return 0


nbaplayers = """
SELECT ?human ?humanLabel ?year_of_birth
WHERE
{
  ?human wdt:P31 wd:Q5; #instance of: human
         wdt:P118 wd:Q155223;    #leauge: nba
         wdt:P569 ?year_of_birth;
         wikibase:sitelinks ?linkcount .

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
}  
ORDER BY DESC(?linkcount)
LIMIT 50
"""
