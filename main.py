import discord, asyncio, os
from utils import get_current_game, is_open
import datetime
from discord.ext import commands
from active_games import active_games
from game_room import Game_room
from ready_game import ready_game
from start_round import *


token = open("token.txt", 'r').read()
game = discord.Game(f"!명령어: 사용할 수 있는 명령어 목록 출력")
bot = commands.Bot(command_prefix='!', 
                    status=discord.Status.online, activity=game)

with open('src/black_and_white.png', 'rb') as f:
    image = f.read()

@bot.command()
async def 명령어(ctx):
    if str(ctx.channel.type) == 'private':
        return
    await ctx.send("""
!명령어 : 사용할 수 있는 명령어 목록을 출력합니다.
!규칙 : 게임의 규칙을 보여줍니다.
!시작 : 참가할 수 있는 게임을 만듭니다. 같은 채널에 이미 시작한 게임이 있다면 사용할 수 없습니다.
!참가 : 시작한 게임에 참가합니다. 시작한 게임이 존재하지 않거나 게임이 마감된 상태라면 사용할 수 없습니다.
!마감 : 참가를 마감하고 게임을 시작하기 위한 명령어입니다. 마감되지 않은 게임이 없다면 사용할 수 없습니다.
!리셋 : 진행 중인 게임을 초기화합니다. 새로운 게임을 시작할 수 있는 상태가 됩니다.
    """, reference=ctx.message)

@bot.command()
async def 규칙(ctx):
    if str(ctx.channel.type) == 'private':
        return
    await ctx.send('https://www.youtube.com/watch?v=F0X8JbX4Mjk&t=2s', reference=ctx.message)
    await ctx.send("""
1. 게임 대상자 2명은 0~8까지 9장의 숫자타일을 지급받는다.
2. 9개의 숫자타일은 흑색, 백색으로 나뉘며 0, 2, 4, 6, 8은 흑색, 1, 3, 5, 7은 백색 타일로 구성되어 있다.
3. 1라운드의 선플레이어는 랜덤으로 결정하며, 2라운드부터는 전 라운드에 승리한 플레이어가 선 플레이어가 된다.
4. 선 플레이어가 0~8까지의 숫자타일 중 1개를 뒷면이 보이도록 제시한 뒤, 후 플레이어가 타일을 제시한다.
5. 제시된 타일은 딜러만 확인하며, 둘 중 더 높은 숫자타일을 제시한 플레이어가 승리 승점을 획득한다.
6. 상대가 어떤 숫자타일을 냈는지는 승패가 결정된 후에도 공개되지 않는다.
7. 즉 플레이어들은 자신이 낸 숫자타일과 흑, 백으로 나뉜 타일로 상대방의 남은 타일을 유추해 게임을 진행해야 한다.
8. 9번의 대결 결과, 승점이 더 높은 플레이어가 승자가 된다.
    """, reference=ctx.message)
    

@bot.command()
async def 시작(ctx):
    if str(ctx.channel.type) == 'private':
        return
    if ctx.channel.id in active_games:
        await ctx.send("이미 시작한 게임이 존재합니다.")
        return
    print(f"{datetime.datetime.now()} : <start> {ctx.channel.id}")
    current_game = {
        'game_room': Game_room()
    }
    active_games[ctx.channel.id] = current_game
    room_info = current_game['game_room']
    room_info.main_channel = ctx
    room_info.members.append(ctx.message.author)
    room_info.can_join = True
    embed = discord.Embed(title="흑과백 게임에 오신 것을 환영합니다!",
                          description="흑과백은 숫자 타일을 제시해 높은 숫자를 낸 플레이어가 승점을 획득하는 게임입니다. 상대방의 심리를 파악하세요!") 
    embed.add_field(
        name="참가 방법", value="게임에 참가하고 싶다면 !참가를 입력해주세요.", inline=False)
    await bot.change_presence(activity=discord.Game(name=f"{len(active_games)}개 게임"))
    await ctx.send(embed=embed)

@bot.command()  
async def 참가(ctx):
    if str(ctx.channel.type) == 'private':
        return
    room_info = await is_open(ctx)
    if not room_info:
        return

    player = ctx.message.author
    if player not in room_info.members:
        room_info.members.append(player)
        await ctx.send("{}님이 참가하셨습니다. 게임을 시작하려면 !마감을 입력해주세요.".format(player.name), reference=ctx.message)
        print("join")
    else:
        await ctx.send("{}님은 이미 참가중입니다.".format(player.name), reference=ctx.message)

