# -*- coding: utf-8 -*-
"""
MemoZik - Build Data & MIDI Extractor Script
Génère le catalogue musical tracks.js à partir des fichiers MIDI locaux.
Extrait les métadonnées, anecdotes culturelles, distracteurs QCM et séquences de notes audio.
"""

import os
import json
import base64
import struct

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIDI_DIR = os.path.join(BASE_DIR, "midi")
OUTPUT_JS = os.path.join(BASE_DIR, "tracks.js")

TRACK_DEFINITIONS = [
    # ==========================================
    # CLASSIQUE & BAROQUE (25 morceaux)
    # ==========================================
    {
        "id": "beethoven_furelise",
        "file": "beethoven_furelise.mid",
        "title": "Lettre à Élise (Für Elise)",
        "composer": "Ludwig van Beethoven",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme (1810)",
        "genre": "Bagatelle pour piano solo en la mineur (WoO 59)",
        "year": 1810,
        "country": "Allemagne / Autriche",
        "instrumentation": "Piano solo",
        "clue": "Bagatelle pour piano composée en 1810, l'une des mélodies les plus célèbres du monde.",
        "funFact": "Composée en 1810, cette pièce n'a été découverte et publiée qu'en 1867, quarante ans après la mort de Beethoven. L'identité exacte d'« Élise » reste un mystère : certains historiens pensent qu'il s'agissait en réalité de Thérèse Malfatti, dont Beethoven était épris, et que le transcripteur Ludwig Nohl aurait mal lu son écriture manuscrite chaotique !",
        "distractors": [
            {"composer": "Wolfgang Amadeus Mozart", "title": "Sonate facile n°16 en do majeur"},
            {"composer": "Frédéric Chopin", "title": "Nocturne op. 9 n°2 en mi bémol majeur"},
            {"composer": "Franz Schubert", "title": "Impromptu op. 90 n°4"}
        ]
    },
    {
        "id": "beethoven_symph5",
        "file": "beethoven_symph5.mid",
        "title": "Symphonie n°5 (1er mouvement - Allegro con brio)",
        "composer": "Ludwig van Beethoven",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Classicisme viennois / Romantisme (1808)",
        "genre": "Symphonie orchestrale en ut mineur (op. 67)",
        "year": 1808,
        "country": "Allemagne / Autriche",
        "instrumentation": "Grand orchestre symphonique",
        "clue": "Le célèbre motif rythmique à quatre notes 'pom-pom-pom-pom' symbolisant le destin qui frappe à la porte.",
        "funFact": "Les quatre notes initiales (trois brèves, une longue) forment le motif le plus célèbre de toute la musique occidentale. Pendant la Seconde Guerre mondiale, la BBC utilisait ce motif comme indicatif radio car en morse, trois points et un trait (...-) correspondent à la lettre 'V', symbole de la Victoire !",
        "distractors": [
            {"composer": "Johannes Brahms", "title": "Symphonie n°1 en ut mineur"},
            {"composer": "Piotr Ilitch Tchaïkovski", "title": "Symphonie n°5 en mi mineur"},
            {"composer": "Gustav Mahler", "title": "Symphonie n°1 'Titan'"}
        ]
    },
    {
        "id": "beethoven_ode_joy",
        "file": "beethoven_ode_joy.mid",
        "title": "Ode à la joie (Symphonie n°9)",
        "composer": "Ludwig van Beethoven",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme (1824)",
        "genre": "Symphonie chorale en ré mineur (op. 125)",
        "year": 1824,
        "country": "Allemagne / Autriche",
        "instrumentation": "Orchestre symphonique et chœur",
        "clue": "Hymne officiel de l'Union européenne, composé sur un poème de Friedrich von Schiller.",
        "funFact": "Lors de la création triomphale à Vienne en 1824, Beethoven était déjà totalement sourd. Placé dos au public, il dut être tourné par la cantatrice Caroline Unger pour voir la salle debout qui l'acclamait à tout rompre avec mouchoirs et chapeaux en l'air !",
        "distractors": [
            {"composer": "Wolfgang Amadeus Mozart", "title": "Requiem (Lacrimosa)"},
            {"composer": "Georg Friedrich Händel", "title": "Messie (Hallelujah)"},
            {"composer": "Giuseppe Verdi", "title": "Aida (Marche triomphale)"}
        ]
    },
    {
        "id": "beethoven_moonlight",
        "file": "beethoven_moonlight.mid",
        "title": "Sonate au clair de lune (Sonate quasi una fantasia op. 27 n°2)",
        "composer": "Ludwig van Beethoven",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Classicisme / Romantisme (1801)",
        "genre": "Sonate pour piano en do dièse mineur",
        "year": 1801,
        "country": "Allemagne / Autriche",
        "instrumentation": "Piano solo",
        "clue": "Sonate nocturne et tourmentée dédiée à sa jeune élève la comtesse Giulietta Guicciardi.",
        "funFact": "Le titre poétique 'Au clair de lune' n'a pas été donné par Beethoven ! C'est le critique musical et poète Heinrich Rellstab qui, cinq ans après la mort du compositeur, compara le 1er mouvement à une barque glissant sur le lac des Quatre-Cantons sous la lune.",
        "distractors": [
            {"composer": "Claude Debussy", "title": "Clair de lune"},
            {"composer": "Frédéric Chopin", "title": "Nocturne en do dièse mineur"},
            {"composer": "Robert Schumann", "title": "Scènes d'enfants (Rêverie)"}
        ]
    },
    {
        "id": "mozart_turca",
        "file": "mozart_turca.mid",
        "title": "Marche turque (Rondo Alla Turca)",
        "composer": "Wolfgang Amadeus Mozart",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Classicisme (1783)",
        "genre": "Sonate pour piano n°11 en la majeur (K. 331)",
        "year": 1783,
        "country": "Autriche",
        "instrumentation": "Piano solo",
        "clue": "Mouvement final virevoltant imitant le son des fanfares de janissaires ottomans.",
        "funFact": "Au XVIIIe siècle, la mode à Vienne était aux 'turqueries' militaires. Pour imiter le fracas des cymbales, triangles et grosses caisses des janissaires ottomans, certains pianos de l'époque possédaient une pédale spéciale dite 'pédale turque' qui frappait une clochette ou le dessous de la table d'harmonie !",
        "distractors": [
            {"composer": "Ludwig van Beethoven", "title": "La Ruine d'Athènes (Marche turque)"},
            {"composer": "Joseph Haydn", "title": "Symphonie n°100 'Militaire'"},
            {"composer": "Gioachino Rossini", "title": "L'Italienne à Alger"}
        ]
    },
    {
        "id": "mozart_sym40",
        "file": "mozart_sym40.mid",
        "title": "Symphonie n°40 en sol mineur (1er mouvement - Molto allegro)",
        "composer": "Wolfgang Amadeus Mozart",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Classicisme (1788)",
        "genre": "Symphonie en sol mineur (K. 550)",
        "year": 1788,
        "country": "Autriche",
        "instrumentation": "Orchestre classique",
        "clue": "L'une des deux seules symphonies écrites par Mozart en mode mineur, d'une intensité dramatique poignante.",
        "funFact": "Mozart a composé ses trois plus grandes symphonies (les 39, 40 et 41 'Jupiter') en un éclair de génie absolu durant l'été 1788, en moins de six semaines seulement, sans que l'on sache avec certitude si elles furent jouées de son vivant !",
        "distractors": [
            {"composer": "Joseph Haydn", "title": "Symphonie n°94 'La Surprise'"},
            {"composer": "Franz Schubert", "title": "Symphonie n°8 'Inachevée'"},
            {"composer": "Felix Mendelssohn", "title": "Symphonie n°4 'Italienne'"}
        ]
    },
    {
        "id": "bach_toccata",
        "file": "bach_toccata.mid",
        "title": "Toccata et Fugue en ré mineur (BWV 565)",
        "composer": "Johann Sebastian Bach",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Baroque (vers 1704)",
        "genre": "Pièce pour orgue à tuyaux",
        "year": 1704,
        "country": "Allemagne",
        "instrumentation": "Grand orgue",
        "clue": "L'ouverture monumentale pour orgue la plus dramatique de l'histoire, souvent associée au cinéma d'épouvante.",
        "funFact": "Bach avait à peine 20 ans lorsqu'il l'aurait composée pour tester la puissance et la réactivité des tuyaux d'orgue d'Arnstadt. Elle est devenue l'emblème des films d'angoisse et du cinéma gothique depuis son apparition mémorable dans Fantasia de Walt Disney (1940) et Docteur Jekyll et M. Hyde (1931).",
        "distractors": [
            {"composer": "Georg Friedrich Händel", "title": "Concerto pour orgue en fa majeur"},
            {"composer": "Dietrich Buxtehude", "title": "Passacaille en ré mineur"},
            {"composer": "Henry Purcell", "title": "Music for the Funeral of Queen Mary"}
        ]
    },
    {
        "id": "bach_prelude",
        "file": "bach_prelude.mid",
        "title": "Prélude n°1 en do majeur (Le Clavier bien tempéré, Livre I)",
        "composer": "Johann Sebastian Bach",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Baroque (1722)",
        "genre": "Prélude en arpèges au clavier (BWV 846)",
        "year": 1722,
        "country": "Allemagne",
        "instrumentation": "Clavecin / Piano",
        "clue": "Une suite limpide d'arpèges ascendants qui a servi de base à l'Ave Maria de Gounod.",
        "funFact": "Plus d'un siècle après sa création, le compositeur français Charles Gounod improvisa sur ce prélude de Bach une ligne mélodique vocale restée célèbre dans le monde entier : l'Ave Maria de Gounod !",
        "distractors": [
            {"composer": "François Couperin", "title": "Les Barricades mystérieuses"},
            {"composer": "Domenico Scarlatti", "title": "Sonate en ré mineur K. 141"},
            {"composer": "Jean-Philippe Rameau", "title": "Le Rappel des Oiseaux"}
        ]
    },
    {
        "id": "vivaldi_winter",
        "file": "vivaldi_winter.mid",
        "title": "Les Quatre Saisons : L'Hiver (L'Inverno - 1er mouvement)",
        "composer": "Antonio Vivaldi",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Baroque (1725)",
        "genre": "Concerto pour violon en fa mineur (RV 297)",
        "year": 1725,
        "country": "Italie",
        "instrumentation": "Violon solo et orchestre à cordes",
        "clue": "Le violoniste roux vénitien décrit ici le claquement de dents, le vent glacial et le piétinement sur la neige.",
        "funFact": "Vivaldi avait lui-même rédigé des sonnets explicatifs gravés sur les partitions : ce premier mouvement décrit précisément 'trembler de froid dans la neige gelée, courir et trépigner des pieds à chaque instant, et par la violence du gel claquer des dents' !",
        "distractors": [
            {"composer": "Arcangelo Corelli", "title": "Concerto grosso 'Pour la nuit de Noël'"},
            {"composer": "Tomaso Albinoni", "title": "Adagio en sol mineur"},
            {"composer": "Giuseppe Tartini", "title": "Le Trille du Diable"}
        ]
    },
    {
        "id": "chopin_minute_waltz",
        "file": "chopin_minute_waltz.mid",
        "title": "Valse minute (Valse du petit chien op. 64 n°1)",
        "composer": "Frédéric Chopin",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme (1847)",
        "genre": "Valse brillante pour piano en ré bémol majeur",
        "year": 1847,
        "country": "Pologne / France",
        "instrumentation": "Piano solo",
        "clue": "Valse tournoyante et fulgurante inspirée par un chien courant après sa propre queue.",
        "funFact": "Contrairement à une idée reçue, 'minute' ne signifie pas qu'elle doit être jouée en 60 secondes (ce qui serait un massacre musical !), mais 'minuscule / petite valse' en français. George Sand l'appelait affectueusement 'La valse du petit chien' car elle fut inspirée par son chiot Marquis tournant en rond pour attraper sa queue !",
        "distractors": [
            {"composer": "Franz Liszt", "title": "Valse de Méphisto"},
            {"composer": "Johannes Brahms", "title": "Valse op. 39 n°15"},
            {"composer": "Piotr Ilitch Tchaïkovski", "title": "Valse des fleurs"}
        ]
    },
    {
        "id": "chopin_revolutionary",
        "file": "chopin_revolutionary.mid",
        "title": "Étude révolutionnaire (op. 10 n°12 en do mineur)",
        "composer": "Frédéric Chopin",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme (1831)",
        "genre": "Étude pour piano solo",
        "year": 1831,
        "country": "Pologne / France",
        "instrumentation": "Piano solo",
        "clue": "Cascades passionnées à la main gauche nées du désespoir lors de la chute de Varsovie face à l'armée russe.",
        "funFact": "Chopin composa cette œuvre furieuse à Stuttgart en apprenant que Varsovie venait d'être écrasée par les troupes du Tsar russe lors de l'insurrection de novembre 1830. Rongé par la culpabilité d'être loin de ses compatriotes, il déversa sa rage dans des cascades épiques de la main gauche.",
        "distractors": [
            {"composer": "Franz Liszt", "title": "Étude d'exécution transcendante n°4 'Mazeppa'"},
            {"composer": "Sergueï Rachmaninov", "title": "Prélude en do dièse mineur"},
            {"composer": "Alexandre Scriabine", "title": "Étude op. 8 n°12"}
        ]
    },
    {
        "id": "tchaikovsky_1812",
        "file": "tchaikovsky_1812.mid",
        "title": "Ouverture 1812 (Ouverture solennelle op. 49)",
        "composer": "Piotr Ilitch Tchaïkovski",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme russe (1880)",
        "genre": "Ouverture orchestrale héroïque",
        "year": 1880,
        "country": "Russie",
        "instrumentation": "Orchestre symphonique, cloches et canons réels",
        "clue": "Œuvre spectaculaire commémorant la victoire russe sur Napoléon, intégrant de véritables coups de canon !",
        "funFact": "Pour recréer la bataille de la Moskova, la partition originale de Tchaïkovski prévoit de véritables tirs de canon d'artillerie coordonnés par détonateurs électriques ainsi que des volées de cloches d'églises en tutti !",
        "distractors": [
            {"composer": "Modeste Moussorgski", "title": "La Grande Porte de Kiev"},
            {"composer": "Alexandre Borodine", "title": "Dans les steppes de l'Asie centrale"},
            {"composer": "Nikolaï Rimski-Korsakov", "title": "La Grande Pâque russe"}
        ]
    },
    {
        "id": "tchaikovsky_nutcracker",
        "file": "tchaikovsky_nutcracker.mid",
        "title": "Casse-Noisette (Ouverture miniature)",
        "composer": "Piotr Ilitch Tchaïkovski",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme russe (1892)",
        "genre": "Ballet féerique (op. 71)",
        "year": 1892,
        "country": "Russie",
        "instrumentation": "Orchestre symphonique sans violoncelles ni contrebasses",
        "clue": "Ballet de Noël emblématique racontant l'aventure enchantée de Clara et du prince Casse-Noisette.",
        "funFact": "Pour son ballet Casse-Noisette, Tchaïkovski fit importer en grand secret de Paris un instrument tout juste inventé par Auguste Mustel : le céleste. Il voulait à tout prix surprendre ses rivaux russes Rimski-Korsakov et Glazounov avant qu'ils ne découvrent sa sonorité de clochettes cristallines !",
        "distractors": [
            {"composer": "Léo Delibes", "title": "Coppélia (Prélude et Mazurka)"},
            {"composer": "Sergueï Prokofiev", "title": "Cendrillon"},
            {"composer": "Igor Stravinsky", "title": "Petrouchka"}
        ]
    },
    {
        "id": "ravel_bolero",
        "file": "ravel_bolero.mid",
        "title": "Boléro",
        "composer": "Maurice Ravel",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Modernisme / Impressionnisme français (1928)",
        "genre": "Ballet orchestral en un crescendo continu",
        "year": 1928,
        "country": "France",
        "instrumentation": "Orchestre symphonique et caisse claire obstinée",
        "clue": "Une œuvre hypnotique construite sur un crescendo orchestral ininterrompu de 15 minutes sur le même rythme de caisse claire.",
        "funFact": "Ravel lui-même décrivait avec ironie son Boléro comme 'un morceau d'orchestre sans musique, un crescendo continu d'une durée d'un quart d'heure sur un seul thème sans aucun développement' ! Lors de la première, une spectatrice cria au scandale 'Au fou ! Au fou !', ce à quoi Ravel répondit avec un sourire amusé : 'Celle-là, elle a compris !'",
        "distractors": [
            {"composer": "Claude Debussy", "title": "La Mer (Dialogue du vent et de la mer)"},
            {"composer": "Manuel de Falla", "title": "L'Amour sorcier (Danse rituelle du feu)"},
            {"composer": "Gabriel Fauré", "title": "Pavane op. 50"}
        ]
    },
    {
        "id": "debussy_clairdelune",
        "file": "debussy_clairdelune.mid",
        "title": "Clair de lune (Suite bergamasque n°3)",
        "composer": "Claude Debussy",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Impressionnisme français (1890)",
        "genre": "Pièce pour piano solo inspirée de Paul Verlaine",
        "year": 1890,
        "country": "France",
        "instrumentation": "Piano solo",
        "clue": "Poème pianistique délicat et vaporeux inspiré du recueil 'Fêtes galantes' de Verlaine.",
        "funFact": "Initialement, Debussy avait titré cette pièce 'Promenade sentimentale'. C'est le sublime poème de Paul Verlaine commençant par 'Votre âme est un paysage choisi / Que vont charmant masques et bergamasques...' qui lui donna son titre définitif et immortel.",
        "distractors": [
            {"composer": "Maurice Ravel", "title": "Pavane pour une infante défunte"},
            {"composer": "Erik Satie", "title": "Gymnopédie n°1"},
            {"composer": "Gabriel Fauré", "title": "Clair de lune (Mélodie op. 46)"}
        ]
    },
    {
        "id": "debussy_arabesque",
        "file": "debussy_arabesque.mid",
        "title": "Première Arabesque (Deux Arabesques L. 66)",
        "composer": "Claude Debussy",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Impressionnisme / Art Nouveau (1888)",
        "genre": "Arabesque pour piano solo en mi majeur",
        "year": 1888,
        "country": "France",
        "instrumentation": "Piano solo",
        "clue": "Ondulations fluides et élégantes rappelant les motifs floraux de l'Art Nouveau naissant.",
        "funFact": "Debussy composa cette pièce alors qu'il n'avait que 26 ans. Inspiré par les courbes végétales de l'Art nouveau, il voulait traduire en notes la fluidité du dessin : la polyrythmie entre deux notes à la main droite contre trois à la main gauche crée cette sensation magique de vagues ondulantes.",
        "distractors": [
            {"composer": "Frédéric Chopin", "title": "Fantaisie-Impromptu op. 66"},
            {"composer": "Robert Schumann", "title": "Arabesque en do majeur op. 18"},
            {"composer": "Franz Liszt", "title": "Consolation n°3 en ré bémol majeur"}
        ]
    },
    {
        "id": "rossini_williamtell",
        "file": "rossini_williamtell.mid",
        "title": "Guillaume Tell (Ouverture - Galop final)",
        "composer": "Gioachino Rossini",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Bel Canto romantique (1829)",
        "genre": "Ouverture d'opéra (Galop héroïque)",
        "year": 1829,
        "country": "Italie / France",
        "instrumentation": "Orchestre d'opéra avec trompettes et cors héroïques",
        "clue": "La chevauchée triomphante de trompettes la plus célèbre du monde, immortalisée par The Lone Ranger.",
        "funFact": "Après avoir composé ce chef-d'œuvre à l'âge de 37 ans seulement, Rossini prit sa retraite de l'opéra et n'écrivit plus aucun opéra pendant les 40 années restantes de sa vie, préférant se consacrer à la gastronomie et aux réceptions parisiennes !",
        "distractors": [
            {"composer": "Giuseppe Verdi", "title": "Nabucco (Ouverture)"},
            {"composer": "Jacques Offenbach", "title": "La Belle Hélène (Ouverture)"},
            {"composer": "Franz von Suppé", "title": "Cavalerie légère"}
        ]
    },
    {
        "id": "rossini_barber",
        "file": "rossini_barber.mid",
        "title": "Le Barbier de Séville (Ouverture)",
        "composer": "Gioachino Rossini",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Opéra-bouffe italien (1816)",
        "genre": "Ouverture d'opéra-bouffe",
        "year": 1816,
        "country": "Italie",
        "instrumentation": "Orchestre d'opéra",
        "clue": "Ouverture joyeuse et pétillante mettant en vedette le célèbre crescendo rossinien et le rusé Figaro.",
        "funFact": "Incroyable mais vrai : Rossini a composé la totalité de son chef-d'œuvre Le Barbier de Séville en seulement 13 jours ! La légende raconte que lorsqu'on demandait à Donizetti si Rossini avait vraiment pu écrire un opéra en treize jours, Donizetti répondait : 'C'est tout à fait possible, il a toujours été si paresseux !'",
        "distractors": [
            {"composer": "Wolfgang Amadeus Mozart", "title": "Les Noces de Figaro (Ouverture)"},
            {"composer": "Gaetano Donizetti", "title": "Don Pasquale (Ouverture)"},
            {"composer": "Vincenzo Bellini", "title": "Norma (Ouverture)"}
        ]
    },
    {
        "id": "saint_saens_swan",
        "file": "saint_saens_swan.mid",
        "title": "Le Carnaval des animaux : Le Cygne",
        "composer": "Camille Saint-Saëns",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme français (1886)",
        "genre": "Fantaisie zoologique (mouvement n°13)",
        "year": 1886,
        "country": "France",
        "instrumentation": "Violoncelle solo et deux pianos",
        "clue": "Mélodie noble et pure de violoncelle glissant sur des arpèges de piano ondoyants.",
        "funFact": "Craignant pour sa réputation de compositeur sérieux, Saint-Saëns interdit formellement toute publication du Carnaval des animaux de son vivant, jugeant cette fantaisie trop frivole. Il ne fit qu'une seule exception : Le Cygne, qu'il autorisa à publier dès 1887 !",
        "distractors": [
            {"composer": "Gabriel Fauré", "title": "Élégie pour violoncelle op. 24"},
            {"composer": "Jules Massenet", "title": "Méditation de Thaïs"},
            {"composer": "Edward Elgar", "title": "Salut d'amour op. 12"}
        ]
    },
    {
        "id": "saint_saens_dansemacabre",
        "file": "saint_saens_dansemacabre.mid",
        "title": "Danse macabre (op. 40)",
        "composer": "Camille Saint-Saëns",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Poème symphonique (1874)",
        "genre": "Poème symphonique en sol mineur",
        "year": 1874,
        "country": "France",
        "instrumentation": "Violon solo accordé en triton (diabolus in musica) et xylophone",
        "clue": "À minuit sonnant, la Mort accorde son violon dissonant et fait danser les squelettes au clair de lune.",
        "funFact": "Pour imiter le bruit des os de squelettes qui s'entrechoquent dans la nuit, Saint-Saëns utilise pour la première fois de l'histoire un xylophone au sein d'un grand orchestre symphonique classique !",
        "distractors": [
            {"composer": "Hector Berlioz", "title": "Symphonie fantastique (Songe d'une nuit de sabbat)"},
            {"composer": "Modeste Moussorgski", "title": "Une nuit sur le mont Chauve"},
            {"composer": "Paul Dukas", "title": "L'Apprenti sorcier"}
        ]
    },
    {
        "id": "saint_saens_aquarium",
        "file": "saint_saens_aquarium.mid",
        "title": "Le Carnaval des animaux : L'Aquarium",
        "composer": "Camille Saint-Saëns",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme français (1886)",
        "genre": "Fantaisie zoologique (mouvement n°7)",
        "year": 1886,
        "country": "France",
        "instrumentation": "Deux pianos, flûte, harmonium et glockenspiel",
        "clue": "Ambiance magique et aquatique de poissons scintillants, rendue célèbre par le Festival de Cannes.",
        "funFact": "Cette musique mystérieuse et scintillante est devenue mondialement célèbre en France car elle a servi pendant des décennies de générique officiel pour la montée des marches du Festival de Cannes !",
        "distractors": [
            {"composer": "Maurice Ravel", "title": "Jeux d'eau"},
            {"composer": "Claude Debussy", "title": "En bateau"},
            {"composer": "Gabriel Fauré", "title": "Sicilienne op. 78"}
        ]
    },
    {
        "id": "satie_gymnopedie",
        "file": "satie_gymnopedie.mid",
        "title": "Première Gymnopédie (Lent et douloureux)",
        "composer": "Erik Satie",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Avant-garde parisienne (1888)",
        "genre": "Pièce pour piano en sol majeur",
        "year": 1888,
        "country": "France",
        "instrumentation": "Piano solo",
        "clue": "Trois temps mélancoliques et épurés composés par le célèbre pianiste excentrique de Montmartre.",
        "funFact": "Satie s'est inspiré des fêtes de la Grèce antique (les Gymnopaedies où de jeunes danseurs dansaient nus). Rejetant les lourdeurs romantiques du XIXe siècle, Satie crée une musique zen, dépouillée et minimaliste avec 70 ans d'avance sur la musique ambient !",
        "distractors": [
            {"composer": "Claude Debussy", "title": "Rêverie"},
            {"composer": "Maurice Ravel", "title": "Menuet sur le nom d'Haydn"},
            {"composer": "Francis Poulenc", "title": "Mouvements perpétuels"}
        ]
    },
    {
        "id": "schubert_avemaria",
        "file": "schubert_avemaria.mid",
        "title": "Ave Maria (Ellens dritter Gesang - D. 839)",
        "composer": "Franz Schubert",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme viennois (1825)",
        "genre": "Lied pour voix et piano",
        "year": 1825,
        "country": "Autriche",
        "instrumentation": "Voix et piano / cordes",
        "clue": "L'une des prières musicales les plus émouvantes et universellement chantées au monde.",
        "funFact": "À l'origine, cette pièce n'était pas du tout destinée à la liturgie catholique ! Schubert avait mis en musique un poème de l'écrivain écossais Walter Scott tiré de 'La Dame du lac', où le personnage d'Ellen Douglas chante une prière à la Vierge Marie dans une grotte des Highlands.",
        "distractors": [
            {"composer": "Charles Gounod & J.S. Bach", "title": "Ave Maria"},
            {"composer": "César Franck", "title": "Panis Angelicus"},
            {"composer": "Gabriel Fauré", "title": "Cantique de Jean Racine"}
        ]
    },
    {
        "id": "rimsky_bumblebee",
        "file": "rimsky_bumblebee.mid",
        "title": "Le Vol du bourdon",
        "composer": "Nikolaï Rimski-Korsakov",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme russe (1900)",
        "genre": "Intermède orchestral de l'opéra 'Le Conte du tsar Saltan'",
        "year": 1900,
        "country": "Russie",
        "instrumentation": "Orchestre symphonique / soliste virtuose",
        "clue": "Frénésie de doubles-croches chromatiques imitant le vol en zigzag d'un insecte vrombissant.",
        "funFact": "Dans l'opéra, le prince Gvidon est transformé en bourdon par le cygne magique pour traverser la mer et piquer sa tante maléfique ! Cette pièce est devenue l'épreuve reine de vitesse pour les musiciens du monde entier (violon, piano, guitare, flûte et même tuba).",
        "distractors": [
            {"composer": "Niccolò Paganini", "title": "Moto Perpetuo op. 11"},
            {"composer": "Pablo de Sarasate", "title": "Zapateado"},
            {"composer": "Vittorio Monti", "title": "Czardas"}
        ]
    },
    {
        "id": "brahms_hungarian",
        "file": "brahms_hungarian.mid",
        "title": "Danse hongroise n°1 en sol mineur (Allegro molto)",
        "composer": "Johannes Brahms",
        "category": "classical",
        "categoryLabel": "🎻 Musique Classique & Baroque",
        "era": "Romantisme (1869)",
        "genre": "Danse tsigane hongroise (Csárdás)",
        "year": 1869,
        "country": "Allemagne / Hongrie",
        "instrumentation": "Piano à quatre mains / Orchestre symphonique",
        "clue": "Rythmes tsiganes fougueux alternant mélancolie poignante et accélérations endiablées.",
        "funFact": "Brahms tomba amoureux de la musique folklorique tsigane lors d'une tournée de concerts avec le violoniste virtuose hongrois Eduard Reményi en 1853. Ses 21 danses hongroises furent un tel succès d'édition qu'elles assurèrent la fortune financière de Brahms pour le restant de ses jours !",
        "distractors": [
            {"composer": "Franz Liszt", "title": "Rhapsodie hongroise n°2"},
            {"composer": "Béla Bartók", "title": "Danses populaires roumaines"},
            {"composer": "Antonín Dvořák", "title": "Danse slave op. 46 n°8"}
        ]
    },

    # ==========================================
    # POP, ROCK & CHANSON (25 tubes légendaires)
    # ==========================================
    {
        "id": "queen_bohemian",
        "file": "queen_bohemian.mid",
        "title": "Bohemian Rhapsody",
        "composer": "Queen (Freddie Mercury)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1970 (1975)",
        "genre": "Rock progressif / Opéra-rock",
        "year": 1975,
        "country": "Royaume-Uni",
        "instrumentation": "Piano, guitare électrique, basse, batterie et chœurs opéra",
        "clue": "Morceau d'anthologie sans refrain, passant de la ballade intimiste à un opéra loufoque puis au hard rock déchaîné.",
        "funFact": "La maison de disques EMI refusa initialement de sortir le titre en single, persuadée qu'une chanson de près de 6 minutes ne passerait jamais en radio ! Freddie Mercury confia alors la bande à son ami animateur radio Kenny Everett en lui disant de ne surtout pas la diffuser... Everett la joua 14 fois en un seul week-end, provoquant une hystérie chez les auditeurs !",
        "distractors": [
            {"composer": "Led Zeppelin", "title": "Stairway to Heaven"},
            {"composer": "Pink Floyd", "title": "Wish You Were Here"},
            {"composer": "David Bowie", "title": "Space Oddity"}
        ]
    },
    {
        "id": "queen_killerqueen",
        "file": "queen_killerqueen.mid",
        "title": "Killer Queen",
        "composer": "Queen (Freddie Mercury)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1970 (1974)",
        "genre": "Glam Rock / Pop baroque",
        "year": 1974,
        "country": "Royaume-Uni",
        "instrumentation": "Piano bastringue, harmonies vocales et guitare solo multicanale",
        "clue": "Chanson sophistiquée aux claquements de doigts parlant d'une courtisane haut de gamme friande de Moët & Chandon.",
        "funFact": "C'est le tout premier hit planétaire de Queen qui les propulsa au sommet des charts américains et britanniques. Brian May a enregistré le solo de guitare en superposant quatre couches harmoniques distinctes pour créer un effet de fanfare d'instruments à vent avec sa fameuse guitare Red Special.",
        "distractors": [
            {"composer": "Elton John", "title": "Bennie and the Jets"},
            {"composer": "Roxy Music", "title": "Love Is the Drug"},
            {"composer": "T. Rex", "title": "Get It On"}
        ]
    },
    {
        "id": "beatles_yesterday",
        "file": "beatles_yesterday.mid",
        "title": "Yesterday",
        "composer": "The Beatles (Paul McCartney)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1960 (1965)",
        "genre": "Ballade acoustique pop",
        "year": 1965,
        "country": "Royaume-Uni",
        "instrumentation": "Guitare acoustique et quatuor à cordes",
        "clue": "La chanson la plus reprise de toute l'histoire de la musique avec plus de 2200 versions enregistrées.",
        "funFact": "Paul McCartney a rêvé la mélodie complète dans son sommeil chez sa petite amie Jane Asher ! À son réveil, persuadé qu'il s'agissait inconsciemment d'un vieux morceau de jazz qu'il avait déjà entendu, il composa des paroles temporaires hilarantes : 'Scrambled eggs, Oh, my baby how I love your legs...' avant de trouver 'Yesterday' !",
        "distractors": [
            {"composer": "The Beatles", "title": "Let It Be"},
            {"composer": "Simon & Garfunkel", "title": "The Sound of Silence"},
            {"composer": "Bob Dylan", "title": "Blowin' in the Wind"}
        ]
    },
    {
        "id": "michaeljackson_billiejean",
        "file": "michaeljackson_billiejean.mid",
        "title": "Billie Jean",
        "composer": "Michael Jackson",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1980 (1982)",
        "genre": "Post-disco / Funk pop",
        "year": 1982,
        "country": "États-Unis",
        "instrumentation": "Ligne de basse mythique, boîte à rythme et nappes de synthétiseur",
        "clue": "Ligne de basse de légende et premier Moonwalk télévisé lors des 25 ans du label Motown.",
        "funFact": "Le producteur Quincy Jones détestait initialement la chanson : il trouvait l'intro de basse trop longue et voulait la renommer 'Not My Lover' pour éviter la confusion avec la tenniswoman Billie Jean King ! Michael Jackson insista pied à pied en expliquant que cette longue intro donnait une irrépressible envie de danser. Il avait évidemment raison !",
        "distractors": [
            {"composer": "Prince", "title": "When Doves Cry"},
            {"composer": "Stevie Wonder", "title": "Superstition"},
            {"composer": "Michael Jackson", "title": "Smooth Criminal"}
        ]
    },
    {
        "id": "michaeljackson_beatit",
        "file": "michaeljackson_beatit.mid",
        "title": "Beat It",
        "composer": "Michael Jackson",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1980 (1982)",
        "genre": "Hard rock / Dance rock",
        "year": 1982,
        "country": "États-Unis",
        "instrumentation": "Guitares hard rock saturées, batterie percutante et chant incisif",
        "clue": "Crossover rock légendaire avec le solo de guitare fulgurant d'Eddie Van Halen.",
        "funFact": "Eddie Van Halen a enregistré le solo d'anthologie gratuitement en guise de faveur d'une demi-heure ! Lors de l'enregistrement en studio, le volume et la saturation étaient tellement intenses qu'un haut-parleur du studio a littéralement pris feu !",
        "distractors": [
            {"composer": "Michael Jackson", "title": "Bad"},
            {"composer": "Bon Jovi", "title": "Livin' on a Prayer"},
            {"composer": "Queen", "title": "Another One Bites the Dust"}
        ]
    },
    {
        "id": "abba_dancingqueen",
        "file": "abba_dancingqueen.mid",
        "title": "Dancing Queen",
        "composer": "ABBA",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1970 (1976)",
        "genre": "Europop / Disco",
        "year": 1976,
        "country": "Suède",
        "instrumentation": "Glissando de piano d'ouverture, cordes soyeuses et chœurs scintillants",
        "clue": "Le chef-d'œuvre absolu de la pop disco suédoise, célébrant les jeunes reines du dancefloor de dix-sept ans.",
        "funFact": "Lorsqu'Anni-Frid Lyngstad écouta la maquette instrumentale pour la première fois en studio, elle fondit en larmes d'émotion en disant à Benny Andersson et Björn Ulvaeus : 'C'est la plus belle chanson du monde, elle va être numéro 1 partout !'. Elle est devenue le seul numéro 1 d'ABBA aux États-Unis.",
        "distractors": [
            {"composer": "ABBA", "title": "Mamma Mia"},
            {"composer": "Bee Gees", "title": "Stayin' Alive"},
            {"composer": "Boney M.", "title": "Daddy Cool"}
        ]
    },
    {
        "id": "pinkfloyd_anotherbrick",
        "file": "pinkfloyd_anotherbrick.mid",
        "title": "Another Brick in the Wall (Part 2)",
        "composer": "Pink Floyd (Roger Waters)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1970 (1979)",
        "genre": "Rock progressif / Disco-rock",
        "year": 1979,
        "country": "Royaume-Uni",
        "instrumentation": "Chœur d'enfants d'école, solo de guitare Stratocaster de David Gilmour",
        "clue": "'We don't need no education...' Hymne de rébellion contre l'autoritarisme scolaire avec son chœur d'écoliers.",
        "funFact": "C'est le producteur Bob Ezrin qui a eu l'idée d'introduire un tempo disco four-on-the-floor et de faire enregistrer en secret des élèves de l'école voisine d'Islington Green School à Londres. La chanson fut bannie en Afrique du Sud en 1980 après avoir été adoptée comme chant de ralliement par les lycéens manifestant contre l'Apartheid.",
        "distractors": [
            {"composer": "The Police", "title": "Roxanne"},
            {"composer": "The Who", "title": "Baba O'Riley"},
            {"composer": "Dire Straits", "title": "Sultans of Swing"}
        ]
    },
    {
        "id": "nirvana_smellslike",
        "file": "nirvana_smellslike.mid",
        "title": "Smells Like Teen Spirit",
        "composer": "Nirvana (Kurt Cobain)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1990 (1991)",
        "genre": "Grunge / Rock alternatif",
        "year": 1991,
        "country": "États-Unis",
        "instrumentation": "Dynamique calme/tempête : riff de guitare saturé et batterie féroce de Dave Grohl",
        "clue": "L'hymne de la 'Génération X' qui propulsa le mouvement grunge de Seattle au rang de phénomène planétaire.",
        "funFact": "Le titre vient d'un graffiti que son amie Kathleen Hanna avait tagué sur le mur de la chambre de Kurt Cobain : 'Kurt smells like Teen Spirit'. Cobain croyait que c'était une formule philosophique rebelle sur l'esprit révolutionnaire des adolescents, ignorant totalement que 'Teen Spirit' était simplement une marque de déodorant pour jeunes filles !",
        "distractors": [
            {"composer": "Pearl Jam", "title": "Alive"},
            {"composer": "Soundgarden", "title": "Black Hole Sun"},
            {"composer": "The Smashing Pumpkins", "title": "1979"}
        ]
    },
    {
        "id": "nirvana_comeasyouare",
        "file": "nirvana_comeasyouare.mid",
        "title": "Come As You Are",
        "composer": "Nirvana (Kurt Cobain)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1990 (1991)",
        "genre": "Grunge / Rock alternatif",
        "year": 1991,
        "country": "États-Unis",
        "instrumentation": "Riff de guitare hypnotique avec effet chorus aquatique (Electro-Harmonix Small Clone)",
        "clue": "Riff de guitare sombre et aquatique avec la phrase récurrente 'And I swear that I don't have a gun...'",
        "funFact": "Nirvana hésitait à sortir la chanson en single car le riff de guitare ressemblait énormément à celui de 'Eighties' du groupe post-punk Killing Joke. Le panneau d'entrée de la ville natale de Kurt Cobain, Aberdeen dans l'État de Washington, arbore aujourd'hui officiellement la devise : 'Welcome to Aberdeen - Come As You Are'.",
        "distractors": [
            {"composer": "Radiohead", "title": "Creep"},
            {"composer": "R.E.M.", "title": "Losing My Religion"},
            {"composer": "Foo Fighters", "title": "Everlong"}
        ]
    },
    {
        "id": "daftpunk_aroundtheworld",
        "file": "daftpunk_aroundtheworld.mid",
        "title": "Around the World",
        "composer": "Daft Punk (Thomas Bangalter & Guy-Manuel de Homem-Christo)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1990 (1997)",
        "genre": "French Touch / House",
        "year": 1997,
        "country": "France",
        "instrumentation": "Ligne de basse funk hypnotique, vocoder et synthétiseurs vintage",
        "clue": "Pionniers de la French Touch répétant inlassablement la même phrase 144 fois sur un groove irrésistible.",
        "funFact": "La phrase éponyme est répétée exactement 144 fois dans la version album et 80 fois dans le clip culte réalisé par Michel Gondry où chaque instrument est personnifié par des danseurs (robots, squelettes, momies et nageuses synchronisées) !",
        "distractors": [
            {"composer": "Cassius", "title": "Cassius 1999"},
            {"composer": "Stardust", "title": "Music Sounds Better with You"},
            {"composer": "Modjo", "title": "Lady (Hear Me Tonight)"}
        ]
    },
    {
        "id": "daftpunk_onemoretime",
        "file": "daftpunk_onemoretime.mid",
        "title": "One More Time",
        "composer": "Daft Punk (ft. Romanthony)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 2000 (2000)",
        "genre": "French Touch / Disco-House",
        "year": 2000,
        "country": "France / États-Unis",
        "instrumentation": "Cuivres samplés en boucle, auto-tune novateur et kick house énergique",
        "clue": "L'ouverture mythique de l'album Discovery et du film d'animation Interstella 5555 de Leiji Matsumoto.",
        "funFact": "Le sample de cuivres flamboyant est extrait du morceau 'More Spell on You' d'Eddie Johns (1979), découpé et réarrangé de façon virtuose par le duo casqué. Le morceau popularisa l'usage créatif et artistique de l'Auto-Tune dans la musique électronique mondiale.",
        "distractors": [
            {"composer": "Daft Punk", "title": "Harder, Better, Faster, Stronger"},
            {"composer": "Justice", "title": "D.A.N.C.E."},
            {"composer": "Laurent Garnier", "title": "The Man with the Red Face"}
        ]
    },
    {
        "id": "daftpunk_getlucky",
        "file": "daftpunk_getlucky.mid",
        "title": "Get Lucky",
        "composer": "Daft Punk ft. Pharrell Williams & Nile Rodgers",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 2010 (2013)",
        "genre": "Nu-disco / Funk",
        "year": 2013,
        "country": "France / États-Unis",
        "instrumentation": "Guitare rythmique 'chucking' de Nile Rodgers, basse groovy et voix de velours",
        "clue": "Le raz-de-marée funk de l'été 2013 qui remporta le Grammy Award de l'enregistrement de l'année.",
        "funFact": "Nile Rodgers (fondateur de Chic) joua ses parties de guitare légendaires au mythique studio Electric Lady à New York, là même où le premier album de Chic avait été enregistré en 1977. La chanson s'est vendue à près de 10 millions d'exemplaires dans le monde !",
        "distractors": [
            {"composer": "Bruno Mars", "title": "Treasure"},
            {"composer": "Mark Ronson ft. Bruno Mars", "title": "Uptown Funk"},
            {"composer": "Pharrell Williams", "title": "Happy"}
        ]
    },
    {
        "id": "aha_takeonme",
        "file": "aha_takeonme.mid",
        "title": "Take On Me",
        "composer": "A-ha (Magne Furuholmen, Morten Harket, Pål Waaktaar)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1980 (1985)",
        "genre": "Synth-pop / New wave",
        "year": 1985,
        "country": "Norvège",
        "instrumentation": "Riff ultra-rapide de synthétiseur Roland Juno-60 et voix atteignant plus de deux octaves et demie",
        "clue": "Riff de synthétiseur scandinave légendaire et clip révolutionnaire en rotoscopie (dessin animé au crayon).",
        "funFact": "La chanson fut initialement un échec commercial cuisant dans sa première version de 1984 ! C'est le réenregistrement produit par Alan Tarney associé au clip d'animation au crayon révolutionnaire de Steve Barron (qui demanda 16 semaines de dessin image par image) qui en fit un triomphe planétaire !",
        "distractors": [
            {"composer": "Depeche Mode", "title": "Just Can't Get Enough"},
            {"composer": "Eurythmics", "title": "Sweet Dreams (Are Made of This)"},
            {"composer": "Tears for Fears", "title": "Everybody Wants to Rule the World"}
        ]
    },
    {
        "id": "acdc_highwaytohell",
        "file": "acdc_highwaytohell.mid",
        "title": "Highway to Hell",
        "composer": "AC/DC (Angus Young, Malcolm Young, Bon Scott)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1970 (1979)",
        "genre": "Hard rock",
        "year": 1979,
        "country": "Australie",
        "instrumentation": "Riff de guitare Gibson SG d'Angus Young et voix éraillée de Bon Scott",
        "clue": "L'hymne hard rock ultime de la route de l'enfer, dernier album enregistré avec Bon Scott.",
        "funFact": "Le titre faisait référence à la Canning Highway en Australie, une autoroute très accidentée reliant Perth à Fremantle où de nombreux accidents mortels se produisaient près du pub fréquenté par le groupe, ainsi qu'au rythme exténuant des tournées interminables d'AC/DC !",
        "distractors": [
            {"composer": "Led Zeppelin", "title": "Whole Lotta Love"},
            {"composer": "Deep Purple", "title": "Smoke on the Water"},
            {"composer": "Kiss", "title": "Rock and Roll All Nite"}
        ]
    },
    {
        "id": "acdc_thunderstruck",
        "file": "acdc_thunderstruck.mid",
        "title": "Thunderstruck",
        "composer": "AC/DC (Angus Young, Malcolm Young)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1990 (1990)",
        "genre": "Hard rock",
        "year": 1990,
        "country": "Australie",
        "instrumentation": "Tapping / legato effréné à la guitare d'Angus Young et chœur martial 'Thunder !'",
        "clue": "Arpège vertigineux à la guitare joué à une seule main sur le manche et chant de guerre scandé dans les stades.",
        "funFact": "Angus Young a composé le célèbre riff introductif en s'amusant sur sa guitare acoustique à cordes de nylon. Il le joue en live en hammer-on et pull-off à la main gauche tout en saluant la foule de la main droite !",
        "distractors": [
            {"composer": "AC/DC", "title": "Back in Black"},
            {"composer": "Guns N' Roses", "title": "Welcome to the Jungle"},
            {"composer": "Scorpions", "title": "Rock You Like a Hurricane"}
        ]
    },
    {
        "id": "gunsnroses_sweetchild",
        "file": "gunsnroses_sweetchild.mid",
        "title": "Sweet Child O' Mine",
        "composer": "Guns N' Roses",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1980 (1987)",
        "genre": "Hard rock / Ballade rock",
        "year": 1987,
        "country": "États-Unis",
        "instrumentation": "Intro de guitare Gibson Les Paul de Slash et voix suraiguë d'Axl Rose",
        "clue": "Riff circulaire en arpège de Slash, né d'un simple exercice d'échauffement.",
        "funFact": "Slash détestait ce riff au départ ! Il le considérait comme un simple exercice d'échauffement ridicule pour les doigts façon 'musique de cirque'. Lorsque le bassiste Duff McKagan et le guitariste rythmique Izzy Stradlin ont commencé à plaquer des accords par-dessus et qu'Axl Rose a posé ses paroles d'amour, le chef-d'œuvre est né.",
        "distractors": [
            {"composer": "Bon Jovi", "title": "You Give Love a Bad Name"},
            {"composer": "Aerosmith", "title": "Dream On"},
            {"composer": "Van Halen", "title": "Jump"}
        ]
    },
    {
        "id": "eltonjohn_rocketman",
        "file": "eltonjohn_rocketman.mid",
        "title": "Rocket Man (I Think It's Going to Be a Long, Long Time)",
        "composer": "Elton John & Bernie Taupin",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1970 (1972)",
        "genre": "Pop rock / Glam rock",
        "year": 1972,
        "country": "Royaume-Uni",
        "instrumentation": "Piano bastringue, pedal steel guitar et harmonies spatiales",
        "clue": "Ballade spatiale mélancolique sur la solitude d'un astronaute en mission vers Mars.",
        "funFact": "Inspirée d'une nouvelle de science-fiction de Ray Bradbury dans 'L'Homme illustré', Bernie Taupin a eu l'idée des paroles en observant une étoile filante en voiture. N'ayant pas de papier sous la main, il dut se répéter les phrases en boucle dans sa tête pendant deux heures de route pour ne pas les oublier !",
        "distractors": [
            {"composer": "David Bowie", "title": "Starman"},
            {"composer": "Elton John", "title": "Tiny Dancer"},
            {"composer": "Billy Joel", "title": "Piano Man"}
        ]
    },
    {
        "id": "eltonjohn_stillstanding",
        "file": "eltonjohn_stillstanding.mid",
        "title": "I'm Still Standing",
        "composer": "Elton John & Bernie Taupin",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1980 (1983)",
        "genre": "New wave / Pop rock énergique",
        "year": 1983,
        "country": "Royaume-Uni",
        "instrumentation": "Piano bondissant, synthétiseurs percutants et basse slap",
        "clue": "Hymne éclatant de résilience et de renaissance personnelle avec son clip haut en couleur tourné à Cannes et Nice.",
        "funFact": "Le clip vidéo exubérant et coloré a été tourné sur la Promenade des Anglais à Nice et à l'hôtel Carlton de Cannes. Durant le tournage, Elton John fit la fête toute la nuit avec Duran Duran et détruisit accidentellement sa suite d'hôtel dans une ambiance mémorable !",
        "distractors": [
            {"composer": "George Michael", "title": "Faith"},
            {"composer": "Wham!", "title": "Wake Me Up Before You Go-Go"},
            {"composer": "Elton John", "title": "Crocodile Rock"}
        ]
    },
    {
        "id": "oasis_wonderwall",
        "file": "oasis_wonderwall.mid",
        "title": "Wonderwall",
        "composer": "Oasis (Noel Gallagher)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1990 (1995)",
        "genre": "Britpop / Rock acoustique",
        "year": 1995,
        "country": "Royaume-Uni",
        "instrumentation": "Guitare acoustique folk avec capo 2e frette, violoncelle et voix nasale de Liam Gallagher",
        "clue": "L'hymne Britpop des années 90 par excellence : 'Today is gonna be the day that they're gonna throw it back to you...'",
        "funFact": "Le titre est un hommage direct au premier album solo de George Harrison (des Beatles), la bande originale du film psychédélique 'Wonderwall' (1968). Noel Gallagher laissa le choix à son frère Liam : chanter soit 'Wonderwall', soit 'Don't Look Back in Anger' !",
        "distractors": [
            {"composer": "Blur", "title": "Country House"},
            {"composer": "The Verve", "title": "Bitter Sweet Symphony"},
            {"composer": "Oasis", "title": "Don't Look Back in Anger"}
        ]
    },
    {
        "id": "georgemichael_careless",
        "file": "georgemichael_careless.mid",
        "title": "Careless Whisper",
        "composer": "George Michael & Andrew Ridgeley",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1980 (1984)",
        "genre": "Sophisti-pop / Ballade soul",
        "year": 1984,
        "country": "Royaume-Uni",
        "instrumentation": "Solo de saxophone alto le plus célèbre des années 80",
        "clue": "Le solo de saxophone romantique le plus imité au monde sur des regrets d'infidélité.",
        "funFact": "George Michael a auditionné pas moins de dix saxophonistes professionnels à Londres sans parvenir à obtenir exactement la tonalité et la sensualité qu'il avait en tête ! C'est finalement Steve Gregory qui réussit la prise parfaite, bien que la bande ait dû être légèrement ralentie pour atteindre la tonalité exacte voulue par George Michael.",
        "distractors": [
            {"composer": "Spandau Ballet", "title": "True"},
            {"composer": "Sade", "title": "Smooth Operator"},
            {"composer": "Phil Collins", "title": "Against All Odds"}
        ]
    },
    {
        "id": "coldplay_vivalavida",
        "file": "coldplay_vivalavida.mid",
        "title": "Viva La Vida",
        "composer": "Coldplay (Chris Martin, Guy Berryman, Jonny Buckland, Will Champion)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 2000 (2008)",
        "genre": "Baroque pop / Rock orchestral",
        "year": 2008,
        "country": "Royaume-Uni",
        "instrumentation": "Section de cordes martelées en staccato, timbales et cloche d'église",
        "clue": "Fresque historique sur la déchéance d'un roi déchu, ornée de la célèbre toile de Delacroix 'La Liberté guidant le peuple'.",
        "funFact": "Le titre espagnol 'Viva La Vida' ('Vive la vie') a été emprunté à une nature morte de pastèques peinte par l'artiste mexicaine Frida Kahlo huit jours avant sa mort, malgré ses intenses souffrances physiques.",
        "distractors": [
            {"composer": "The Killers", "title": "Mr. Brightside"},
            {"composer": "Keane", "title": "Somewhere Only We Know"},
            {"composer": "Snow Patrol", "title": "Chasing Cars"}
        ]
    },
    {
        "id": "coldplay_clocks",
        "file": "coldplay_clocks.mid",
        "title": "Clocks",
        "composer": "Coldplay",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 2000 (2002)",
        "genre": "Post-Britpop / Piano-rock alternatif",
        "year": 2002,
        "country": "Royaume-Uni",
        "instrumentation": "Arpège de piano en boucle hypnotique en mi bémol majeur et guitares planantes",
        "clue": "Arpège tournoyant au piano qui valut à Coldplay le Grammy Award de l'enregistrement de l'année en 2004.",
        "funFact": "Le morceau a failli ne jamais figurer sur l'album A Rush of Blood to the Head ! Le groupe l'avait d'abord mis de côté pour l'album suivant, mais leur manager Phil Harvey les supplia de le finaliser immédiatement en affirmant que c'était le plus grand titre qu'ils avaient jamais écrit.",
        "distractors": [
            {"composer": "Radiohead", "title": "Karma Police"},
            {"composer": "Coldplay", "title": "The Scientist"},
            {"composer": "Muse", "title": "Starlight"}
        ]
    },
    {
        "id": "greenday_americanidiot",
        "file": "greenday_americanidiot.mid",
        "title": "American Idiot",
        "composer": "Green Day (Billie Joe Armstrong, Mike Dirnt, Tré Cool)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 2000 (2004)",
        "genre": "Punk rock / Pop punk",
        "year": 2004,
        "country": "États-Unis",
        "instrumentation": "Power chords frénétiques de guitare saturée et basse vrombissante",
        "clue": "Pamphlet punk anti-guerre et coup de tonnerre rock dénonçant la manipulation des médias.",
        "funFact": "L'album entier est né après le vol des bandes maîtresses de leur projet d'album précédent 'Cigarettes and Valentines'. Plutôt que de réenregistrer les mêmes chansons, Green Day décida de repartir de zéro et créa ce qui devint le plus grand opéra punk-rock des années 2000 !",
        "distractors": [
            {"composer": "The Offspring", "title": "The Kids Aren't Alright"},
            {"composer": "Blink-182", "title": "All the Small Things"},
            {"composer": "Sum 41", "title": "Fat Lip"}
        ]
    },
    {
        "id": "rickastley_nevergonna",
        "file": "rickastley_nevergonna.mid",
        "title": "Never Gonna Give You Up",
        "composer": "Rick Astley (Stock Aitken Waterman)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1980 (1987)",
        "genre": "Dance-pop / Blue-eyed soul",
        "year": 1987,
        "country": "Royaume-Uni",
        "instrumentation": "Synthétiseurs LinnDrum, boîte à rythme et voix baryton puissante",
        "clue": "Le tube pop devenu le phénomène internet le plus célèbre de l'histoire du web : le 'Rickroll' !",
        "funFact": "Alors âgé de 21 ans et travaillant comme garçon de thé dans les studios des producteurs Stock Aitken Waterman, Rick Astley impressionna par sa voix grave inattendue. Deux décennies plus tard, la chanson donna naissance au canular en ligne 'Rickroll', accumulant plus d'1,5 milliard de vues !",
        "distractors": [
            {"composer": "Kylie Minogue", "title": "I Should Be So Lucky"},
            {"composer": "Jason Donovan", "title": "Too Many Broken Hearts"},
            {"composer": "Bananarama", "title": "Venus"}
        ]
    },
    {
        "id": "leonardcohen_hallelujah",
        "file": "leonardcohen_hallelujah.mid",
        "title": "Hallelujah",
        "composer": "Leonard Cohen",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1980 (1984)",
        "genre": "Ballade folk / Poésie sacrée et profane",
        "year": 1984,
        "country": "Canada",
        "instrumentation": "Arpèges en 6/8, chœurs d'église et voix sépulcrale",
        "clue": "'Now I've heard there was a secret chord that David played...' Ballade immortelle reprise par Jeff Buckley et Shrek.",
        "funFact": "Leonard Cohen mit plusieurs années à écrire la chanson, rédigeant près de 80 couplets différents dans sa chambre d'hôtel du Royalton à New York, parfois en sous-vêtements et en se tapant la tête contre le sol de désespoir ! Son label Columbia refusa même de sortir l'album aux États-Unis, jugeant le morceau sans intérêt commercial.",
        "distractors": [
            {"composer": "Jeff Buckley", "title": "Grace"},
            {"composer": "Nick Cave", "title": "Into My Arms"},
            {"composer": "Bob Dylan", "title": "Knockin' on Heaven's Door"}
        ]
    },

    # ==========================================
    # CINÉMA, JEUX VIDÉO & CULTE (10 morceaux)
    # ==========================================
    {
        "id": "celinedion_titanic",
        "file": "celinedion_titanic.mid",
        "title": "My Heart Will Go On (Thème de Titanic)",
        "composer": "James Horner & Céline Dion",
        "category": "soundtrack",
        "categoryLabel": "🎬 Cinéma, Jeux Vidéo & Séries",
        "era": "Années 1990 (1997)",
        "genre": "Bande originale de film / Ballade pop",
        "year": 1997,
        "country": "Canada / États-Unis",
        "instrumentation": "Flûte irlandaise (tin whistle), synthétiseur et voix lyrique puissante",
        "clue": "Le thème d'amour immortel de Jack et Rose sur la proue du Titanic.",
        "funFact": "Le réalisateur James Cameron ne voulait absolument aucune chanson pop avec des paroles dans son film Titanic, et Céline Dion ne voulait pas l'enregistrer car elle n'aimait pas le morceau au départ ! Le compositeur James Horner enregistra une maquette secrète en une seule prise. En l'écoutant avec le générique de fin, Cameron fut ému aux larmes et donna son accord.",
        "distractors": [
            {"composer": "Whitney Houston", "title": "I Will Always Love You (Bodyguard)"},
            {"composer": "Elton John", "title": "Can You Feel the Love Tonight (Le Roi Lion)"},
            {"composer": "Mariah Carey", "title": "Without You"}
        ]
    },
    {
        "id": "zimmer_pirates",
        "file": "zimmer_pirates.mid",
        "title": "He's a Pirate (Pirates des Caraïbes)",
        "composer": "Hans Zimmer & Klaus Badelt",
        "category": "soundtrack",
        "categoryLabel": "🎬 Cinéma, Jeux Vidéo & Séries",
        "era": "Années 2000 (2003)",
        "genre": "Bande originale de film d'aventure",
        "year": 2003,
        "country": "Allemagne / États-Unis",
        "instrumentation": "Orchestre symphonique héroïque et percussions d'action épiques",
        "clue": "Le thème épique du capitaine Jack Sparrow fendant les vagues sur le Black Pearl.",
        "funFact": "Hans Zimmer composa le thème principal en une seule nuit chez lui après un appel d'urgence du réalisateur Gore Verbinski, le compositeur initial Alan Silvestri ayant quitté le projet à la dernière minute. En moins de 24 heures, le thème de pirates le plus célèbre du XXIe siècle était né !",
        "distractors": [
            {"composer": "John Williams", "title": "Les Aventuriers de l'arche perdue (Indiana Jones)"},
            {"composer": "Howard Shore", "title": "Le Seigneur des Anneaux (La Communauté de l'Anneau)"},
            {"composer": "Danny Elfman", "title": "Edward aux mains d'argent"}
        ]
    },
    {
        "id": "morricone_goodbadugly",
        "file": "morricone_goodbadugly.mid",
        "title": "Le Bon, la Brute et le Truand (The Good, the Bad and the Ugly)",
        "composer": "Ennio Morricone",
        "category": "soundtrack",
        "categoryLabel": "🎬 Cinéma, Jeux Vidéo & Séries",
        "era": "Années 1960 (1966)",
        "genre": "Western spaghetti / Musique de film",
        "year": 1966,
        "country": "Italie",
        "instrumentation": "Sifflement humain, ocarina, cris de coyote et guitare électrique",
        "clue": "Le duel au soleil d'anthologie dans le cimetière de Sad Hill avec Clint Eastwood.",
        "funFact": "Le motif à deux notes imitant le hurlement d'un coyote a été créé à l'aide de véritables voix humaines vocalisées ('Aï-ou-aï-ou-aï'). Chaque protagoniste (le Bon, la Brute et le Truand) possède son propre instrument pour ce motif : la flûte soprano, l'ocarina et deux voix masculines en fausset !",
        "distractors": [
            {"composer": "Ennio Morricone", "title": "Il était une fois dans l'Ouest (L'Homme à l'harmonica)"},
            {"composer": "Elmer Bernstein", "title": "Les Sept Mercenaires"},
            {"composer": "Nino Rota", "title": "Le Parrain"}
        ]
    },
    {
        "id": "kondo_supermario",
        "file": "kondo_supermario.mid",
        "title": "Super Mario Bros. (Thème Overworld)",
        "composer": "Koji Kondo",
        "category": "soundtrack",
        "categoryLabel": "🎬 Cinéma, Jeux Vidéo & Séries",
        "era": "Années 1980 (1985)",
        "genre": "Musique de jeu vidéo / Chiptune calypso",
        "year": 1985,
        "country": "Japon",
        "instrumentation": "Puce sonore 8-bits NES (2 ondes carrées, 1 onde triangle, 1 générateur de bruit)",
        "clue": "La mélodie 8-bits la plus fredonnée de la planète Terre, créée pour le plombier moustachu de Nintendo.",
        "funFact": "C'est la toute première musique de jeu vidéo de l'histoire à avoir été inscrite au Registre national des enregistrements de la Bibliothèque du Congrès américain en 2023 pour son importance historique et culturelle mondiale !",
        "distractors": [
            {"composer": "Koji Kondo", "title": "The Legend of Zelda (Thème principal)"},
            {"composer": "David Wise", "title": "Donkey Kong Country"},
            {"composer": "Nobuo Uematsu", "title": "Final Fantasy (Prélude)"}
        ]
    },
    {
        "id": "tetris_korobeiniki",
        "file": "tetris_korobeiniki.mid",
        "title": "Tetris (Thème A - Korobeiniki)",
        "composer": "Folklore Russe / Alexey Pajitnov / Hirokazu Tanaka",
        "category": "soundtrack",
        "categoryLabel": "🎬 Cinéma, Jeux Vidéo & Séries",
        "era": "Chanson du XIXe siècle / Jeu vidéo (1989)",
        "genre": "Chanson folklorique russe / Chiptune Game Boy",
        "year": 1989,
        "country": "Russie / Japon",
        "instrumentation": "Puce sonore Game Boy / Balalaïka et accordéon",
        "clue": "L'empilement frénétique de tétraminos sur l'écran monochrome de la mythique Game Boy.",
        "funFact": "À l'origine, 'Korobeïniki' ('Les Colporteurs') est un poème de Nikolaï Nekrassov publié en 1861 racontant le marchandage amoureux entre un jeune marchand ambulant et une jeune paysanne. Adaptée pour la Game Boy par Hirokazu Tanaka en 1989, elle est devenue indissociable du jeu vidéo !",
        "distractors": [
            {"composer": "Traditionnel Russe", "title": "Kalinka"},
            {"composer": "Traditionnel Russe", "title": "Les Yeux noirs (Otchi tchornye)"},
            {"composer": "Traditionnel Russe", "title": "Katioucha"}
        ]
    },
    {
        "id": "metallica_nothingelse",
        "file": "metallica_nothingelse.mid",
        "title": "Nothing Else Matters",
        "composer": "Metallica (James Hetfield & Lars Ulrich)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 1990 (1991)",
        "genre": "Heavy metal / Power ballad",
        "year": 1991,
        "country": "États-Unis",
        "instrumentation": "Arpège en cordes à vide (mi, sol, si, mi), orchestre de Michael Kamen et solo poignant",
        "clue": "La ballade metal la plus célèbre de tous les temps, jouée en arpèges ouverts à la guitare électrique.",
        "funFact": "James Hetfield a composé l'introduction d'arpège d'une seule main alors qu'il parlait au téléphone avec sa petite amie ! Comme l'autre main tenait le combiné, les quatre premières notes sont toutes jouées sur des cordes à vide (mi mineur) sans avoir besoin d'appuyer sur le manche !",
        "distractors": [
            {"composer": "Scorpions", "title": "Wind of Change"},
            {"composer": "Guns N' Roses", "title": "November Rain"},
            {"composer": "Iron Maiden", "title": "Wasted Years"}
        ]
    },
    {
        "id": "avicii_levels",
        "file": "avicii_levels.mid",
        "title": "Levels",
        "composer": "Avicii (Tim Bergling)",
        "category": "pop_rock",
        "categoryLabel": "🎸 Pop, Rock & Variété",
        "era": "Années 2010 (2011)",
        "genre": "EDM / Progressive house",
        "year": 2011,
        "country": "Suède",
        "instrumentation": "Synthétiseur lead sautillant en drop euphorique et sample d'Etta James",
        "clue": "L'hymne des festivals EDM des années 2010 samplant la voix soul d'Etta James : 'Oh, sometimes I get a good feeling...'",
        "funFact": "Avicii a construit son tube mondial autour d'un sample de la reine de la soul Etta James ('Something's Got a Hold on Me', 1962). La mélodie de synthétiseur est devenue tellement universelle qu'elle fut jouée lors de la messe royale du mariage du prince Carl Philip de Suède en 2015 !",
        "distractors": [
            {"composer": "Swedish House Mafia", "title": "Don't You Worry Child"},
            {"composer": "Calvin Harris", "title": "Summer"},
            {"composer": "Martin Garrix", "title": "Animals"}
        ]
    },
    {
        "id": "brubeck_takefive",
        "file": "brubeck_takefive.mid",
        "title": "Take Five",
        "composer": "The Dave Brubeck Quartet (Paul Desmond)",
        "category": "soundtrack",
        "categoryLabel": "🎬 Cinéma, Jeux Vidéo & Séries",
        "era": "Années 1950 (1959)",
        "genre": "Cool jazz en mesure asymétrique 5/4",
        "year": 1959,
        "country": "États-Unis",
        "instrumentation": "Saxophone alto aérien, piano modal en 5/4 et solo de batterie légendaire de Joe Morello",
        "clue": "Le morceau de jazz instrumental le plus vendu de l'histoire, célèbre pour sa mesure rare à 5 temps (5/4).",
        "funFact": "Le titre 'Take Five' est un double jeu de mots : il fait référence à la fois à l'expression américaine 'faire une pause de 5 minutes' et à la métrique musicale rarissime à 5 temps par mesure (3+2), que Dave Brubeck et Paul Desmond découvrirent lors d'une tournée en Turquie !",
        "distractors": [
            {"composer": "Miles Davis", "title": "So What"},
            {"composer": "John Coltrane", "title": "Giant Steps"},
            {"composer": "Thelonious Monk", "title": "'Round Midnight"}
        ]
    },
    {
        "id": "adele_skyfall",
        "file": "adele_skyfall.mid",
        "title": "Skyfall (007 James Bond)",
        "composer": "Adele & Paul Epworth",
        "category": "soundtrack",
        "categoryLabel": "🎬 Cinéma, Jeux Vidéo & Séries",
        "era": "Années 2010 (2012)",
        "genre": "Bande originale de film / Soul dramatique",
        "year": 2012,
        "country": "Royaume-Uni",
        "instrumentation": "Orchestre symphonique de 77 musiciens aux studios Abbey Road et voix soul de velours",
        "clue": "Chanson thème du 23e James Bond avec Daniel Craig, récompensée par l'Oscar de la meilleure chanson originale.",
        "funFact": "Adele était enceinte de son premier enfant lorsqu'elle enregistra la voix finale aux studios Abbey Road. Elle expliqua que sa voix était naturellement descendue de plusieurs tons durant la grossesse, ce qui donna au morceau sa couleur grave, sombre et envoûtante !",
        "distractors": [
            {"composer": "Shirley Bassey", "title": "Goldfinger"},
            {"composer": "Billie Eilish", "title": "No Time to Die"},
            {"composer": "Tina Turner", "title": "GoldenEye"}
        ]
    },
    {
        "id": "coolio_gangsta",
        "file": "coolio_gangsta.mid",
        "title": "Gangsta's Paradise",
        "composer": "Coolio ft. L.V. (Stevie Wonder)",
        "category": "soundtrack",
        "categoryLabel": "🎬 Cinéma, Jeux Vidéo & Séries",
        "era": "Années 1990 (1995)",
        "genre": "Hip-hop / Bande originale de film (Esprits rebelles)",
        "year": 1995,
        "country": "États-Unis",
        "instrumentation": "Chœurs religieux dramatiques, boîte à rythme hip-hop et cordes sombres",
        "clue": "L'ouverture mythique 'As I walk through the valley of the shadow of death...', bande originale d'Esprits Rebelles.",
        "funFact": "La chanson reprend la mélodie et les arrangements du chef-d'œuvre de Stevie Wonder 'Pastime Paradise' (1976). Stevie Wonder refusa initialement d'accorder ses droits, n'aimant pas les jurons dans le rap. Coolio accepta de réécrire l'intégralité du texte sans aucune grossièreté pour obtenir sa bénédiction !",
        "distractors": [
            {"composer": "Tupac Shakur", "title": "Changes"},
            {"composer": "The Notorious B.I.G.", "title": "Juicy"},
            {"composer": "Eminem", "title": "Lose Yourself"}
        ]
    }
]

