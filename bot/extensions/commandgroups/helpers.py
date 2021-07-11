def get_msgtype_from_message(message):
    """
    Helper to find out what kind of message has been reacted on

    :param message: Message that we need to look at
    :return Message type
    """
    return message.embeds[0].title


def get_reply_from_reaction(reaction, flow):
    """
    Helper to generate a reply given a reaction

    :param reaction: Reaction from user
    :param flow: Workflow definition
    :return: What we are going to reply
    """

    selection = convert_from_emoji(str(reaction))
    msgtype = get_msgtype_from_message(reaction.message)
    next_workflow_step = get_next_step(msgtype, flow)
    return generate_workflow_reply(next_workflow_step, selection)


def get_next_step(msgtype, flow):
    """
    Helper to get the next step in a workflow

    :param msgtype: Message type of the current step
    :param flow: Current workflow
    :return: Name of the next step
    """
    for idx, item in enumerate(flow):
        if item['step'] == msgtype:
            next_step = idx + 1
            if next_step < len(flow):
                return str(flow(next_step)['step'])
            else:
                raise ValueError('{} is the last step in the flow'.format(msgtype))


def generate_workflow_reply(workflow_step, choice, flow):
    """
    Helper to generate new reply at workflow step

    :param workflow_step: Current step in the workflow
    :param choice: Previous choice made
    :param flow: Workflow definition
    :return: Complete discord message
    """

    ### TODO