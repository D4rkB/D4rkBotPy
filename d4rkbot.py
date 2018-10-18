import discord, random, asyncio

client = discord.Client()
players = {}
queue = []
COR = 0xF7FE2E
musicatual = ''


async def check_queue(id, sv, message):
    global musicatual
    if len(queue) != 1:
        del queue[0]
        voice = client.voice_client_in(sv)
        player = await voice.create_ytdl_player(queue[0])
        players[id].stop()
        players[id] = player
        player.start()
        if message.content.lower() == '-s' or message.content.lower() == '-skip':
            matual = musicatual
            musicatual = player.title
            mscskip = discord.Embed(
                title="\n",
                color=COR,
                description='A música **{}** foi pulada e agora está a tocar a música **{}**'.format(matual, musicatual)
            )
            await client.send_message(message.channel, embed=mscskip)
        await asyncio.sleep(player.duration)
        await check_queue(id, sv, message)
    else:
        del queue[0]
        can = client.voice_client_in(sv)
        await asyncio.sleep(10)
        await can.disconnect()


def randcor():
    global COR
    COR = random.randint(0x00000, 0xFFFFFF)
    return COR


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='D4rkB', type=3))
    print('Bot Online!')
    print(client.user.name)
    print(client.user.id)
    print('------------------')


@client.event
async def on_member_join(member):
    canal = client.get_channel('498504505336266752')
    msg = f'Bem Vindo! {member.mention}'
    await client.send_message(canal, msg)


@client.event
async def on_member_remove(member):
    canal = client.get_channel('498504505336266752')
    msg = f'Adeus! {member.mention}'
    await client.send_message(canal, msg)


@client.event
async def on_message(message):
    global musicatual
    if message.content.lower() == '-help' or message.content.lower() == '-ajuda':
        await client.send_message(message.channel, '---------AJUDA--------- \n'
                                                   '-moeda - Jogar cara/coroa comigo \n'
                                                   '-entrar - Entro no teu canal de voz \n'
                                                   '-sair - Saio do canal de voz em que estou \n'
                                                   '-play - Procura uma música no youtube e toca-a \n'
                                                   '-pause - Pausa a música que estiver a dar \n'
                                                   '-resume - Tira o pause da música\n'
                                                   '-skip - Salta a música\n'
                                                   '-info - Informações sobre mim')
    elif message.content.lower() == '-moeda':
        choice = random.randint(1, 2)
        if choice == 1:
            await client.add_reaction(message, '😀')
        else:
            await client.add_reaction(message, '👑')

    elif message.content.lower() == '-entrar':
        try:
            canal = message.author.voice.voice_channel
            await client.join_voice_channel(canal)
        except discord.InvalidArgument:
            await client.send_message(message.channel, 'Precisas de estar num canal de voz para usar este comando!')

    elif message.content.lower() == '-sair':
        try:
            canal = client.voice_client_in(message.server)
            await canal.disconnect()
            queue.clear()
        except AttributeError:
            await client.send_message(message.channel, 'Eu não estou em nenhum canal de voz!')

    elif message.content.lower().startswith('-play ') or message.content.lower().startswith('-p '):
        if message.content.lower().startswith('-play'):
            yt_url = message.content[6:]
        else:
            yt_url = message.content[3:]
        if client.is_voice_connected(message.server):
            try:
                voice = client.voice_client_in(message.server)
                if yt_url.startswith('http'):
                    player = await voice.create_ytdl_player(yt_url)
                    queue.append(yt_url)
                else:
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    queue.append('ytsearch: {}'.format(yt_url))
                if len(queue) == 0:
                    players[message.server.id].stop()
                    players[message.server.id] = player
                    player.start()
                    musicatual = player.title
                    mscemb = discord.Embed(
                        title="Música para tocar:",
                        color=randcor()
                    )
                    mscemb.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                    mscemb.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                    mscemb.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                    mscemb.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb.add_field(name="Dislikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb)
                else:
                    mscemb3 = discord.Embed(
                        title="Música adicionada na lista:",
                        color=randcor()
                    )
                    mscemb3.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb3.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb3.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                    mscemb3.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                    mscemb3.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                    mscemb3.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb3.add_field(name="Dislikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb3)
            except discord.InvalidArgument:
                await client.send_message(message.channel, 'Precisas de estar num canal de voz para usar este comando!')
            except Exception as e:
                    await client.send_message(message.server, "Erro: [{error}]".format(error=e))

        if not client.is_voice_connected(message.server):
            try:
                channel = message.author.voice.voice_channel
                voice = await client.join_voice_channel(channel)
                if yt_url.startswith('http'):
                    player = await voice.create_ytdl_player(yt_url)
                    queue.append(yt_url)
                else:
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    queue.append('ytsearch: {}'.format(yt_url))
                players[message.server.id] = player
                player.start()
                musicatual = player.title
                mscemb2 = discord.Embed(
                    title="Música para tocar:",
                    color=randcor()
                )
                mscemb2.add_field(name="Nome:", value="`{}`".format(player.title))
                mscemb2.add_field(name="Visualizações:", value="`{}`".format(player.views))
                mscemb2.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                mscemb2.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                mscemb2.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                mscemb2.add_field(name="Likes:", value="`{}`".format(player.likes))
                mscemb2.add_field(name="Dislikes:", value="`{}`".format(player.dislikes))
                await client.send_message(message.channel, embed=mscemb2)
                await asyncio.sleep(player.duration)
                if musicatual == player.title:
                    await check_queue(message.server.id, message.server, message)
            except discord.InvalidArgument:
                await client.send_message(message.channel, 'Precisas de estar num canal de voz para usar este comando!')
            except Exception as error:
                await client.send_message(message.channel, "Erro: [{error}]".format(error=error))
    elif message.content.startswith('-pause'):
        try:
            players[message.server.id].pause()
            mscpause = discord.Embed(
                title="\n",
                color=COR,
                description="Musica pausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscpause)
        except KeyError:
            await client.send_message(message.channel, "Não há nenhuma música a tocar!")
        except Exception as error:
            await client.send_message(message.channel, "Erro: [{error}]".format(error=error))
    elif message.content.startswith('-resume'):
        if client.is_voice_connected(message.server) and len(queue) != 0:
            try:
                mscresume = discord.Embed(
                    title="\n",
                    color=COR,
                    description="Musica a continuar!"
                )
                await client.send_message(message.channel, embed=mscresume)
                players[message.server.id].resume()
            except Exception as error:
                await client.send_message(message.channel, "Erro: [{error}]".format(error=error))
        else:
            mcresume2 = discord.Embed(
                title="\n",
                color=COR,
                description="Não há nenhuma música a tocar!"
            )
            await client.send_message(message.channel, embed=mcresume2)
    elif message.content.lower() == '-s' or message.content.lower() == '-skip':
        await check_queue(message.server.id, message.server, message)

    elif message.content.lower() == '-info' or message.content.lower() == '-credits':
        mscinfo = discord.Embed(
            title='Info',
            color=COR,
            description='Linguagem de programação usada - **Python 3.6**\n'
                        'Bibliotecas usadas - **discord.py**, **random**, **asyncio**\n'
                        'Autor - **D4rkB**\n'
                        #'Curiosidade: Linhas de código - **228** e a aumentar.. :D\n'
                        '-help para **ver todos os comandos**'
        )
        await client.send_message(message.channel, embed=mscinfo)
client.run('TOKEN')