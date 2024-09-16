import mysql.connector
deletedCompanyNames=["BHL" , "MNP"]
companyNames = [  'AB' ,'AL', 'ALKM', 'ARTES', 'ASSAD', 'AST', 'ATB', 'ATL', 'BH', 'BIAT', 'BNA', 'BS', 'BT', 'BTEI', 'CC', 'CIL', 'GIF', 'ICF', 'LSTR', 'MGR', 'NAKL', 'PLTU', 'POULA', 'SCB', 'SERVI', 'SFBT', 'SIAM', 'SIMP', 'SIPHA', 'SITS', 'SMG', 'SOKNA', 'SOMOC', 'SOPAT', 'SOTE', 'SPDI', 'STAR', 'STB', 'STPIL', 'TAIR', 'TINV', 'TJL', 'TLNET', 'TLS', 'TPR', 'TRE', 'UBCI', 'UIB', 'WIFAK', 'STVR', 'AMS', 'BHASS', 'AETEC', 'LNDOR', 'NBL', 'OTH', 'STPAP', 'SOTEM', 'SAH', 'HANL', 'CELL', 'CITY', 'ECYCL', 'MPBS', 'BL', 'DH', 'MIP', 'TGH', 'UADH', 'PLAST', 'UMED', 'SMD', 'SAMAA', 'ASSMA']
updateNames=["updatestock","updatenews"]
allTableNames = [ 'USDTND' , "AL" , 'AB' ,'AL', 'ALKM', 'ARTES', 'ASSAD', 'AST', 'ATB', 'ATL', 'BH', 'BIAT', 'BNA', 'BS', 'BT', 'BTEI', 'CC', 'CIL', 'GIF', 'ICF', 'LSTR', 'MGR', 'BHL', 'MNP', 'NAKL', 'PLTU', 'POULA', 'SCB', 'SERVI', 'SFBT', 'SIAM', 'SIMP', 'SIPHA', 'SITS', 'SMG', 'SOKNA', 'SOMOC', 'SOPAT', 'SOTE', 'SPDI', 'STAR', 'STB', 'STPIL', 'TAIR', 'TINV', 'TJL', 'TLNET', 'TLS', 'TPR', 'TRE', 'UBCI', 'UIB', 'WIFAK', 'STVR', 'AMS', 'BHASS', 'AETEC', 'LNDOR', 'NBL', 'OTH', 'STPAP', 'SOTEM', 'SAH', 'HANL', 'CELL', 'CITY', 'ECYCL', 'MPBS', 'BL', 'DH', 'MIP', 'TGH', 'UADH', 'PLAST', 'UMED', 'SMD', 'SAMAA', 'ASSMA']
EPOCHS_TRAIN = 100
EPOCHS_ALL = 2

