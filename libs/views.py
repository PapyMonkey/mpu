import discord

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(
        label="Click me!",
        style=discord.ButtonStyle.blurple,
        emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked
    @discord.ui.button(
        label="Don't click me!",
        style=discord.ButtonStyle.grey,
        emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback_2(self, button, interaction):
        await interaction.response.send_message("I SAID NO!") # Send a message when the button is clicked

class DropdownSelectMovie(discord.ui.View):
    @discord.ui.button(
        label="Click me!",
        style=discord.ButtonStyle.blurple,
        emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked
    @discord.ui.button(
        label="Don't click me!",
        style=discord.ButtonStyle.grey,
        emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback_2(self, button, interaction):
        await interaction.response.send_message("I SAID NO!") # Send a message when the button is clicked
