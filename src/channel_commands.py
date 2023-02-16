from events import *

"""help
Usage : !list

Affiche tous les jeux présents dans la base de données du bot et leurs descriptions
"""
@bot.command(name="list")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def list_games(ctx) :

	ok,err,arg = bot.prepare(ctx, "list")

	if ok :

		# on vérifie que la liste de jeu n'est pas vide
		if bot.games.dic != {} :

			game_list = list(bot.games.keys())
			game = game_list[0]
			game_str = f"**{game}** : {bot.games[game]['description']}\n"

			res = ""
			last_game_sent = False

			while not(last_game_sent) :

				if game == game_list[-1] :
					if len(res+game_str) <= 2000 :
						await ctx.channel.send(res+game_str)
					else :
						await ctx.channel.send(res)
						await ctx.channel.send(game_str)
					last_game_sent = True
				else :
					if len(res+game_str) > 2000 :
						await ctx.channel.send(res)
						res = game_str
					else :
						res += game_str

					game = game_list[game_list.index(game)+1]
					game_str = f"**{game}** : {bot.games[game]['description']}\n"

		else :
			await ctx.channel.send(f"Je ne connais aucun jeu, apprends m'en un s'il-te-plaît. :worried:")

	else :
		await bot.send_err(ctx, err)

"""help
Usage : !add game_name

Ajoute un nouveau jeu à la base de données du bot
NB : Si le nom du jeu contient au moins un espace, il faut le mettre entre guillemets
"""
@bot.command(name="add")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def add_game(ctx, name: str) :
	ok,err,args = bot.prepare(ctx, "add", name=name)
	if ok :
		name = args[0]
		bot.games[name] = {
			"description" : "",
		   	"Règles" : "",
		   	"nombre de joueurs" : "",
		   	"temps de jeu" : "",
		   	"owner" : str(ctx.author)
		}
		bot.write_games()
		await ctx.channel.send(f"Fini ! J'ai ajouté {name} à ma liste de jeux. J'ai hâte d'y jouer ! :slight_smile:")
	
	else :
		await bot.send_err(ctx, err)


"""help
Usage : !rename game_name1 game_name2

Remplace le nom d'un jeu sans avoir à tout réécrire (c'est pratique)
"""
@bot.command(name="rename")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def rename_game(ctx, name1: str, name2: str) :
	ok,err,args = bot.prepare(ctx, "rename", name1=name1, name2=name2)
	if ok :
		game,name2 = args
		bot.games[name2] = bot.games[game]
		bot.games.pop(game)
		bot.write_games()
		await ctx.channel.send(f"Et voilà ! Un nom tout neuf !")
	else :
		await bot.send_err(ctx, err)

"""help
Usage : !del game_name

Supprime un jeu de la base de donnée du bot
"""
@bot.command(name="del")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def del_game(ctx, name: str) :
	ok,err,args = bot.prepare(ctx, "del", name=name)
	if ok :
		game = args[0]
		bot.games.pop(game)
		bot.write_games()
		await ctx.channel.send(f"D'accord, je retire {game} de ma liste. As-tu perdu ce jeu ? :worried:")
	else :
		await bot.send_err(ctx, err)

""" help
Usage : !desc game_name description

Modifie la description du jeu renseigné
NB1 : Mettez des guillemets autour de la description
NB2 : On peut utiliser la notation \\`\\`\\` de discord pour entrer la description plus facilement, ils seront supprimés et les sauts de ligne seront ignorés (attention : mettez les guillemets autour des \\`\\`\\`)
NB3 : Si la description contient des guillemets, pensez à les échapper avec un \\
"""
@bot.command(name="desc")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def desc_game(ctx, name: str, desc: str) :
	ok,err,args = bot.prepare(ctx, "desc", name=name, desc=desc)
	if ok :
		game,desc = args
		# On met à jour la description	
		bot.games[game]["description"] = desc
		bot.write_games()
		await ctx.channel.send(f"Intéressant ! {game} semble être un jeu passionnant ! :star_struck:")
	else :
		await bot.send_err(ctx, err)