@bot.command()
async def 마감(ctx):
    if str(ctx.channel.type) == 'private':
        return
    if ctx.channel.id not in active_games:
        await ctx.send("시작한 게임이 존재하지 않습니다.", reference=ctx.message)
        return

    current_game = active_games[ctx.channel.id]
    if len(current_game['game_room'].members) < 2:
        await ctx.send("플레이어 수가 2명 이하입니다. 게임을 시작할 수 없습니다.", reference=ctx.message)
        return

    if not current_game['game_room'].can_join:
        await ctx.send("게임이 이미 시작되었습니다.", reference=ctx.message)
        return
    current_game['game_room'].can_join = False
    current_game['game_room'].start = True
    await ctx.send("참가가 마감되었습니다.", reference=ctx.message)
    await ready_game(current_game)
    await start_round(current_game)
    print("close")

@bot.command()
async def 리셋(ctx):
    if str(ctx.channel.type) == 'private':
        return
    if ctx.channel.id not in active_games:
        await ctx.send("시작한 게임이 존재하지 않습니다.", reference=ctx.message)
        return
    del active_games[ctx.channel.id]
    await bot.change_presence(activity=discord.Game(name=f"{len(active_games)}개 게임"))
    await ctx.send("진행하는 게임을 중단합니다.", reference=ctx.message)
    print("reset")

@bot.event
async def on_ready():
    await bot.user.edit(avatar=image)

    # print 예제
    discord_py="discord.py"
    dis="discord"
    api="API"
    namuwiki="나무위키"
    print(f"{discord_py}는 {dis}의 {api}입니다. {discord_py} 문서는 {namuwiki}에서 만들어졌습니다.")

# event 추가 예정
# @bot.event
# async def on_message(message):
#     if message.author.bot:
#         return
#     if message.channel.id not in active_games:
#         return
    
#     room_info = active_games[message.channel.id]['game_room']
#     if not room_info.start:
#         return

#     if message.author not in room_info.members:
#         return





# async 예제
# 지울 예정
@bot.command(aliases=['안녕', 'hi', '안녕하세요'])
async def hello(ctx):
    await ctx.send(f'{ctx.author.mention}님 안녕하세요!')

@bot.command(name="반응")
async def get_reaction_and_react(ctx):
    msg = await ctx.send("1, 2, 3 반응 중 2 반응을 달아주세요.")
    reaction_list = ['1️⃣', '2️⃣', '3️⃣']
    for r in reaction_list:
        await msg.add_reaction(r)
    def check(reaction, user):
        return str(reaction) in reaction_list and user == ctx.author and reaction.message.id == msg.id


