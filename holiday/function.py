"""
function module for invoking lambda function to populate holiday schedule for trash pickup.
"""


def lambda_handler(event, context):
    """
    lambda function for populating trash holiday schedule
    :param event: lambda event
    :param context: lambda context
    """
    print(event)
    print(context)
