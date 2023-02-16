# GameBot

GameBot est un gentil bot discord qui aime les jeux de société.

# Présentation générale

GameBot est un bot discord principalement conçu pour maintenir une liste de jeux de société (la liste de tous les jeux possédés par les membres du serveur discord dans lequel il se trouve). Chaque membre du serveur peut ajouter/modifier/supprimer les jeux qu'il possède de la liste du bot.

GameBot permet aussi de gérer l'annonce de la prochaine soirée jeux de société organisée par le propriétaire du bot : il peut l'annoncer en mentionnant @everyone et annoncer son annulation (si elle dois malheureusement être annulée) en mentionnant ceux qui comptaient s'y rendre.

# Fonctionnalités

GameBot dispose de nombreuses fonctionnalités que je vais expliquer plus en détails dans cette partie.

Il possède un certain nombre de commandes utilisables par tous les membres du serveur discord depuis le salon principal du bot dont voici le liste :
- !hello (pour dire bonjour au bot, il répond par une rapide présentation de ses fonctionnalités)
- !commands (pour afficher la liste des commandes disponibles depuis le salon principal du bot)
- !h [commande] (pour avoir de l'aide à propos d'une commande et savoir comment l'utiliser)
- !list (pour afficher les noms et descriptions des jeux présents dans la liste du bot)
- !info [jeu] (pour avoir plus d'informations sur un jeu en particulier)
- !add [jeu] (pour ajouter un jeu à la liste du bot)
- !rename [jeu] [nouveau nom] (pour modifier le nom d'un jeu)
- !desc [jeu] [description] (pour modifier la description d'un jeu)
- !rules [jeu] [lien] (pour ajouter un lien vers les règles d'un jeu)
- !nbj [jeu] [n_min] [n_max] (pour modifier le nombre de joueurs min et max d'un jeu)
- !tj [jeu] [temps de jeu] (pour modifier le temps de jeu d'un jeu)
- !del [jeu] (pour supprimer un jeu de la liste du bot)

Il possède aussi des commandes utilisables uniquement par le propriétaire du bot depuis un salon que seuls lui et le bot peuvent voir. Ces commandes ont pour objectif de contrôler le bot. En voici le liste :
- !msg [salon] [message] (pour faire envoyer un message par le bot dans un de ses channels)
- !test (pour vérifier que le bot fonctionne bien)
- !dumpm (pour afficher la liste des membres du serveur)
- !kill (pour arrêter le bot)
- !clean [salon] [n] (pour supprimer n messages dans le salon renseigné)
- !commands (pour afficher la liste des commandes disponibles depuis le salon de contrôle du bot)
- !evdate [date] (pour définir la date de la prochaine soirée)
- !evshow pour afficher des informations à propos de la prochaine soirée
- !evannounce (pour annoncer la prochaine soirée)
- !evdel [arg] (pour supprimer la prochaine soirée (si elle a été annoncée, on envoie un message pour prévenir de l'annulation, sauf si arg="done" car dans ce cas, on supprime la soirée car elle est passée))

GameBot a aussi quelques fonctionnalités autres que ces commandes :
- quand quelqu'un essaye d'utiliser une commande depuis un autre salon que le salon principal du bot, il l'informe de cela puis supprime son message 5 secondes plus tard
- quand quelqu'un essaye d'utiliser une commande inexistante, il l'informe de cela puis supprime son message 5 secondes plus tard
- quand quelqu'un oublie un argument à une commande, il l'informe de cela puis supprime son message 5 secondes plus tard

Quelques informations à connaître à propos de GameBot :
- quand GameBot recherche un jeu dans sa liste de jeux, il le fait de façon insensible à la casse. On ne peut donc pas ajouter à sa liste deux jeux ayant le même nom à la casse près et quand on renseigne un nom de jeu en argument d'une commande, on n'est pas obligé de mettre les majuscules au bon endroit.
- quand on veut renseigner un argument contenant au moins une fois le caractère espace, il faut mettre des guillemets autour de l'argument pour éviter que GameBot croit qu'il y a plusieurs arguments
- pour ajouter une description à un jeu de société, on peut utiliser la syntaxe \`\`\`texte\`\`\` de discord pour l'argument "description". Le bot supprimera les \`\`\`. 

# Utiliser GameBot

Si vous voulez utiliser GameBot dans votre serveur discord, vous devrez d'abord :
- créer un nouveau bot depuis le portail des développeurs de discord
- créer un fichier .env dans le dossier src et y placer le token de votre bot sous ce format :
  "TOKEN=VOTRE_TOKEN_ICI"
- modifier les différents id présents dans variable.py (celui du propriétaire du bot, celui du serveur discord et ceux des différents salons du bot)
Ensuite, pour lancer le bot, il vous suffit d'exécuter le script run.sh