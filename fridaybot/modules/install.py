import asyncio
import os
from pathlib import Path
from fridaybot.utils import friday_on_cmd, load_module
from fridaybot.function import get_all_modules
from fridaybot import CMD_HELP

DELETE_TIMEOUT = 5


@friday.on(friday_on_cmd(pattern="install"))
async def install(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        sedplugin = await event.get_reply_message()
        try:
            downloaded_file_name = await event.client.download_media(
                sedplugin,
                "fridaybot/modules/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit(
                    "Friday Has Installed `{}` Sucessfully.".format(
                        os.path.basename(downloaded_file_name)
                    )
                )
            else:
                os.remove(downloaded_file_name)
                await event.edit(
                    "Errors! This plugin is already installed/pre-installed."
                )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(
                f"Error While Installing This Plugin, Please Make Sure That its py Extension. \n**ERROR :** {e}"
            )
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()
    
#    Copyright (C) FridayDevs 2020-2021
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

@borg.on(friday_on_cmd(pattern='pl ?(.*)'))
async def _(event):
    if event.fwd_from:
        return
    lul = event.pattern_match.group(1)
    yesm, nope, total_p = await get_all_modules(event, borg, lul)
    await event.edit(f"Installed {yesm} PLugins. Failed To Install {nope} Plugins And There Were Total {total_p} Plugins")
    
CMD_HELP.update(
    {
        "install": "**Install**\
\n\n**Syntax : **`.install <reply to plugin>`\
\n**Usage :** it installs replyed plugin"
    }
)
