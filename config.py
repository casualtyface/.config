# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import colors
import os
import re
import socket
import subprocess
from typing import Callable
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
alt = "mod1"              # Sets alt key to mod1
myTerm = "alacritty"      # My terminal of choice
myBrowser = "librewolf"   # My browser of choice
myFileManager = "nemo"
# myEmacs = "emacsclient -c -a 'emacs' " # The space at the end is IMPORTANT!


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(myTerm), desc="Launch terminal"),
    Key([mod], "c", lazy.spawn(myFileManager), desc="Launch filemanager"),
    Key([mod], "w", lazy.spawn(myBrowser), desc="Launch browser"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "mod1"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "mod1"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([alt], "Shift_L",  lazy.widget["keyboardlayout"].next_keyboard()),
    Key([mod], "space", lazy.spawn("rofi -show run"), desc="Spawn a rofi using a prompt widget"),
]

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]

#group_labels = ["DEV", "WWW", "SYS", "DOC", "VBOX", "CHAT", "MUS", "VID", "GFX",]
group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
#group_labels = ["", "", "", "", "", "", "", "", "",]


group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]


for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )



### COLORSCHEME ###
# Colors are defined in a separate 'colors.py' file.
# There 10 colorschemes available to choose from:
# colors = colors.doom_one
# colors = colors.dracula
# colors = colors.gruvbox_dark
# colors = colors.monokai_pro
# colors = colors.nord
# colors = colors.oceanic_next
# colors = colors.palenight
# colors = colors.solarized_dark
# colors = colors.solarized_light
# colors = colors.tomorrow_night
colors = colors.tokyonight["night"]

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": colors["cyan"],
                "border_normal": colors["blue"]
                }


layouts = [
    #layout.Bsp(**layout_theme),
    #layout.Floating(**layout_theme)
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    #layout.MonadWide(**layout_theme),
    layout.Max(
         border_width = 0,
         margin = 0,
         ),
    layout.Stack(**layout_theme, num_stacks=2),
    layout.Columns(**layout_theme),
    layout.TreeTab(
         font = "Ubuntu Bold",
         fontsize = 11,
         border_width = 0,
         bg_color = colors["fg"],
         active_bg = colors["bg"],
         active_fg = colors["fg"],
         inactive_bg = colors["bg"],
         inactive_fg = colors["fg"],
         padding_left = 8,
         padding_x = 8,
         padding_y = 6,
         sections = ["ONE", "TWO", "THREE"],
         section_fontsize = 10,
         section_fg = colors["fg"],
         section_top = 15,
         section_bottom = 15,
         level_shift = 8,
         vspace = 3,
         panel_width = 240
         ),
    layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 15,
    padding = 0,
    foreground = colors["fg"],
    background = colors["bg"],

)

extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.Image(
                 filename = "~/.config/qtile/icons/python-white.png",
                 scale = "False",
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)},
                 ),
        widget.Prompt(
                 font = "Ubuntu Mono",
                 fontsize=14,
                 foreground = colors["bg"]
        ),
        widget.GroupBox(
                 fontsize = 14,
                 margin_y = 3,
                 margin_x = 4,
                 padding_y = 2,
                 padding_x = 3,
                 borderwidth = 3,
                 active = colors["white1"],
                 inactive = colors["fg"],
                 rounded = False,
                 highlight_color = colors["black"],
                 highlight_method = "line",
                 this_current_screen_border = colors["light-yellow"],
                 this_screen_border = colors ["green"],
                 other_current_screen_border = colors["light-yellow"],
                 other_screen_border = colors["green"],
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors["fg"],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.CurrentLayoutIcon(
                 # custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                 foreground = colors["fg"],
                 padding = 0,
                 scale = 0.7
                 ),
        widget.CurrentLayout(
                 foreground = colors["fg"],
                 padding = 5
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors["fg"],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.WindowName(
                 foreground = colors["fg"],
                 max_chars = 40
                 ),
        widget.GenPollText(
                 update_interval = 300,
                 func = lambda: subprocess.check_output("printf $(uname -r)", shell=True, text=True),
                 foreground = colors["red"],
                 fmt = '❤  {}',
                 decorations=[
                     BorderDecoration(
                         colour = colors["red"],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.CPU(
                 format = '🏼  Cpu: {load_percent}%',
                 foreground = colors["green"],
                 decorations=[
                     BorderDecoration(
                         colour = colors["green"],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.Memory(
                 foreground = colors["blue"],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                 format = '{MemUsed: .0f}{mm}',
                 fmt = '🖥  Mem: {} used',
                 decorations=[
                     BorderDecoration(
                         colour = colors["blue"],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.DF(
                 update_interval = 60,
                 foreground = colors["yellow"],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e df')},
                 partition = '/',
                 #format = '[{p}] {uf}{m} ({r:.0f}%)',
                 format = '{uf}{m} free',
                 fmt = '✇  Disk: {}',
                 visible_on_warn = False,
                 decorations=[
                     BorderDecoration(
                         colour = colors["yellow"],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.Volume(
                 foreground = colors["magenta"],
                 fmt = '🕫  Vol: {}',
                 decorations=[
                     BorderDecoration(
                         colour = colors["magenta"],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.KeyboardLayout(
                 foreground = colors["cyan"],
                 display_map = {'bg phonetic': 'BG'},
                 configured_keyboards = ['us','bg phonetic'],
                 fmt = '⌨  Kbd: {}',
                 decorations=[
                     BorderDecoration(
                         colour = colors["cyan"],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.Clock(
                 foreground = colors["blue"],
                 format = "⏱  %a, %b %d - %H:%M",
                 decorations=[
                     BorderDecoration(
                         colour = colors["blue"],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.Systray(padding = 3),
        widget.Spacer(length = 0),
                widget.TextBox(
                    text='',
                    mouse_callbacks= {
                        'Button1':
                        lambda: qtile.cmd_spawn(os.path.expanduser('~/.config/rofi/powermenu.sh'))
                    },
                    foreground = '#e39378',
                    padding = 1
                ),
        widget.Spacer(length = 8)
        ]
    return widgets_list


# I use 3 monitors which means that I need 3 bars, but some widgets (such as the systray)
# can only have one instance, otherwise it will crash.  So I define the follow two lists.
# The first one creates a bar with every widget EXCEPT index 15 and 16 (systray and spacer).
# The second one creates a bar with all widgets.
 
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    for widget in widgets_screen1:
        widget.fontsize = 17
    del widgets_screen1[22:23]   # Removes widgets 15 and 16 for bars on Monitors 1 + 3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    for widget in widgets_screen2:
        widget.fontsize = 21
    return widgets_screen2       # Monitor 2 will display ALL widgets in widgets_list

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), background="#00000000", size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=35))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), lazy.window.focus(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors["cyan"],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.pic
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(title="branchdialog"),      # gitk
        Match(title='Confirmation'),      # tastyworks exit box
        Match(title='Qalculate!'),        # qalculate-gtk
        Match(wm_class='kdenlive'),       # kdenlive
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(title="pinentry"),          # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