"""help
Usage : !rules game_name rules_link

Ajoute un lien vers les règles du jeu
"""
@bot.command(name="rules")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def rules_game(ctx, name: str, link: str) :

	ok,err,args = bot.prepare(ctx, "rules", name=name, link=link)

	if ok :
		game,link = args
		bot.games[game]["Règles"] = link
		bot.write_games()
		await ctx.channel.send(f"Je vais aller lire ça. La prochaine fois qu'on joue je serai incollables sur les règles de {game} ! :muscle:")
	else :
		await bot.send_err(ctx, err)

"""help
Usage : !nbj game_name number_min number_max

Modifie le nombre de joueurs du jeu renseigné
NB : on doit avoir number_min <= number_max
"""
@bot.command(name="nbj")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def nbj_game(ctx, name: str, n1: str, n2: str) :
	ok,err,args = bot.prepare(ctx, "nbj", name=name, n1=n1, n2=n2)
	if ok :
		game,n1,n2 = args
		bot.games[game]["nombre de joueurs"] = f"{n1}-{n2}"
		bot.write_games()
		await ctx.channel.send(f"Ok ! c'est noté !")
	else :
		await bot.send_err(ctx, err)

"""help
Usage : !tj game_name game_duration

Modifie la durée d'une partie du jeu renseigné
NB : le paramètre game_duration doit être au format XXhXX ou XXmin
"""
@bot.command(name="tj")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def tj_game(ctx, name: str, tj: str) :
	ok,err,args = bot.prepare(ctx, "tj", name=name, tj=tj)
	if ok :
		game,tj = args
		bot.games[game]["temps de jeu"] = tj
		bot.write_games()
		minutes = 0
		if re.match(r"[0-9]*h[0-5][0-9]", tj) :
			minutes = 60*int(tj.split("h")[0])+int(tj.split("h")[1])
		else :
			minutes = int(tj.split("min")[0])
		if minutes <= 30 :
			await ctx.channel.send(f"Un jeu rapide ! Parfait pour les gens qui veulent pas se prendre la tête pendant des heures. :slight_smile:")
		elif minutes <= 60 :
			await ctx.channel.send(f"Une durée classique pour un jeu de société. ")
		else :
			await ctx.channel.send(f"Plus d'une heure de jeu ?! {game} est un jeu pour les gens qui ont du temps devant eux ! :astonished:")
	else :
		await bot.send_err(ctx, err)

"""help
Usage : !h command_name

Affiche de l'aide à propos d'une commande
"""
@bot.command(name="h")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def help_game(ctx, comm: str) :
	ok,err,args = bot.prepare(ctx, "h", comm=comm)
	if ok :
		comm = args[0]
		await ctx.channel.send(bot.bot_command_dic[comm])
	else :
		await bot.send_err(ctx, err)

"""help
Usage : !commands

Afiche une liste des commandes disponibles
"""
@bot.command(name="commands")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def commands_game(ctx) :
	ok,err,args = bot.prepare(ctx, "commands")
	if ok :
		res = ""
		if bot.bot_channel(ctx) :
			for comm in bot.bot_command_dic :
				res += f"- **{comm}** : "+bot.bot_command_dic[comm].split("\n")[1]+"\n"
		elif bot.control_channel(ctx) :
			for comm in bot.control_command_dic :
				res += f"- **{comm}** : "+bot.control_command_dic[comm].split("\n")[1]+"\n"
		await ctx.channel.send(res)
	else :
		await bot.send_err(ctx, err)

"""help
Usage : !info game_name

Affiches toutes les infos disponibles pour un jeu donné
"""
@bot.command(name="info")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def info_game(ctx, name: str) :
	ok,err,args = bot.prepare(ctx, "info", name=name)
	if ok :
		game = args[0]
		# première ligne avec les "==="
		res = "".join(c for c in ['=']*int((113-len(game))/2)) + f" **{game}** " + "".join(c for c in ['=']*int((113-len(game))/2)) + "\n"
		
		for elt in bot.games[game] :
			res += f"**{elt}** : {bot.games[game][elt]}\n"
		await ctx.channel.send(res)
	else :
		await bot.send_err(ctx, err)

"""help
Usage : !hello

Commande pour dire bonjour au bot (parce qu'il faut être poli dans la vie)
"""
@bot.command(name="hello")
@commands.cooldown(per,rate,commands.BucketType.guild)
async def bot_game(ctx) :
	ok,err,args = bot.prepare(ctx, "hello")
	if ok :
		await ctx.channel.send(hello_msg)
	else :
		await bot.send_err(ctx, err)