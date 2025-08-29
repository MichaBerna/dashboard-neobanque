# Description des colonnes

## Tableau explicatif

Voici la description des colonnes qui sont gardées pour l'entraînement du modèle, et pour son exploitation via l'API.

| Numéro | Nom de la Colonne | Description |
|-|-|-|
| 1 | CODE_GENDER  | Genre du client. Valeurs possibles : "M" (masculin), "F" (féminin). |
| 2 | NAME_INCOME_TYPE  | Type de revenu du client. Valeurs possibles : "Working", "State servant", "Pensioner", "Commercial associate", "Student", "Unemployed", "Businessman", "Maternity leave".  |
| 3 | NAME_EDUCATION_TYPE  | Niveau d'éducation du client. Valeurs possibles : "Secondary / secondary special", "Higher education", "Incomplete higher", "Lower secondary", "Academic degree".  |
| 4 | NAME_HOUSING_TYPE | Type de logement du client. Valeurs possibles : "House / apartment", "With parents", "Municipal apartment", "Rented apartment", "Office apartment", "Co-op apartment". |
| 5 | DAYS_BIRTH | Âge du client en jours au moment de la demande de prêt (valeur négative, plus la valeur est petite, plus le client est âgé). |
| 6 | DAYS_EMPLOYED   | Temps d'emploi du client en jours au moment de la demande de prêt (valeur négative). |
| 7 | DAYS_REGISTRATION | Temps depuis l'enregistrement du client en jours au moment de la demande de prêt (valeur négative). |
| 8 | DAYS_ID_PUBLISH | Temps depuis la publication de l'identification du client en jours au moment de la demande de prêt (valeur négative). |
| 9 | FLAG_EMP_PHONE  | Indique si le client a un téléphone professionnel. Valeurs possibles : 1 (oui), 0 (non).  |
| 10  | REGION_RATING_CLIENT | Évaluation de la région où vit le client.   |
| 11  | REG_CITY_NOT_LIVE_CITY | Indique si la ville de résidence du client est différente de la ville d'enregistrement. Valeurs possibles : 1 (oui), 0 (non).  |
| 12  | REG_CITY_NOT_WORK_CITY | Indique si la ville de travail du client est différente de la ville d'enregistrement. Valeurs possibles : 1 (oui), 0 (non).  |
| 13  | EXT_SOURCE_1 | Score normalisé de la source externe 1 (score de crédit externe). |
| 14  | EXT_SOURCE_2 | Score normalisé de la source externe 2 (score de crédit externe). |
| 15  | EXT_SOURCE_3 | Score normalisé de la source externe 3 (score de crédit externe). |
| 16  | YEARS_BEGINEXPLUATATION_AVG | Âge moyen du début de l'exploitation des immeubles dans la région du client. |
| 17  | YEARS_BUILD_AVG | Âge moyen de construction des immeubles dans la région du client. |
| 18  | ELEVATORS_AVG   | Nombre moyen d'ascenseurs dans les immeubles de la région du client.  |
| 19  | ENTRANCES_AVG   | Nombre moyen d'entrées dans les immeubles de la région du client. |
| 20  | FLOORSMAX_AVG   | Nombre moyen d'étages maximum dans les immeubles de la région du client.  |
| 21  | FLOORSMIN_AVG   | Nombre moyen d'étages minimum dans les immeubles de la région du client.  |
| 22  | HOUSETYPE_MODE  | Type de maison le plus fréquent dans la région du client. Valeurs possibles : "Block of flats", "Specific housing", "Terraced house", etc.  |
| 23  | WALLSMATERIAL_MODE   | Matériau des murs le plus fréquent dans les immeubles de la région du client. Valeurs possibles : "Stone, brick", "Wood, log", "Panel", etc.   |
| 24  | EMERGENCYSTATE_MODE  | État d'urgence le plus fréquent des immeubles dans la région du client. Valeurs possibles : "No", "Yes".   |
| 25  | DAYS_LAST_PHONE_CHANGE | Temps depuis le dernier changement de téléphone du client en jours (valeur négative).  |
| 26  | FLAG_DOCUMENT_3 | Indique si le client a fourni le document 3. Valeurs possibles : 1 (oui), 0 (non). |

## Hypothèses supplémentaires

Les sources externes fournissent un score normalisé (colonnes EXT_SOURCE_1, EXT_SOURCE_2, EXT_SOURCE_3). Nous ne connaissons pas ces sources, aussi nous ne les nommeront que par "notation externe".

Le champ FLAG_DOCUMENT_3 sera traduit dans notre solution par un indicateur précisant si le client a bien fourni tous les documents nécessaires au crédit. 