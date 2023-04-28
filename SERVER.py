import discord
import tools.config as config
from livebet import LiveBet
from bettinguser import *
from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed, Message, Member, Reaction, RawReactionActionEvent
from typing import List, Dict
from engines.bank import Bank
from tools.tools import *
from tools.emojis import *
from tools.config import *
from engines.betresolver import BetResolver
from engines.factchecker import FactChecker
from engines.googlelimiter import Counter

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, token=config.TOKEN)
#Liliane Bet-en-cours
# define a dictionary to store user balances
bank = Bank()
google_api_limiter = Counter()
BOT_ID = None

# define a list to store betting history
bet_history: List[Dict[int, LiveBet]] = {}

@bot.event
async def on_ready():
    channel = bot.get_channel(TESTING_CH_GENERAL)
    message = await channel.send(f'{BOT_NAME} is running.')
    set_bot_id(message.author.id)

def set_bot_id(id: int):
    global BOT_ID
    BOT_ID = id

def init_balance(user: Member):
    if user.id not in bank.balances:
        bank.balances[user.id] = float(INIT_BALANCE)
    
@bot.command(name='balance')
async def balance(ctx: Context):
    mentions = ctx.message.mentions
    if mentions:
        for mention in mentions:
            init_balance(mention.id)
            member_balance = bank.balances[mention.id]
            await ctx.channel.send(f'{mention.name}\'s balance is {member_balance}')
        return
    init_balance(ctx.author)
    member_balance = bank.balances[ctx.author.id]
    await ctx.channel.send(f'Your balance is {member_balance}')

@bot.command(name='bet')
async def bet(ctx: Context):
    bet = await make_bet_out_of_context(ctx)
    mentions = ctx.message.mentions
    if mentions:
        for user in mentions:
            init_balance(user)
            if user.id not in bet.betting_users:
                bet.add_main_bettor(user)
    bank.register_bet(bet)
    
@bot.command(name='resolve')
async def resolve(ctx: Context):
    message = ctx.message
    original_bet = get_bet_from_reply(message)
    
    if original_bet.is_resolved:
        await message.add_reaction(X_REACTION)
        return
    
    if message.reference is None or message.reference.resolved.author.name != BOT_NAME:
        return
    
    #HERE ADD START OF VOTED RESOLVE
    if original_bet.creator_id == message.author.id:
        resolve_claim_id = int(get_content_from_message(message, False))
        if BetResolver(original_bet.claims).resolve(resolve_claim_id):
            original_bet.bet_box.add_resolve_field(ctx, original_bet.get_claim(resolve_claim_id))
            return
        return
    await message.add_reaction(X_REACTION)
    

@bot.command(name='vote')
async def vote(ctx: Context):
    message = get_content_from_message(ctx.message, False)
    tokens = message.split(' ')
    if tokens[0] == 'resolve':
        
        return
    if tokens[0] == 'punish':
        try:
            amount = float(tokens[1])
            for mention in ctx.message.mentions:
                bank.balances[mention.id] -= amount
                await ctx.message.add_reaction()
            
        except Exception as e:
            await ctx.message.add_reaction(POOP_REACTION)
        return
    
    if tokens[0] == 'grace':
        
        return
    
    if tokens[0] == 'cancel':
        
        return
    pass
    
def add_to_balance(user_id: int, amount: float):
    bank.balances[user_id] += amount
    return

async def make_bet_out_of_context(ctx: Context) -> LiveBet:
    message = get_content_from_message(ctx.message, False)
    bet = LiveBet(ctx, message)
    await bet.init_boxes(ctx)
    return bet

