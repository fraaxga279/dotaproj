# датасеты

[датасет на kaggle](https://www.kaggle.com/datasets/atolm1110/hota-hw-dataset) · [соревнование](https://www.kaggle.com/competitions/dota-2-hse-ml-1-course-competition-2026)


| файл | содержимое |
|---|---|
| matches_df_train.csv | матчи и ответ radiant_win |
| matches_df_test.csv | матчи без ответа |
| player_df.csv | игроки, слоты и герои |
| Constants.Heroes.csv | справочник героев |
| game_chat.csv | сообщения radiant и dire за первые 15 минут |
| dota_adv.csv | преимущество по золоту и опыту по минутам |

в `player_df.csv` берутся только составы: остальная статистика почти полностью скрыта в test. итоговая длительность матча в модель не добавляется.