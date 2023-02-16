from channel_commands import *
import sys

@bot.command(name="msg")
async def msg_game(ctx, channel: str, msg: str) :
	if bot.control_channel(ctx) :
		if msg.startswith("```") and msg.endswith("```") :
			msg = msg[3:-3]
		await bot.channels[channel].send(msg)

@bot.command(name="test")
async def test_game(ctx) :
	if bot.control_channel(ctx) :
		await bot.channels["control_channel"].send(f"Tout va bien pour moi, merci ! :slight_smile:")

@bot.command(name="dumpm")
async def dumpmembers_game(ctx) :
	if bot.control_channel(ctx) :
		res = ""
		for member in bot.members :
			res += f"{member}\n"
		await bot.channels["control_channel"].send(res)

@bot.command(name="kill")
async def kill_game(ctx) :
	if bot.control_channel(ctx) :
		sys.exit()

@bot.command(name="clean")
async def clean_game(ctx, channel: str, n: str) :
	if bot.control_channel(ctx) :
		await bot.channels[channel].purge(limit=int(n))


#=============# Gestion des événements #=============#

"""
bot.next_event = {
	"date" : str,
	"participants" : List[str],
	"host" : str,
	"announced" : bool
}

bot.announce_msg : discord.Message
bot.announce_msg_id : int
"""


@bot.command(name="evdate")
async def evdate_game(ctx, date: str) :
	if bot.control_channel(ctx) :
		if not(bot.next_event["announced"]) :
			event = {
				"date" : date,
				"participants" : [str(ctx.author)],
				"host" : str(ctx.author),
				"announced" : False
			}
			bot.next_event = CustomDict(event)
			bot.write_event()
			await ctx.channel.send("C'est bon !")
		else :
			await ctx.channel.send("L'événement a déjà été annoncé, supprime-le avant de modifier la date")

@bot.command(name="evshow")
async def event_game(ctx) :
	if bot.control_channel(ctx) :
		if bot.next_event["date"] != "" :
			res = f"Next event ==================\n"
			for elt in bot.next_event :
				res += f"**{elt}** : {bot.next_event[elt]}\n"
			await ctx.channel.send(res)
		else :
			await ctx.channel.send("Aucun événement enregistré")


@bot.command(name="evannounce")
async def evannounce_game(ctx) :
	if bot.control_channel(ctx) :
		if bot.next_event["date"] != "" :
			if not(bot.next_event["announced"]) :
				announce_msg_txt = f"""
Hello @everyone !
La prochaine soirée jeux arrive, elle est prévue pour {'le ' if re.match(r'.*[0-9].*', bot.next_event['date']) else ''}{bot.next_event['date']} !
Si tu souhaites venir jouer avec nous, réagis avec :+1:.
"""
				bot.next_event["announced"] = True
				bot.write_event()
				bot.announce_msg = await bot.channels["announce_channel"].send(announce_msg_txt)
				bot.announce_msg_id = bot.announce_msg.id
				with open(bot.msg_file, "wt") as f_msg :
					f_msg.write(str(bot.announce_msg_id))
			else :
				await ctx.channel.send("L'événement a déjà été annoncé")
		else :
			await ctx.channel.send("Définis d'abord un événement")


@bot.command(name="evdel")
async def evdel_game(ctx, done: str) :
	if bot.control_channel(ctx) :
		if bot.next_event["date"] != "" :
			if bot.next_event["announced"] :
				if done != "done" :
					cancel_msg = "Hello "
					for member in bot.next_event["participants"] :
						cancel_msg += f"{bot.find_member(member).mention} "
					cancel_msg += f" !\nMalheureusement, la soirée {'du' if re.match(r'.*[0-9].*', bot.next_event['date']) else 'de'} {bot.next_event['date']} ne pourra pas avoir lieu :pensive:\nJ'espère pouvoir la remplacer très vite !"
					await bot.channels["announce_channel"].send(cancel_msg)
				bot.announce_msg = None
				bot.announce_msg_id = 0
				with open(bot.msg_file, "wt") as f_msg :
					f_msg.write(str(bot.announce_msg_id))
			bot.next_event = {
				"date" : "",
				"participants" :[],
				"host" : "",
				"announced" : False
			}
			bot.write_event()