factors = {
    "Attente de résultat": [
        "attente gains",
        "attente resultats",
        "attente performance",
        "annonce résultats financiers",
        "prévisions bénéfices",
        "publication chiffre d'affaires",
        "annonce résultats trimestriels",
        "attente des résultats annuels",
        "prévisions des analystes",
        "consensus des analystes",
        "publication des résultats",
        "attente des chiffres de ventes",
        "attente des chiffres de revenus",
        "attente de la publication des données économiques",
        "attente de la présentation des résultats",
        "attente des données de l'entreprise",
        "attente des indicateurs économiques"
    ],

    "Changements au sein de l'équipe de direction": [
        "changement directeur général",
        "nouveau PDG",
        "départ directeur financier",
        "nouveau directeur des opérations",
        "nomination d'un nouveau directeur technique",
        "changement de président",
        "nouveau responsable marketing",
        "nouveau membre du conseil d'administration",
        "remaniement de l'équipe de direction",
        "démission d'un cadre dirigeant",
        "nouvelle nomination au sein de la direction",
        "arrivée d'un nouveau dirigeant",
        "départ d'un membre du conseil d'administration",
        "démission du PDG",
        "changement de management",
        "réorganisation de l'équipe dirigeante",
        "nouvelle structure de direction"
    ],
    "brevets": [
        "diplome",
        "brevet obtenu",
        "brevet depose",
        "brevet innovation",
        "brevet invention",
        "brevet technologie",
        "brevet premier_plan",
        "Propriété intellectuelle",
        "Dépôt de brevet",
        "Brevet de perfectionnement",
        "Brevet logiciel",
        "Brevet de modèle d'utilité",
        "Protection de la propriété intellectuelle",
        "Enregistrement de brevet",
        "Brevet en instance",
        "Brevet litigieux",
        "Brevet valide",
        "Brevet expiré",
        "Licence de brevet",
        "Brevet international",
        "Brevet délivré",
        "Brevet déposé"
        "Nous avons déposé un brevet pour notre invention révolutionnaire",
        "Nous sommes fiers d'annoncer que nous avons obtenu une protection juridique pour notre innovation",
        "Notre entreprise a obtenu un brevet pour notre technologie de pointe",
        "Nous avons récemment déposé un brevet pour notre produit phare",
        "Notre entreprise a obtenu un brevet pour notre invention révolutionnaire qui va changer l'industrie",
        "Nous sommes ravis d'annoncer que nous avons obtenu un brevet pour notre nouvelle technologie",
        "La société a déposé des brevets pour ses innovations technologiques",
        "Il y a une forte demande pour les brevets de cette société",
        "La société a obtenu des brevets pour ses inventions",
        "L'entreprise possède des brevets exclusifs sur ses produits",
        "La recherche et développement de la société est protégée par des brevets",
        "Notre entreprise a des innovations protégées par des patents",
        "Notre entreprise a obtenu des droits exclusifs pour certaines technologies",
        "Nous avons des produits uniques qui ne peuvent être copiés",
        "Nous avons des technologies protégées par des droits de propriété intellectuelle",
    ],

    "Actifs immobiliers": [
        "acquisition bien immobilier",
        "investissement bien immobilier",
        "nouveau_bien portefeuille",
        "acquisition strategique",
        "investissement avenir",
        "achat_nouveau bien",
        "Nous avons récemment acheté un bien immobilier pour élargir notre portefeuille",
        "Notre entreprise vient de faire un important investissement dans un bien immobilier",
        "Nous sommes heureux d'annoncer l'acquisition d'un nouveau bien immobilier",
        "Notre entreprise vient de faire un investissement stratégique dans un bien immobilier",
        "Nous avons récemment acheté un bien immobilier pour renforcer notre position sur le marché",
        "Les actifs immobiliers de la société ont augmenté de manière significative ces dernières années",
        "Évaluation d'actifs immobiliers",
        "La société a une grande quantité de terrains et de bâtiments",
        "L'entreprise possède des immeubles locatifs dans plusieurs villes",
        "Il y a beaucoup d'opportunités d'investissement dans l'immobilier",
        "Il existe une grande variété d'options d'investissement immobilier, des appartements aux terrains",
    ],
    "Ventes exclusives": [
        "contrat vente exclusif",
        "nouveau client",
        "partenaire strategique",
        "contrat long terme",
        "acteur majeur marche",
        "position avenir",
        "propose des offres exclusives pour ses clients fidèles",
        "Nous avons des ventes exclusives pour nos membres VIP",
        "Notre entreprise a signé un accord de vente exclusive avec un fournisseur de renom",
        "Nos produits sont uniquement disponibles chez nous",
        "Nous avons des offres qui ne peuvent être trouvées nulle part ailleurs",
        "Notre entreprise est le seul distributeur de ces produits dans la région",
        "Nous avons un partenariat exclusif avec un fabricant pour proposer ces produits",
        "Notre entreprise est le seul endroit où vous pouvez acheter cette marque",
        "Nous avons des produits en édition limitée qui ne sont pas disponibles ailleurs",
        "Notre entreprise a obtenu les droits exclusifs de distribution pour ces produits"
    ],
    "La position de l'entreprise sur le marché": [
        "leader marche",
        "acteur majeur",
        "reconnu leader",
        "reconnu acteur majeur",
        "nomme leader",
        "nomme acteur majeur",
        "Notre entreprise est un leader dans son secteur",
        "Nous avons une forte part de marché",
        "Notre entreprise est bien positionnée pour croître dans ce marché",
        "Nous sommes considérés comme l'un des principaux acteurs de notre industrie",
        "Notre entreprise est reconnue pour son expertise dans son domaine",
        "Nous avons une bonne réputation dans notre marché cible",
        "Notre entreprise a une présence importante dans son secteur d'activité"

    ],
    "cours de devises": [
        "hausse valeur devise_dollar",
        "hausse valeur devise_euro",
        "hausse valeur devise_yen",
        "appreciation devise_livre",
        "hausse valeur devise_franc",
        "hausse valeur devise_dollar_canadien",
        "Le taux de change entre les deux monnaies a évolué",
        "Le taux de change entre les deux monnaies est en constante fluctuation",
        "Il y a une fluctuation sur le marché des devises",
        "Il y a une variation sur les taux de change entre les monnaies",
        "Le marché des devises est en constante évolution",
        "Le taux de change entre ces monnaies est sujet à des fluctuations",
        "Il y a une volatilité sur les taux de change"
    ],
    "Signature d'un nouveau contrat": [
        "signent une convention de partenariat",
        "annonce son partenariat avec",
        "partenariat",
        "annonce son partenariat",
        "nouveau contrat grand client",
        "nouveau contrat acteur_majeur",
        "nouveau contrat partenaire_strategique",
        "nouveau contrat long terme",
        "nouveau contrat acteur majeur industrie",
        "nouveau contrat position avenir"
        "Notre entreprise a conclu un accord avec un nouveau partenaire",
        "Nous avons finalisé les termes d'un accord avec un autre acteur du marché",
        "Notre entreprise a réussi à nouer une nouvelle relation commerciale",
        "Nous avons mis en place un partenariat avec une autre entreprise",
        "Notre entreprise a signé un protocole d'accord avec un partenaire stratégique",
        "Nous avons réussi à finaliser un contrat avec un client important",
        "Notre entreprise a signé un nouvel accord de distribution"
    ],
    "Acquisition ou fusion avec une autre entreprise": [
        "acquisition renforcement position",
        "fusion strategique portefeuille produits",
        "acquisition leader industrie",
        "fusion elargissement portee",
        "achat renforcement_position",
        "acquisition strategique leader_industrie",
        "Notre entreprise a étendu son portefeuille en intégrant une nouvelle société",
        "Nous avons renforcé notre présence sur le marché en fusionnant avec une autre entreprise",
        "Notre entreprise a étendu sa gamme de produits en intégrant une société complémentaire",
        "Nous avons renforcé notre position concurrentielle en fusionnant avec une entreprise leader dans son secteur",
        "Notre entreprise a étendu son marché en rachetant une société cible",
        "Nous avons consolidé notre position en intégrant une entreprise complémentaire",
        "Notre entreprise a élargi son activité en fusionnant avec une autre entreprise",
        "fusion d'entreprise",
        "acquisition d'entreprise",
        "rachat d'entreprise",
        "alliance stratégique",
        "cession d'actifs",
        "opération de croissance externe",
        "La société a annoncé une fusion avec une autre entreprise",
        "La société a acquis une entreprise concurrente",
        "La société a procédé au rachat d'une entreprise spécialisée dans un domaine complémentaire",
        "La société a annoncé la conclusion d'une alliance stratégique avec une entreprise partenaire",
        "La société a cédé certains de ses actifs pour se concentrer sur son coeur de métier",
        "La société a poursuivi une stratégie de croissance externe en multipliant les acquisitions ces dernières années"

    ]

}
def connectdb():
    # Connect to the MySQL database
    cnx = mysql.connector.connect(host='localhost', user='root', password='root123',
                                  database='pcd')
    cursor = cnx.cursor()
    return cnx , cursor

def commitdb(cnx , cursor):
    # Commit the changes and close the connection
    cnx.commit()
    cursor.close()
    cnx.close()