{
    "pdf_main": [
        {
            "min_score" : 41,
            "rules": """
                 init a=0, s=0, d=0, f=0, r=0

                 once after f=0 and <<Fax>> set f=1
                 once after f=1 and <<Fax>> set f=2

                 start after f=2 and <<\$>>
                 stop when <<\$>> set f=3
                 store as 'Assurance' weight 5

                
            """
        }
    ]
}