def parse_vlq(data, idx):
    val = 0
    while idx < len(data):
        b = data[idx]
        idx += 1
        val = (val << 7) | (b & 0x7F)
        if not (b & 0x80):
            break
    return val, idx

def extract_notes_from_midi(filepath, max_seconds=50):
    with open(filepath, "rb") as f:
        data = f.read()
    if data[:4] != b"MThd":
        return []
    hdr_len, fmt, ntracks, division = struct.unpack(">IHHH", data[4:14])
    idx = 14
    all_events = []
    for t in range(ntracks):
        if idx >= len(data): break
        chunk_type = data[idx:idx+4]
        if idx+8 > len(data): break
        chunk_len = struct.unpack(">I", data[idx+4:idx+8])[0]
        track_data = data[idx+8:idx+8+chunk_len]
        idx += 8 + chunk_len
        if chunk_type != b"MTrk": continue
        t_idx = 0; tick = 0; running = 0
        while t_idx < len(track_data):
            delta, t_idx = parse_vlq(track_data, t_idx)
            tick += delta
            if t_idx >= len(track_data): break
            b = track_data[t_idx]
            if b & 0x80:
                status = b
                t_idx += 1
                if status < 0xF0: running = status
                else: running = 0
            else:
                status = running
            
            ev_type = status >> 4
            ch = status & 0x0F
            if status == 0xFF:
                if t_idx >= len(track_data): break
                m_type = track_data[t_idx]; t_idx += 1
                l, t_idx = parse_vlq(track_data, t_idx)
                val = track_data[t_idx:t_idx+l]; t_idx += l
                if m_type == 0x51 and len(val) == 3:
                    us = (val[0] << 16) | (val[1] << 8) | val[2]
                    all_events.append((tick, "tempo", us))
            elif status in (0xF0, 0xF7):
                l, t_idx = parse_vlq(track_data, t_idx); t_idx += l
            elif ev_type in (0x8, 0x9, 0xA, 0xB, 0xE):
                if t_idx + 1 >= len(track_data): break
                p1 = track_data[t_idx]; p2 = track_data[t_idx+1]; t_idx += 2
                if ev_type == 0x9:
                    all_events.append((tick, "note_on" if p2 > 0 else "note_off", ch, p1, p2))
                elif ev_type == 0x8:
                    all_events.append((tick, "note_off", ch, p1, 0))
            elif ev_type in (0xC, 0xD):
                if t_idx >= len(track_data): break
                p1 = track_data[t_idx]; t_idx += 1
                if ev_type == 0xC:
                    all_events.append((tick, "program", ch, p1))
    all_events.sort(key=lambda x: x[0])
    
    current_time = 0.0; last_tick = 0; us_per_beat = 500000
    timed_events = []
    div = division if division > 0 else 120
    for ev in all_events:
        tick = ev[0]
        dtick = tick - last_tick
        current_time += dtick * (us_per_beat / 1000000.0) / div
        last_tick = tick
        if ev[1] == "tempo":
            us_per_beat = ev[2]
        timed_events.append((current_time, ev))
        
    active_notes = {}
    completed_notes = []
    current_programs = {i: 0 for i in range(16)}
    
    for t_sec, ev in timed_events:
        kind = ev[1]
        if kind == "program":
            current_programs[ev[2]] = ev[3]
        elif kind == "note_on":
            ch, note, vel = ev[2], ev[3], ev[4]
            key = (ch, note)
            if key in active_notes:
                start_t, start_v, prg = active_notes.pop(key)
                completed_notes.append((start_t, note, round(max(0.04, t_sec - start_t), 3), start_v, ch, prg))
            active_notes[key] = (t_sec, vel, current_programs.get(ch, 0))
        elif kind == "note_off":
            ch, note = ev[2], ev[3]
            key = (ch, note)
            if key in active_notes:
                start_t, start_v, prg = active_notes.pop(key)
                dur = round(max(0.04, t_sec - start_t), 3)
                completed_notes.append((start_t, note, dur, start_v, ch, prg))
                
    for key, (start_t, start_v, prg) in active_notes.items():
        completed_notes.append((start_t, key[1], 0.25, start_v, key[0], prg))
        
    completed_notes.sort(key=lambda x: x[0])
    notes_trimmed = [n for n in completed_notes if n[0] <= max_seconds]
    # Format: [round(t, 2), note, round(dur, 2), vel, ch, prg]
    return [[round(n[0], 2), n[1], round(n[2], 2), n[3], n[4], n[5]] for n in notes_trimmed]

