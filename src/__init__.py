"""
This file registers the model with the Python SDK.
"""

from viam.services.generic import Generic
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .googleCalendar import googleCalendar

Registry.register_resource_creator(Generic.SUBTYPE, googleCalendar.MODEL, ResourceCreatorRegistration(googleCalendar.new, googleCalendar.validate))
