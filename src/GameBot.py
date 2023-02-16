"""
Fichier contenant la classe du bot et une autre classe implémentant
un dictionnaire python auquel j'ai ajouté une méthode
"""

from discord.ext import commands
import discord
import json
import re
import asyncio

from variables import *

class CustomDict(dict) :

	def __init__(self, dic) :
		super().__init__()
		self.dic = dic
		keys = list(dic.keys())
		values = list(dic.values())
		for i in range(len(keys)) :
			self[keys[i]] = values[i]

	# change l'ordre des ensembles clé/valeur du dictionnaire
	# (pour ranger les jeux par ordre alphabétique)
	def new_order(self, keys) :
		values = []
		for key in keys :
			values.append(self[key])
		return CustomDict({key:value for (key,value) in zip(keys, values)})

class GameBot(commands.Bot) :

	def __init__(self, games_file, event_file, msg_file, bot_command_dic, control_command_dic, owner_id) :
		super().__init__(command_prefix="!", intents=discord.Intents.all())

		# dictionnaire stockant les jeux
		self.games = CustomDict({})

		# dictionnaire stockant les membres du serveur du bot
		self.members = CustomDict({})

		# dictionnaire stockant les différents salons dans lesquels le bot peut écrire
		self.channels = CustomDict({})

		# fichier stockant les jeux au format json
		self.games_file = games_file

		# fichier stockant le prochain événement au format json
		self.event_file = event_file

		# fichier stockant l'id du message d'annonce d'événement
		self.msg_file = msg_file

		# dictionnaires stockant les commandes (bot et control)
		self.bot_command_dic = bot_command_dic
		self.control_command_dic = control_command_dic

		self.next_event = {}
		self.announce_msg = None
		self.announce_msg_id = 0

		self.bot_guild = None
		self.bot_guild_roles = None

		self.owner_id = owner_id
		self.alphabet = "?!,;.:/-`{}()[]= \"0123456789AaÀàÂâBbCcçDdEeÉéÈèÊêFfGgHhIiÎîJjKkLlMmNnOoÔôPpQqRrSsTtUuùVvWwXxYyZz\n"

	def bot_channel(self, ctx) :
		""" Is the ctx channel the bot principal channel ?

		Returns :
			bool : True if the ctx channel is the bot principal channel, False if it's not

		"""
		return ctx.channel==self.channels["bot_channel"]

	def control_channel(self, ctx) :
		""" Is the ctx channel the bot control channel ?

		Returns :
			bool : True if the ctx channel is the bot control channel, False if it's not
		
		"""
		return ctx.channel==self.channels["control_channel"]

	def alpha_sort(self, string_list, alphabet) :
		""" Sorts a list of strings according to a specific alphabet

		Parameters :
			string_list (List[str]) : a list of strings (must contain only caracters presents in alphabet)
			alphabet (str) : a string representing an alphabet (must not contain the same caracter twice)

		Returns :
			List[str] : a list containing the same strings as string_list, sorted according the alphabet
		
		"""
		return sorted(string_list, key=lambda word: [alphabet.index(c) for c in [word2.lower() for word2 in word]])
		
	def write_games(self) :
		""" Writes the game list in the game file in a JSON format
		(see the file whose name is stored in self.game_file (see in variables.py) to see what is stored in it)
		"""
		game_list = self.alpha_sort(list(self.games.keys()), self.alphabet)
		self.games = self.games.new_order(game_list)
		json_object = json.dumps(self.games, indent=2)
		with open(self.games_file, "wt") as f_games :
			f_games.write(json_object)

	def write_event(self) :
		""" Writes the next event informations in the event file in a JSON format
		(see the file whose name is stored in self.event_file (see in variables.py) to see what is stored in it)
		"""
		json_object = json.dumps(self.next_event, indent=2)
		with open(self.event_file, "wt") as f_event :
			f_event.write(json_object)

	def find_game(self, name) :
		""" Searches the name of a game in the game list

		Parameters :
			name (str) : string supposed to be the name of a game (with good letters/caracters but not necessarily good capital letters)

		Returns :
			str or None : the right name of the game (with good capital letters) if it exists in the list (None else)

		"""
		for game in list(self.games.keys()) :
			if name.lower() == game.lower() :
				return game
		return None

	def find_member(self, name) :
		""" Searches the name of a member in the guild
		"""
		for member in list(self.members.keys()) :
			if str(name).lower() == str(member).lower() :
				return member
		return None

	def find_role(self, name) :
		""" Searches the name of a role in the guild
		"""
		for role in self.bot_guild_roles :
			if str(name).lower() == role.name.lower() :
				return role
		return None

	def find_reaction(self, message, emoji_name) :
		""" Searches a reaction at a message

		Parameters :
			message (discord.Message) : a message published in the guild
			emoji_name (str) : the name of the emoji we are looking for in the reactions to the message

		Returns :
			discord.Reaction or None : the reaction with the correct emoji if it is present on this message (None else)

		"""
		for reaction in message.reactions :
			if reaction.emoji == emoji_name :
				return reaction
		return None

	def valid_string(self, string) :
		""" Does the string contain only authorised caracters ?
		"""
		for c in string :
			if not(c in self.alphabet) :
				return False
		return True

	def is_number(self, string) :
		""" Does the string represent a number ?
		"""
		for c in string :
			if not(c in "0123456789") :
				return False
		return True

	def knows(self, name) :
		""" Is this game present in the game list ? (case insensitive)
		"""
		return name.lower() in [string.lower() for string in list(self.games.keys())]

	async def send_err(self, ctx, err) :
		""" Sends the error message to the ctx channel (not a real error, just a string informing the user who used a 
		command that he used it in a bad way).
		(if it's not bot channel, remove the error message and the initial message after 5 secondes)
		"""
		await ctx.channel.send(err)
		if ctx.channel != self.channels["bot_channel"] :
			await asyncio.sleep(5)
			await ctx.channel.purge(limit=2)


	def prepare(self, ctx, command: str, *args, **kwargs) :
		""" Does lot of things having to be done before each commands

		Parameters :
			command (str) : the name of the command being used
			**kwargs : all the parameters of the command (keyword-only parameters)

		Returns :
			Tuple[bool, str, List[str]] :
				valid_command and valid_args (bool) : can the command be executed ? (is the use of the command a good use ?)
				error_msg (str) : message to send in the ctx channel in the case of a bad use of the command (see send_err() method)
				arg_list (List[str]) : list of the arguments of the command to be executed

		"""

		valid_command = False
		valid_args = False
		arg_list = []
		error_msg = ""

		# On vérifie que la commande a été lancée dans le bon channel (bot_channel pour les commandes du bot et control_channel pour les commandes de contrôle)
		if ((command in self.bot_command_dic and ctx.channel==self.channels["bot_channel"]) or (command in self.control_command_dic and ctx.channel==self.channels["control_channel"])) :
			valid_command = True
		else :
			return (False, f"Pas ici... :grimacing: Je ne réponds aux commandes que dans #{self.channels['bot_channel']}",[])

		# On échappe le markdown discord et on vérifie que tous les caractères utilisés sont autorisés
		for arg in kwargs :
			kwargs[arg] = discord.utils.escape_markdown(kwargs[arg])
			if arg != "desc" :
				for c in str(kwargs[arg]) :
					if not(c in self.alphabet) :
						return (False, f"'{c}' est un caractère interdit, voici la liste des caractères autorisés : {self.alphabet}", arg_list)

		# On vérifie que les arguments respectent les critères voulus
		if valid_command and command in self.bot_command_dic :

			# commandes sans argument
			if command in ["hello", "commands", "list"] :
				valid_args = True

			# !h comm
			elif command == "h" :
				comm = kwargs["comm"]
				if not(comm in self.bot_command_dic) :
					error_msg = f"Qu'est-ce que c'est que cette commande encore ? Je sais pas faire ça moi, mais peut-être que si tu demandes à M1k3y il saura m'apprendre. :slight_smile:"
				else :
					arg_list = [comm]
					valid_args = True

			# !info name
			elif command == "info" :
				name = kwargs["name"]
				if not(self.knows(name)) :
					error_msg = f"Je ne connais pas {name}, malheureusement... :pensive:"
				else :
					arg_list = [self.find_game(name)]
					valid_args = True

			# !add name
			elif command == "add" :
				name = kwargs["name"]
				if len(name) > MAX_LENGTH_NAME :
					error_msg = f"Nom de jeu trop long :grimacing:"
				elif self.knows(name) :
					error_msg = f"Je connais déjà {self.find_game(name)}, pas besoin de m'en dire plus. :sunglasses:"
				else :
					arg_list = [name]
					valid_args = True

			# !rename name1 name2
			elif command == "rename" :
				name1 = kwargs["name1"]
				name2 = kwargs["name2"]
				if not(self.knows(name1)) :
					error_msg = f"Je ne connais pas {name1}, dis m'en plus... :slight_smile:"
				else :
					game = self.find_game(name1)
					if name2 == game :
						error_msg = f"Le nom que tu proposes est déjà le nom actuel du jeu, je n'ai donc pas modifié {game}."
					elif self.knows(name2) and not(name2.lower()==game.lower()) :
						error_msg = f"Le nom que tu proposes fait déjà partie de ma liste de jeux"
					elif len(name2) > MAX_LENGTH_NAME :
						error_msg = f"Le nom que tu proposes est trop long :grimacing:"
					elif str(ctx.author) != self.games[game]["owner"] and ctx.author.id != self.owner_id :
						error_msg = f"Tu ne peux pas modifier {game}, il appartient à {self.games[game]['owner']} !"
					else :
						arg_list = [game, name2]
						valid_args = True

			# !del name
			elif command == "del" :
				name = kwargs["name"]
				if not(self.knows(name)) :
					error_msg = f"Je ne connais pas {name}, pourquoi veux-tu supprimer un jeu ? :worried:"
				else :
					game = self.find_game(name)
					if str(ctx.author) != self.games[game]["owner"] and ctx.author.id != self.owner_id :
						error_msg = f"Tu ne peux pas supprimer ce jeu, il appartient à {self.games[game]['owner']} !"
					else :
						arg_list = [game]
						valid_args = True

			# !desc name desc
			elif command == "desc" :
				name = kwargs["name"]
				desc = kwargs["desc"]
				if not(self.knows(name)) :
					error_msg = f"Je ne connais pas {name}, ajoute le à ma liste avant de m'expliquer les règles ! :joy:"
				else :
					game = self.find_game(name)
					if len(desc) > MAX_LENGTH_DESC :
						error_msg = f"Description trop longue :grimacing:"
					elif str(ctx.author) != self.games[game]["owner"] and ctx.author.id != self.owner_id :
						error_msg = f"Tu ne peux pas modifier {game}, il appartient à {self.games[game]['owner']} !"
					else :
						if desc.startswith("\\`\\`\\`") and desc.endswith("\\`\\`\\`") :
							desc = desc[6:-6]
						desc = desc.replace("\n", "")
						arg_list = [game, desc]
						valid_args = True

			# !rules name link
			elif command == "rules" :
				name = kwargs["name"]
				link = kwargs["link"]
				if not(self.knows(name)) :
					error_msg = f"Je ne connais pas {name}, apprends-moi à y jouer s'il-te-plaît. :slight_smile:"
				else :
					game = self.find_game(name)
					if len(link) > MAX_LENGTH_RULES :
						error_msg = f"Lien trop long :grimacing:"
					elif str(ctx.author) != self.games[game]["owner"] and ctx.author.id != self.owner_id :
						error_msg = f"Tu ne peux pas modifier {game}, il appartient à {self.games[game]['owner']} !"
					elif not("https://" in link) :
						error_msg = f"Es-tu sûr(e) que ce lien est valide ? :thinking:"
					else :
						arg_list = [game, link]
						valid_args = True

			# !nbj name n1 n2
			elif command == "nbj" :
				name = kwargs["name"]
				n1 = kwargs["n1"]
				n2 = kwargs["n2"]
				if not(self.knows(name)) :
					error_msg = f"Qu'est-ce que c'est que {name} ? Dis m'en plus ! Je veux savoir ! :slight_smile:"
				else :
					game = self.find_game(name)
					if str(ctx.author) != self.games[game]["owner"] and ctx.author.id != self.owner_id :
						error_msg = f"Tu ne peux pas modifier {game}, il appartient à {self.games[game]['owner']} !"
					elif not(self.is_number(n1) and self.is_number(n2)) :
						error_msg = "Veuillez entrer des vrais nombres"
					elif int(n1) > int(n2) :
						error_msg = f"Un jeu se jouant de {n1} à {n2} joueurs ? Tu comptes à l'envers ou quoi ? :zany_face:"
					elif int(n2) > 20 :
						error_msg = f"{n2} joueurs, c'est trop. On peut pas rentrer à {n2} dans un appartement !"
					else :
						arg_list = [game, n1, n2]
						valid_args = True

			# !tj name tj
			elif command == "tj" :
				name = kwargs["name"]
				tj = kwargs["tj"]
				if not(self.knows(name)) :
					error_msg = f"Euh... Je ne connais pas {name}. J'ai honte, c'est sûrement un excellent jeu. Apprends-moi s'il-te-plaît. :hugging:"
				else :
					game = self.find_game(name)
					if str(ctx.author) != self.games[game]["owner"] and ctx.author.id != self.owner_id :
						error_msg = f"Tu ne peux pas modifier {game}, il appartient à {self.games[game]['owner']} !"
					if not(re.match(r"[0-9]*h[0-5][0-9]", tj) or re.match(r"[0-9]*min", tj)) :
						error_msg = f"Je connais deux formats différents pour écrire une durée : pour un jeu qui dure 75 minutes, j'accepte 1h15 et 75min (mais pas 0h75, faut pas abuser... Et pourquoi pas -1h135 ou -2h195 ? On aura tout vu !)"
					elif len(tj) > MAX_LENGTH_TJ :
						error_msg = "Oula, c'est trop long comme jeu... :grimacing:"
					else :
						arg_list = [game, tj]
						valid_args = True

			else :
				error_msg = f"Oula, il semblerait que M1k3y ait oublié d'implémenter cette commande, tu peux aller l'insulter."

		return (valid_command and valid_args, error_msg, arg_list)