@bot.event
async def on_raw_reaction_add(payload):
    current_game = get_current_game(payload.user_id)
    room_info = current_game['game_room'] if current_game else None
    game_status = current_game['game_status'] if current_game and 'game_status' in current_game else None

    # 1. 플레이어가 들어가 있는 게임 정보가 있을 때만 반응한다
    if not (room_info and game_status):
        return

    # 2. 해당 플레이어의 차례가 아니면 무시해야함
    if payload.user_id != game_status.first_player.id and game_status.turn == -1:
        return
    if payload.user_id != game_status.second_player.id and game_status.turn == 1:
        return

    # 3. DM으로 받는게 아니면 무시해야함.
    channel = await bot.fetch_channel(payload.channel_id)
    if str(channel.type) == 'text':
        return

    # 4. 잘못된 이모지를 받으면 무시
    if str(payload.emoji) not in room_info.emojis.keys():
        print("Wrong emoji")
        return   

    tile_num = room_info.emojis[str(payload.emoji)]

    for member in room_info.members:
        if payload.user_id == member.id:
            if tile_num in game_status.numeric_tiles[member]:
                print(tile_num)
                game_status.game_results[member].append(tile_num)
                game_status.numeric_tiles[member].remove(tile_num)

                if tile_num % 2 == 0:  # 흑색 타일
                    tile_info = '흑색'
                    tile_color = 0x000000
                else:
                    tile_info = '백색'
                    tile_color = 0xFFFFFF
                
                embed = discord.Embed(title=f"{room_info.members[0].name} {game_status.scores[room_info.members[0]]} {game_status.round}R {game_status.scores[room_info.members[1]]} {room_info.members[1].name}", color=tile_color)
                
                # 조건문 추가해야. 선 플레이어가 이모지를 넣을 경우와 후 플레이어가 이모지를 넣을 경우 구분
                # 1. 선 플레이어가 이모지를 넣었을 경우
                if game_status.turn == -1:
                    embed.add_field(name=f"{game_status.first_player.name}님이 제시한 타일의 색은 {tile_info}입니다.", 
                                    value=f"이어서 {game_status.second_player.name}님 께서는 타일을 제시해주시기 바랍니다.", inline=False)
                    
                    game_status.turn *= -1
                    # file = discord.File("src/tiles.png", filename="tiles.png")
                    # embed.set_image(url="attachment://tiles.png")
                    await room_info.main_channel.send(embed=embed)
                    asyncio.ensure_future(decide_tile(room_info, game_status))
                else:
                    embed.add_field(name=f"{game_status.second_player.name}님이 제시한 타일의 색은 {tile_info}입니다.", 
                                    value=f"{game_status.round}라운드 결과 발표하겠습니다.", inline=False)
                    # 5초 쉬고
                    # time.sleep(5)
                    # 결과 발표

                    a = game_status.game_results[game_status.first_player][game_status.round-1]
                    b = game_status.game_results[game_status.second_player][game_status.round-1]
                    if a > b:
                        round_winner = game_status.first_player
                        round_loser = game_status.second_player
                    elif a < b:
                        round_winner = game_status.second_player
                        round_loser = game_status.first_player
                    else:
                        round_winner = None

                    if round_winner:
                        embed.add_field(name=f"{round_winner.name} 승", 
                                    value=f"{round_winner.name}님의 승리입니다.", inline=False)
                        game_status.scores[round_winner]+=1
                        game_status.first_player = round_winner
                        game_status.second_player = round_loser
                    else:
                        embed.add_field(name=f"무승부입니다.", 
                                    value=f"무승부로 라운드가 끝났기 때문에 다음 라운드에서 {game_status.first_player.name}님이 선 플레이어입니다", inline=False)

                    game_status.turn *= -1
                    await room_info.main_channel.send(embed=embed)
                    asyncio.ensure_future(start_round(current_game))
                    
                # embed = discord.Embed(title=f"선플레이어이신 {game_status.first_player.name}님이 제시한 타일의 색은 {tile_info}입니다.", 
                # description=f"이어서 {game_status.second_player.name}님 께서는 타일을 제시해주시기 바랍니다.", color=tile_color)
            else:
                embed = discord.Embed(title=f"{member.name}님이 가지고 있지 않은 타일입니다.",
                          description=f"""현재 가지고 있는 타일을 제시해주세요.""")
                                     
                await member.send(embed=embed)
                break


    # if str(payload.emoji) in room_info.emojis and room_info.emojis[str(payload.emoji)]:
    #     await judge_merlin(payload, current_game) if game_status.assassination else await add_teammate(payload, room_info.emojis[str(payload.emoji)], current_game)          
    # elif str(payload.emoji) in ["👍","👎"]:
    #     asyncio.ensure_future(vote(current_game, current_round, payload, lock_for_vote))
    # elif str(payload.emoji) in ["⭕", "❌"]:
    #     asyncio.ensure_future(try_mission(payload, current_round['team'], current_game, lock_for_mission))

# @bot.event
# async def on_raw_reaction_add(payload):
#     channel = await bot.fetch_channel(payload.channel_id)
#     message = await channel.fetch_message(payload.message_id)
#     await message.clear_reactions()

# @bot.event
# async def on_message(message):
#     if "안녕" in message.content:
#         await message.delete()
#         await message.channel.send(f"{message.author.mention} 님이 비속어를 사용하였습니다.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.message.content} 는 존재하지 않는 명령어입니다.")
        return
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f"엇! 제가 다른 분들에게 메세지를 보낼 수 없어요! 아마 제게 메세지를 발송할 권한이 주어지지 않은 것 같아요. 혹시 모르는 사람의 DM을 차단한 분이 계시지 않을까요?")
        return
    await ctx.send("오류가 발생하였습니다. !리셋을 통해 게임을 새로고침해주세요.")
    print(f"black_and_white - {datetime.datetime.now()} : <Error> {ctx.channel.id}, error: {error}")

bot.run(token)