def main():
    print(f"Building data for {len(TRACK_DEFINITIONS)} tracks...")
    processed_tracks = []
    
    for item in TRACK_DEFINITIONS:
        fname = item["file"]
        fpath = os.path.join(MIDI_DIR, fname)
        if not os.path.exists(fpath):
            print(f"MISSING FILE: {fpath}")
            continue
        
        # Read raw midi
        with open(fpath, "rb") as f:
            raw_bytes = f.read()
        
        notes = extract_notes_from_midi(fpath, max_seconds=45)
        duration = round(notes[-1][0] + notes[-1][2], 1) if notes else 30.0
        
        track_entry = {
            "id": item["id"],
            "title": item["title"],
            "composer": item["composer"],
            "category": item["category"],
            "categoryLabel": item["categoryLabel"],
            "era": item["era"],
            "genre": item["genre"],
            "year": item["year"],
            "country": item["country"],
            "instrumentation": item["instrumentation"],
            "clue": item["clue"],
            "funFact": item["funFact"],
            "distractors": item["distractors"],
            "file": f"midi/{fname}",
            "duration": duration,
            "noteCount": len(notes),
            "notes": notes
        }
        processed_tracks.append(track_entry)
        print(f"  + {item['title']} ({item['composer']}): {len(notes)} notes, {duration}s")
    
    # Write to tracks.js
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("/**\n * MemoZik - Base de données des 60 chefs-d'œuvre musicaux\n")
        f.write(" * Chaque morceau contient métadonnées complètes, distracteurs et séquence de notes pour synthèse Web Audio.\n")
        f.write(" */\n\n")
        f.write("const MUSIC_TRACKS = ")
        f.write(json.dumps(processed_tracks, ensure_ascii=False, indent=2))
        f.write(";\n\n")
        f.write("if (typeof module !== 'undefined' && module.exports) {\n    module.exports = MUSIC_TRACKS;\n}\n")
    
    print(f"DONE! Successfully generated {OUTPUT_JS} with {len(processed_tracks)} tracks!")

if __name__ == "__main__":
    main()