async def claim_from_reply(message: Message):
    bet_message = message.reference.resolved
    bet = get_bet_from_reply(message)
    if bet.is_resolved:
        await message.add_reaction(X_REACTION)
        return
    user = message.author
    user_id = user.id
    betting_user = BettingUserFromMember(user)
    try:
        amount = get_amount_from_message(message)
        if user_id in bet.betting_users:
            await message.add_reaction(X_REACTION)
            return
        if amount > bank.balances[user.id]:
            await message.add_reaction(X_REACTION)
            await message.channel.send(f"You're too poor, {user.nick}.")
            return
        claim_text = get_content_from_message(message, True)
        if await bet.add_claim(claim_text, amount, betting_user):
            bank.balances[betting_user.id] -= amount
            await bet_message.edit(embed=bet.bet_box)
            await bet_message.add_reaction(INT_EMOJI_ENUM[bet.claim_count - 1])
        else:
            await message.add_reaction(X_REACTION)
    except Exception as e:
        await message.add_reaction(POOP_REACTION)
        raise e

def get_bet_from_reply(message: Message) -> LiveBet:
    #TODO: MAKE SURE WE ONLY TREAT REPLIES TO BETS
    message = message.reference.resolved
    if message.embeds:
        return bank.get_bet_from_message_id(message.id)
    raise Exception

async def numerical_reaction_handle(reaction: Reaction, user: Member):
    if reaction.message.id in bank.votebox_message_id:
        print("ADD VOTE")
        pass
    else:
        index = INT_EMOJI_ENUM.index(reaction.emoji)
        bet = bank.get_bet_from_message_id(reaction.message.id)
        if bet.is_resolved or user.id in bet.betting_users:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return
        betting_user = BettingUser(user.id, user)
        init_balance(user)
        if bet.add_minor_bettor(betting_user, index):
            bank.balances[betting_user.id] -= bet.get_claim(index).minor_amount
        pass

@bot.event
async def on_message(message: Message):
    init_balance(message.author)
    if len(message.content) > 0 and message.content[0] == '!':
        await bot.process_commands(message)
        return
    if message.reference is None or message.reference.resolved.author.name != BOT_NAME:
        return
    if message.reference.resolved.author.name == BOT_NAME:
        await claim_from_reply(message)
        return
    bot.process_commands(message)
    
@bot.event
async def on_command_error(ctx: Context, error):
    if isinstance(error, commands.errors.UserInputError):
        await ctx.message.add_reaction(POOP_REACTION)
        if ctx.command.name == 'bet':
            await ctx.message.reply("To initiate a bet: ```!bet \"Je parie que Quentin est capable de manger 100 nuggets en une heure.\" (optionnal): @user1 @user2 @user3```")
        if ctx.command.name == 'claim':
            await ctx.message.reply("To make a claim on a bet: ```!claim \"Je pense que Quentin est incapable de manger 100 nuggets en une heure.\" 3000 ru6r0VnR -> (Bet code)```If a claim already exists, you need to join the bet on a already existing claim, by reacting with the claim's number.")

@bot.event
async def on_reaction_add(reaction: Reaction, user: Member):
    message_id = reaction.message.id
    original_message_author_id = reaction.message.author.id
    if original_message_author_id == BOT_ID and user.id != BOT_ID:
        bet = bank.get_bet_from_message_id(message_id)
        if reaction.emoji in INT_EMOJI_ENUM:
            await numerical_reaction_handle(reaction, user)      
        if reaction.emoji == SEARCH_REACTION:
            if bet.is_resolved or bet.is_searched or not google_api_limiter.can_search_google():
                await reaction.message.remove_reaction(reaction.emoji, user)
                return
            await bet.display_result()
            bet.is_searched = True
        pass

@bot.event
async def on_raw_reaction_remove(event: RawReactionActionEvent):
    channel = bot.get_channel(event.channel_id)
    message = await channel.fetch_message(event.message_id)
    bet_id = message.id
    if event.user_id != BOT_ID and bet_id in bank.bets:
        if event.emoji.name in INT_EMOJI_ENUM:
            index = INT_EMOJI_ENUM.index(event.emoji.name)
            bet = bank.get_bet_from_message_id(message.id)
            co_id = [c.owner.id for c in bet.claims]
            if not bet.is_resolved and event.user_id not in co_id:
                betting_user = BettingUser(event.user_id, event.member)
                bet.remove_minor_bettor(betting_user, index)
                bank.balances[betting_user.id] =+ bet.get_claim(index).minor_amount

bot.run(token=config.TOKEN)