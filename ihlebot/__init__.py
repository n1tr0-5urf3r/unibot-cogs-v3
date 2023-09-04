from .ihlebot import Ihlebot

async def setup(bot):
    await bot.add_cog(Ihlebot(bot))
