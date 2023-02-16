# nom des fichiers .json dans lequel le bot va lire
games_file = "json/games.json"
event_file = "json/event.json"
msg_file = "json/msgid.txt"

bot_owner_id = 394185214479302656

# id du salon dans lequel le bot répond aux commandes (qui sont tappées dans ce salon et pas ailleurs)
bot_guild_id = 1064187729597976616
bot_channel_id = 1074651037031473172
announce_channel_id = 1075392928815517707
welcome_channel_id = 1074651070200037466
general_channel_id = 1064187729597976619
control_channel_id = 1066665178596380733
error_channel_id = 1067570753375064165

# liste des commandes du bot et de leurs descriptions (commandes disponibles dans le bot_channel)
bot_command_dic = {
	"hello"    : "**Usage : !hello**\nCommande pour dire bonjour au bot (parce qu'il faut être poli dans la vie)",
	"commands" : "**Usage : !commands**\nAfiche une liste des commandes disponibles",
	"h"        : "**Usage : !h command_name**\nAffiche de l'aide à propos d'une commande",
	"list"     : "**Usage : !list**\nAffiche tous les jeux présents dans la base de données du bot et leurs descriptions",
	"info"     : "**Usage : !info game_name**\nAffiches toutes les infos disponibles pour un jeu donné",
	"add"      : "**Usage : !add game_name**\nAjoute un nouveau jeu à la base de données du bot\nNB : Si le nom du jeu contient au moins un espace, il faut le mettre entre guillemets",
	"rename"   : "**Usage : !rename game_name1 game_name2**\nRemplace le nom d'un jeu sans avoir à tout réécrire (c'est pratique)",
	"del"      : "**Usage : !del game_name**\nSupprime un jeu de la base de donnée du bot",
	"desc"     : "**Usage : !desc game_name description**\nModifie la description du jeu renseigné\nNB1 : Mettez des guillemets autour de la description\nNB2 : On peut utiliser la notation \\`\\`\\` de discord pour entrer la description plus facilement, ils seront supprimés et les sauts de ligne seront ignorés (attention : mettez les guillemets autour des \\`\\`\\`)\nNB3 : Si la description contient des guillemets, pensez à les échapper avec un \\",
	"rules"    : "**Usage : !rules game_name rules_link**\nAjoute un lien vers les règles du jeu",
	"nbj"      : "**Usage : !nbj game_name number_min number_max**\nModifie le nombre de joueurs du jeu renseigné\nNB : on doit avoir number_min <= number_max",
	"tj"       : "**Usage : !tj game_name game_duration**\nModifie la durée d'une partie du jeu renseigné\nNB : le paramètre game_duration doit être au format XXhXX ou XXmin"
}

# liste des commandes de contôle du bot et de leurs descriptions (commandes disponibles dans le control_channel, réservées au propriétaire du bot)
control_command_dic = {
	"msg" : "\n",
	"test" : "\n",
	"dumpm" : "\n",
	"kill" : "\n",
	"clean" : "\n",
	"commands" : "\n",
	"evdate" : "\n",
	"evshow" : "\n",
	"evannounce" : "\n",
	"evdel" : "\n"
}

MAX_LENGTH_NAME = 80
MAX_LENGTH_DESC = 1600
MAX_LENGTH_RULES = 150
MAX_LENGTH_TJ = 5

pentester_pro = "pentester pro"

per = 1
rate = 5


hello_msg = """
Salut ! :wave:\n
Moi c'est **GameBot** :robot:, je suis un bot qui aime les jeux de société (j'en connais plein :slight_smile:).\n
Je peux te parler des jeux que je connais et tu pourra même peut-être y jouer bientôt. :game_die: :black_joker:\n
Si tu veux, tu peux m'apprendre un nouveau jeu, mais tu dois pouvoir y jouer avec moi (ça serait dommage de me donner envie de jouer à un jeu sans pouvoir le tester).\n
Pour l'instant j'ai peu de fonctionnalités mais je devrais en apprendre d'autre bientôt. :star: :medal: Tappe !commands pour connaîtres toutes mes capacités ! :muscle:\n
Quelques petites choses importantes à savoir :
- Je recherche les jeux dans ma liste de manière case-insensitive (donc on ne peut pas ajouter deux jeux ayant le même nom aux majuscules prêt, et quand tu mets un nom de jeu en argument d'une commande, tu n'es pas obligé de mettre les majuscules)
- Quand tu écrit une description de jeu (c'est long une description :face_exhaling:), tu peux utuliser les \\`\\`\\` de discord pour que ça soit plus simple, je les retirerai et ignorerai les retours à la ligne
- Tu ne pourras pas modifier ou supprimer un jeu qui a été ajouté par quelqu'un d'autre\n
A bientôt ! :slight_smile:
"""
