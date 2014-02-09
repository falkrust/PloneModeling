from five import grok

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable

from zope.lifecycleevent.interfaces import IObjectAddedEvent

import random
import string


from cs492.plonemodeling import MessageFactory as _

region_list = SimpleVocabulary(
    [SimpleTerm(value=u'us-east-1', title=_(u'us-east-1')),
     SimpleTerm(value=u'us-west-1', title=_(u'us-west-1')),
     SimpleTerm(value=u'us-west-2', title=_(u'us-west-2'))]
    )

instance_type_list = SimpleVocabulary([])



# Interface class; used to define content-type schema.

class IVirtualMachine(form.Schema, IImageScaleTraversable):
    """
    Specification of an EC2 instance
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/virtual_machine.xml to define the content type.

    #form.model("models/virtual_machine.xml")

    accessKey = schema.TextLine(
            title=_(u"AWS Access Key"),
    )

    secretKey = schema.TextLine(
            title=_(u"AWS Secret Key"),
    )

    region = schema.Choice(
            title=_(u"Region"),
            vocabulary=region_list,
            description = u"Perferably the list of available elements would be built dynamically ",
            required=False,
    )

    instance_type = schema.Choice(
            title=_(u"Instance Type"),
            vocabulary=instance_type_list,
            required=False,
            description = u"Perferably the list of available elements would be built dynamically ",
    )


    machineImage = schema.TextLine(
            title=_(u"Amazon Machine Image"),
    )

    monitorString = schema.TextLine(
            title=_(u"Monitor Identifier"),
            required=False
    )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class VirtualMachine(Container):
    grok.implements(IVirtualMachine)

    # Add your class methods and properties here
    def getTitle(self):
        return self.title


# View class
# The view will automatically use a similarly named template in
# virtual_machine_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IVirtualMachine)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here

@grok.subscribe(IVirtualMachine, IObjectAddedEvent)
def createVirtualMachine(virtual_machine, event):
    virtual_machine.monitorString = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(5))
