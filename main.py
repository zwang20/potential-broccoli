import discord
import csv
import os

with open('token.txt', 'r') as f:
    TOKEN = f.read()

puzzle_answers = ['test1', 'test2', 'test3', 'test4', 'test5']


def change_file(userid, field, new):
    field_pos = {'userid': 0, 'solve1': 1, 'solve2': 2, 'solve3': 3, 'solve4': 4, 'solve5': 5}
    with open('users.csv', 'r') as old_file, open('updated_users.csv', 'w+') as new_file:
        for row in old_file:
            row_content = row.split(',')
            if row_content[0] == str(userid):
                row_content[field_pos[field]] = str(new)
                new_file.write(str(','.join(row_content)))
            else:
                new_file.write(row)
    os.remove('users.csv')
    os.rename('updated_users.csv', 'users.csv')


def check_user(userid, field):
    with open('users.csv', newline='') as users:
        for user in csv.DictReader(users):
            if int(user['userid']) == userid:
                return user[field]


def add_user(userid):  # will be changed
    with open('users.csv', newline='') as users:
        for user in csv.DictReader(users):
            if int(user['userid']) == userid:
                break
        else:
            with open('users.csv', 'a', newline='') as users:
                writer = csv.DictWriter(users, fieldnames=['userid', 'solve1', 'solve2', 'solve3', 'solve4', 'solve5'])
                writer.writerow({'userid': userid,
                                 'solve1': False,
                                 'solve2': False,
                                 'solve3': False,
                                 'solve4': False,
                                 'solve5': False})


def check_meta(userid):
    for i in range(5):
        if check_user(userid, 'solve{}'.format(str(i+1))):
            pass
        else:
            return False
    else:
        return True


class MyClient(discord.Client):
    @staticmethod
    async def on_ready():
        print('\nOnline')
        print('We have logged in as {0.user}'.format(client))

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        message.content = message.content.lower()
        message_words = message.content.split()
        add_user(message.author.id)

        if message.content.startswith('!'):
            if message.content == '!help':
                embed = discord.Embed(title="Help Page", color=0x000000)
                embed.add_field(name="!puzz[number] [answer]", value="Check the answer of your [number]th puzzle.",
                                inline=False)
                embed.add_field(name="!getmeta", value="Get the meta, if you've answered all 5 puzzles correctly!",
                                inline=False)
                await message.channel.send(embed=embed)

            elif message.content.startswith('!puzz'):
                puzzle_no = int(message_words[0][-1])
                if message_words[1] == puzzle_answers[puzzle_no-1]:
                    change_file(message.author.id, 'solve{}'.format(str(puzzle_no)), True)
                    embed = discord.Embed(color=0x00ff00)
                    embed.add_field(name="Correct!", value="Your answer to puzzle {} is correct!".format(puzzle_no),
                                    inline=False)
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(color=0xff0000)
                    embed.add_field(name="Incorrect.", value="Your answer to puzzle {} is incorrect.".format(puzzle_no),
                                    inline=False)
                    await message.channel.send(embed=embed)

            elif message.content.startswith('!getmeta'):
                if check_meta(message.author.id):
                    print("Congratulations! Here's the meta!")

            else:
                await message.channel.send("Use !help to see how to use this bot.")


client = MyClient()
client.run(TOKEN)