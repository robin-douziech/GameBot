import sys
import asyncio

from GameBot import *

bot = GameBot(games_file, event_file, msg_file, bot_command_dic, control_command_dic, bot_owner_id)
bot.remove_command("help")

@bot.event
async def on_ready() :

	# serveur du bot
	bot.bot_guild = bot.get_guild(bot_guild_id)


	# salons du bot
	bot.channels["bot_channel"] = bot.bot_guild.get_channel(bot_channel_id)
	bot.channels["announce_channel"] = bot.bot_guild.get_channel(announce_channel_id)
	bot.channels["general_channel"] = bot.bot_guild.get_channel(general_channel_id)
	bot.channels["welcome_channel"] = bot.bot_guild.get_channel(welcome_channel_id)
	bot.channels["control_channel"] = bot.bot_guild.get_channel(control_channel_id)
	bot.channels["error_channel"] = bot.bot_guild.get_channel(error_channel_id)


	# rôles du serveur
	bot.bot_guild_roles = await bot.bot_guild.fetch_roles()


	# membres du serveur principal
	bot.members = CustomDict({})
	for member in bot.bot_guild.members :
		bot.members[member] = {"name" : member.name,
							   "id"   : int(str(member).split("#")[1])}


	# jeux de la liste
	print(f"Openning {bot.games_file}.")
	with open(bot.games_file, "rt") as f_games :
		bot.games = CustomDict(json.load(f_games))


	# prochain événement
	print(f"Openning {bot.event_file}.")
	with open(bot.event_file, "rt") as f_event :
		bot.next_event = CustomDict(json.load(f_event))


	# message d'annonce
	print(f"Openning {bot.msg_file}.")
	with open(bot.msg_file, "rt") as f_msg :
		bot.announce_msg_id = int(f_msg.read())
	if bot.announce_msg_id != 0 :
		bot.announce_msg = await bot.channels["announce_channel"].fetch_message(bot.announce_msg_id)
		print(f"announce_msg : {bot.announce_msg.content}")
	else :
		print("No announce message.")


	# réactions au message d'annonce
	bot.next_event["participants"] = [bot.next_event["host"]]
	if bot.announce_msg_id != 0 :
		for reaction in bot.announce_msg.reactions :
			if reaction.emoji == "👍" :
				async for user in reaction.users() :
					if user.id != bot.find_member(bot.next_event["host"]).id :
						bot.next_event["participants"].append(str(user))
	bot.write_event()


	print(f"bot-guild : {bot.bot_guild}")
	print(f"bot-channel : {bot.channels['bot_channel'].name}")
	print(f"general-channel : {bot.channels['general_channel'].name}")
	print(f"welcome-channel : {bot.channels['welcome_channel'].name}")
	print(f"control-channel : {bot.channels['control_channel'].name}")
	print(f"error-channel : {bot.channels['error_channel'].name}")

	print(f"{bot.user.display_name} est prêt.")


@bot.event
async def on_member_join(member) :

	# on vérifie que le member vient de rejoindre le server bot_guild (le même bot peut être actif sur plusieurs serveurs)
	if member in bot.bot_guild.members and not(member in bot.members) :

		await bot.channels["welcome_channel"].send(f"Bienvenue {member.display_name} ! On espère que tu as amené des jeux ! :game_die: :black_joker:")

		bot.members[member] = {"name" : member.name,
							   "id"   : int(str(member).split("#")[1])}


@bot.event
async def on_member_remove(member) :

	# on vérifie que le member vient de quitter le serveur bot_guild
	if member in bot.members and not(member in bot.bot_guild.members) :

		bot.members.pop(member)


@bot.event
async def on_raw_reaction_add(payload) :
	if payload.message_id == bot.announce_msg_id :
		if payload.emoji.name == "👍" :

			# bot.announce_msg est une image figée d'un message, il faut "reload" ce message quand une réaction est ajoutée ou supprimée pour pouvoir voir cette réaction
			bot.announce_msg = await bot.channels["announce_channel"].fetch_message(bot.announce_msg_id)

			reaction = bot.find_reaction(bot.announce_msg, payload.emoji.name)

			# mise à jour de la liste de participants
			if reaction != None :
				bot.next_event["participants"] = [str(user) async for user in reaction.users()]
				if not(bot.next_event["host"] in bot.next_event["participants"]) :
					bot.next_event["participants"] = [bot.next_event["host"]] + bot.next_event["participants"]
			else :
				bot.next_event["participants"] = [bot.next_event["host"]]

			bot.write_event()

			if str(payload.member) != bot.next_event["host"] :
				await bot.channels["control_channel"].send(f"{payload.member} sera présent(e) à la prochaine soirée !")


@bot.event
async def on_raw_reaction_remove(payload) :
	if payload.message_id == bot.announce_msg_id :
		if payload.emoji.name == "👍" :

			# bot.announce_msg est une image figée d'un message, il faut "reload" ce message quand une réaction est ajoutée ou supprimée pour pouvoir voir cette réaction
			bot.announce_msg = await bot.channels["announce_channel"].fetch_message(bot.announce_msg_id)

			reaction = bot.find_reaction(bot.announce_msg, payload.emoji.name)

			participants_old = bot.next_event["participants"]

			# mise à jour de la liste de participants
			if reaction != None :
				bot.next_event["participants"] = [str(user) async for user in reaction.users()]
				if not(bot.next_event["host"] in bot.next_event["participants"]) :
					bot.next_event["participants"] = [bot.next_event["host"]] + bot.next_event["participants"]
			else :
				bot.next_event["participants"] = [bot.next_event["host"]]

			# recherche du membre qui a supprimé la réaction
			member = ""
			for str_user in participants_old :
				if not(str_user in bot.next_event["participants"]) :
					member = str_user

			bot.write_event()

			if member != "" :
				await bot.channels["control_channel"].send(f"Finalement, {member} ne pourra pas venir à la soirée")


@bot.event
async def on_command_error(ctx, error) :
	if isinstance(error, discord.ext.commands.errors.CommandNotFound) :
		await ctx.channel.send(f"Je ne connais pas cette commande")
		await asyncio.sleep(5)
		await ctx.channel.purge(limit=2)
	elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument) :
		await ctx.channel.send(f"Il manque des arguments : tappe !h <commande> pour voir comment utiliser cette commande")
		await asyncio.sleep(5)
		await ctx.channel.purge(limit=2)
	elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown) :
		await ctx.channel.purge(limit=1)
	else :
		await ctx.channel.send(f"{ctx.author.display_name} a réussi à provoquer une nouvelle erreur, bien joué ! (eh oui, j'ai bien suivi les cours de MB de Yvan Courbon, c'est le client qui s'occupe de débugger mon code)")
		await bot.channels["error_channel"].send(f"error : {error}")
		sys.exit()
	await bot.channels["error_channel"].send(f"error : {error}")
