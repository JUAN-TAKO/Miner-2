regexes = {
    "ref": "([0-9]{8}P[0-9] | [0-9]{10}P[0-9])",
    "date": "[0-9]{2}/[0-9]{2}/[0-9]{4}"
}

rules = {
    "pdf_main": [
        {
            "min_score" : 41,
            "max_score" : 50,
            "rules": """
                init a=0, s=0, d=0, f=0, r=0;

                once after f=0 and <<Fax>> set f=1;
                once after f=1 and <<Fax>> set f=2;

                start after f=2 and <<$>>
                stop when <<$>> set f=3
                store as 'Assurance' weight 5;

                start when r=0 and @ref
                stop after @ref set r=1
                store as 'Ref' weight 5;

                start when d=0 and @date
                stop after @date set d=1
                store as 'Date1' weight 5

                start when d=1 and @date
                stop after @date set d=2
                store as 'Date2' weight 5;

                start when <<Dossier$:$>>
                stop when <<$>>
                store as 'Dossier' weight 5;

                start when <<intervention suivante :$>>
                stop when <<$>>
                store as 'Type' weight 5;

                start when <<Nature du sinistre:>>
                stop when <<$>>
                store as 'Nature' weight 1;

                start when d=2 and <<$>>
                stop when <<Sociétaire>> set d=3
                store as 'Charges' weight 5;

                start when d=3 and <<$>>
                stop when <<$>>
                store as 'Type' weight 5;
            """
        }
    ]
}