regexes = {
    "ref": "[0-9]{8,10}P[0-9]",
    "date": "[0-9]{2}/[0-9]{2}/[0-9]{4}",
    "code": "[0-9]{5}",
    "tel": "[0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2}",
    "$" : "\$"
}

rules = {
    "pdf_main": [
        {
            "min_score" : 41,
            "max_score" : 49,
            "rules": """
                init a=0, s=0, d=0, f=0, r=0;

                once after f=0 and <<Fax>> set f=1;
                once after f=1 and <<Fax>> set f=2;

                start after f=2 and @$
                stop when @$ set f=3
                store as 'Assurance' weight 5;

                start when r=0 and @ref
                stop after @ref set r=1
                store as 'Ref' weight 5;

                start when d=0 and @date
                stop after @date set d=1
                store as 'Date1' weight 5;

                start when d=1 and @date
                stop after @date set d=2
                store as 'Date2' weight 5;

                start after <<Dossier\$\:\$>>
                stop when @$ store as 'Dossier' weight 5;

                start after <<intervention suivante \:\$>>
                stop when @$ store as 'Type' weight 5;

                start after <<Nature du sinistre\:>>
                stop when @$ store as 'Nature' weight 1;

                start after d=2 and @$
                stop when <<Sociétaire>> set d=3
                store as 'Charges' weight 5;

                start after d=3 and @$
                stop when @$ set d=4
                store as 'Societaire' weight 5;

                start after d=4 and @$
                stop when @$ set d=5
                store as 'Police' weight 5;

                start after <<Tél évènement \:>> 
                stop when @$ store as 'Tél ev' weight 1;

                start after <<Portable \:>> 
                stop when @$ set t=1
                store as 'Portable' weight 0;

                start after <<Observations>> 
                stop when <<\$Nous vous remercions>> set t=2
                store as 'Observations' weight 1;
            """
        }
    ],
    "pdf_address" : [
        {
            "min_score": 12,
            "max_score": 12,
            "rules": """
                init p=0;
                once when <<N° Police>> set p=1;
                once after p=1 and @$ set p=2;
                
                start after p=2
                stop when @$ set p=3
                store as 'Adresse 1' weight 3;

                start after p=3
                stop when @$ set p=4
                store as 'Adresse 2' weight 3;

                start when p=4 and @code
                stop after @code set p=5
                store as 'Code' weight 3;

                start after p=5 and @$
                stop when @$ set p=6
                store as 'Ville' weight 3;
            """
        },
        {
            "min_score": 9,
            "max_score": 9,
            "rules": """
                init p=0;
                once when <<N° Police>> set p=1;
                once after p=1 and @$ set p=2;
                
                start after p=2
                stop when @$ set p=3
                store as 'Adresse 1' weight 3;

                start when p=3 and @code
                stop after @code set p=4
                store as 'Code' weight 3;

                start after p=4 and @$
                stop when @$ set p=5
                store as 'Ville' weight 3;
            """
        }
    ],
    "dynaren_main": [
        {
            "min_score": 20,
            "max_score": 20,
            "rules": """
                init d=0,c=0;
                force 'Assurance' to 'Dynaren';

                start after <<N° sinistre \: >>
                stop when @$ store as 'Ref' weight 5;

                start after <<Assuré \: Madame >>
                stop after @$ store as 'Dossier' weight 5;

                start after <<Assuré \: Monsieur >>
                stop after @$ store as 'Dossier' weight 5;

                start after d=0 and <<Nature du sinistre \: >>
                stop when << du >> set d=1 
                store as 'Type' weight 5;

                start when d=1 and @date
                stop after @date set d=2
                store as 'Date' weight 5;

                start after <<Dommages déclarés \:>>
                stop when @$ store as 'Observations' weight 5;
            """
        }
    ],
    "dynaren_address": [
        {
            "min_score": 9,
            "max_score": 9,
            "rules": """
                init a=0;

                once after <<Lieu du sinistre \: >> set a=1;
                
                start when a=1
                stop when @code set a=2
                store as 'Adresse 1' weight 3;
                
                start when a=2 and @code
                stop after @code set a=3
                store as 'Code' weight 3;

                start after a=3
                stop when @$ set a=4
                store as 'Ville' weight 3;
            """
        }
    ],
    "fidelia_dynaren_mail": [
        {
            "min_score": 19,
            "max_score": 27,
            "rules": """
                init d=0,c=0;
                force 'Assurance' to 'Dynaren';

                start after <<N° dossier \: >>
                stop when @$ store as 'Ref' weight 5;

                start when d=0 and @date
                stop after @date set d=1
                store as 'Date' weight 5;

                start after <<Assistance chez \:\$>>
                stop when @$ store as 'Dossier' weight 5;

                start after <<communiqué par l'assureur \: >>
                stop after @$ store as 'Type' weight 5;

                once after <<Libellé de la prise en charge >> set c=1;
                
                start after c=1 and <<\:\$>>
                stop when @$ set c=2 
                store as 'Charges' weight 5;
                
                start after c=1 and <<\: >>
                stop when @$ set c=2
                store as 'Charges' weight 5;

                start after <<N° tél fixe \:>>
                stop when @$ store as 'Tél ev' weight 2;

                start after <<N° téléphone portable \: >>
                stop when @$ store as 'Portable' weight 2;

                start after <<N° téléphone portable \:\$>>
                stop when @$ store as 'Portable' weight 2;

                start after <<dommages et/ou les prestations >>
                stop when <<Veuillez noter les modalit>>
                store as 'Observations' weight 5;
            """
        }
    ],
    "fidelia_dynaren_address": [
        {
            "min_score": 15,
            "max_score": 15,
            "rules": """
                init p=0;

                once after <<Assistance chez \:\$>> set p=1;
                once when p=1 and @$ set p=2;
                
                start after p=2
                stop when @$ set p=3
                store as 'Adresse 1' weight 3;

                start after p=3
                stop when @$ set p=4
                store as 'Adresse 2' weight 3;
                
                start when p=4 and @code
                stop after @code set p=5
                store as 'Code' weight 3;

                start after p=5
                stop when @$ set p=6
                store as 'Ville' weight 3;
                
                once when p=6 and <<Cordialement>> weight 3 set p=7;
            """
        },
        {
            "min_score": 12,
            "max_score": 12,
            "rules": """
                init p=0;

                once after <<Assistance chez \:\$>> set p=1;
                once after p=1 and @$ set p=2;
                
                start after p=2
                stop when @$ set p=3
                store as 'Adresse 1' weight 3;
                
                start when p=3 and @code
                stop after @code set p=4
                store as 'Code' weight 3;

                start after p=4
                stop when @$ set p=5
                store as 'Ville' weight 3;
                
                once when p=5 and <<Cordialement>> weight 3 set p=6;
            """
        }
    ],
    "filassistance_header" : [
        {
            "min_score": 21,
            "max_score": 29,
            "rules": """
                init f=0, d=0, c=0;

                once after f=0 and <<\$Fax\ :>> set f=1;
                once after f=1 and @$ set f=2;
                once after f=2 and @$ set f=3;
                start after f=3 and @$
                stop when @$ set f=4
                store as 'Assurance' weight 0;

                start after f=4 and <<\, le >>
                stop when @$ set f=5
                store as 'Date' weight 5;

                start after <<Numéro de dossier \:\$>>
                stop when @$ store as 'Ref' weight 5;

                start after <<Bénéficiaire \:\$>>
                stop when @$ store as 'Dossier' weight 5;

                start after <<mission suivante \:\$>>
                stop when @$ store as 'Type' weight 5;

                once after c=0 and <<Total\$MISSION\$>> set c=1;
                once after c=1 and @$ set c=2;

                start after c=1
                stop when @$ set c=2
                store as 'Charges' weight 5;

                start after <<Téléphone (principal) \:>>
                stop when @$ store as 'Tél ev' weight 2;

                start after <<Observations \:\$>>
                stop when <<RECAPITULATIF>>
                store as 'Observations' weight 2; 
                
            """
        },
        {
            "min_score": 18,
            "max_score": 22,
            "rules": """
                init d=0, f=0;

                once after f=0 and <<\$Fax\ :>> set f=1;
                once after f=1 and @$ set f=2;
                once after f=2 and @$ set f=3;
                start after f=3 and @$
                stop when @$ set f=4
                store as 'Assurance' weight 0;

                start after f=4 and <<\, le >>
                stop when @$ set f=5
                store as 'Date' weight 5;

                start after <<Numéro de dossier \:\$>>
                stop when @$ store as 'Ref' weight 5;


                start after <<Bénéficiaire \:\$>>
                stop when @$ store as 'Dossier' weight 5;

                start after <<mission suivante \:\$>>
                stop when @$ store as 'Type' weight 5;
                
                start after <<Téléphone (principal) \:>>
                stop when @$ store as 'Tél ev' weight 2;

            """
        }
    ],
    "filassistance_header_address": [
        {
            "min_score": 12,
            "max_score": 12,
            "rules": """
                init p=0;

                once after <<Bénéficiaire \:\$>> set p=1;
                once after p=1 and @$ set p=2;

                start when p=2
                stop after <<\, >> set p=3
                store as 'Adresse 1' weight 3;

                start when p=3 stop after @$ set p=4
                store as 'Adresse 2' weight 3;

                start when p=4 and @code
                stop after @code set p=5
                store as 'Code' weight 3;

                start when p=5 stop after @$ set p=6
                store as 'Ville' weight 3;
            """
        },
        {
            "min_score": 9,
            "max_score": 9,
            "rules": """
                init p=0;

                once after <<Bénéficiaire \:\$>> set p=1;
                once after p=1 and @$ set p=2;

                start when p=2 stop after @$ set p=3
                store as 'Adresse 1' weight 3;

                start when p=3 and @code
                stop after @code set p=4
                store as 'Code' weight 3;

                start when p=4 stop after @$ set p=5
                store as 'Ville' weight 3;
            """
        }
    ],
    "homeserve": [
        {
            "min_score": 37,
            "max_score": 43,
            "rules": """
                init d=0, n=0;
                force 'Assurance' to 'HomeServe';

                start after <<N°>> and n=0
                stop when @$ set n=1
                store as 'Ref' weight 5;

                start after d=0 and <<Date \: >>
                stop after @date set d=1
                store as 'Date' weight 5;

                start after <<et NOM \: >>
                stop when @$ store as 'Dossier' weight 5;

                start after <<Contrat client \: >>
                stop when @$ store as 'Type' weight 5;

                start after <<Coût de l’intervention>>
                stop when <<\$En cas>>
                store as 'Charges' weight 5;

                start after <<Tél. Domicile \:>>
                stop when @$ store as 'Tél ev' weight 1;

                start after <<Tél. portable \:>>
                stop when @$ store as 'Tél portable' weight 1;

                start after <<Détails \: >>
                stop when @$
                store as 'Observations' weight 1;

                start after <<Adresse \: >>
                stop when @$ store as 'Adresse 1' weight 5;

                start after <<CP \:\$>>
                stop when @$ store as 'Code' weight 5;

                start after <<Ville \: >>
                stop when @$ store as 'Ville' weight 5;
            """
        }
    ]
}