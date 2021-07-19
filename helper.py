from collections import namedtuple

def parse_string(content: str) -> dict:
    """Takes a string of search queries, parses them, and return a dict payload"""

    str_list = content.split()
    payload = dict()

    if str_list[0].lower() == "new":
        payload.update({"_sop": "10"})

    if str_list[0].lower() == "best":
        payload.update({"_sop": "12"})

    if str_list[0].lower() == "ending" or str_list[0].lower() == "end":
        payload.update({"_sop": "1"})

    if str_list[0].lower() == "low" or str_list[0].lower() == "lowest":
        payload.update({"_sop": "15"})

    if str_list[0].lower() == "high" or str_list[0].lower() == "highest":
        payload.update({"_sop": "16"})

    payload.update({"_nkw": " ".join(str_list[1:])})

    return payload


def parse_count(botmessage: str) -> namedtuple:
    """Reads the number at end of the message given and returns a namedtuple of the message and number"""

    count = 0
    complete_message = namedtuple("complete_message", ["message", "num"])

    message_contents = botmessage.split()

    try:
        count = int(message_contents[-1])
        botmessage = " ".join(message_contents[:-1])
        return complete_message(message=botmessage[6:], num=count)

    except ValueError:
        return complete_message(message=botmessage[6:], num=count)
