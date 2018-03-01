import re

bot_prefix = "[Aa]drij [:,]? *"
gooey_prefix = "^\[(slack|discord)\] (?P<nick>.+?): *"
gooey_preprocessor = re.compile(gooey_prefix + "(?P<msg>.*)$")
# Greeting using hello/hi
greeter = re.compile(bot_prefix + "[Hh](ello|i)")
# Reply with pong to ping
ping = re.compile(bot_prefix + "[Pp](ing|ING)")
# Disconnect message
exit = re.compile(bot_prefix + "[Tt]ime +to +go +to +bed")
# Random regarding options
random_float = re.compile(bot_prefix + "[Rr](ANDOM|andom)")
random_dice = re.compile(
    bot_prefix + "([Tt](HROW|hrow) +)?([Tt](HE|he)|[Aa] +)?[Dd](ICE|ice)")
# Tell the time, timezone
time = re.compile(bot_prefix + "time([:,]? +please)?$")
timezone = re.compile(bot_prefix + "timezone([:,]? +please)?$")
# Tell The Rules
the_rules = re.compile(bot_prefix + "[Tt]he +[Rr]ules\s*$")
# The help
help = re.compile(bot_prefix + "[Hh](ELP|elp)")
# Remember feature
remember = re.compile(
    bot_prefix + "([Ww]hat +about +|([Cc]ould +you +)?([Pp]lease +)?remember +)(?P<note>.*)")
# Say something to someone
say = re.compile(bot_prefix + "([Pp]lease +)?[Ss]ay +(?P<msg>.*) +to +"
                              "(?P<nick>.+)$")
# GooeyJr loop
loop = re.compile("Adrij: Gooey Jr, at your service!")
loop_iterations_passed = 0
# Retrieve message
retrieve = re.compile(bot_prefix + "[Rr]etrieve +(message +)?(number +)?"
                                   "(?P<num>\d+)")
google = re.compile(bot_prefix + ".*(?P<msg>(([Hh][Oo][Ww] +[Tt][Oo])|[Ww]["
                                 "Hh][Aa][Tt](( +[Ii][Ss])|'[Ss])).*)")
issue = re.compile(".*#(?P<num>\d+)[\D$]")