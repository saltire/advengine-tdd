import json
import textwrap

from advengine.adventure import Adventure


if __name__ == '__main__':
    with open('./games/starflight.json', 'rb') as gfile:
        jstr = gfile.read()
        data = json.loads(jstr)
        adv = Adventure(data)

        messages = adv.start_game()

    while True:
        for message in messages:
            if message == 'PAUSE':
                input('Press any key...')
                print()
            else:
                for line in message.splitlines():
                    for wrapline in textwrap.wrap(line):
                        print(wrapline)
                print()

        messages = adv.do_command(input('> '))
