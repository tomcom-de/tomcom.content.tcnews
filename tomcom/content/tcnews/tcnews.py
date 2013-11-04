# -*- coding: utf-8 -*-
#
#
# Copyright (c) 2010 by []
# Generator: ArchGenXML Version 2.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements,Interface
from tomcom.content.tcnews.config import *

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.base import registerATCT as registerType
from Products.ATContentTypes import ATCTMessageFactory as _
from DateTime import DateTime

from plone.app.blob.subtypes.file import ExtensionBlobField
from archetypes.schemaextender.field import ExtensionField
from plone.app.blob.field import BlobField

from archetypes.schemaextender.field import ExtensionField
from plone.app.blob.interfaces import IBlobImageField
from plone.app.blob.config import blobScalesAttr
from plone.app.blob.field import BlobField
from plone.app.blob.mixins import ImageFieldMixin
from Acquisition import aq_base
from Products.ATContentTypes.configuration import zconf

class TCExtensionImageBlobField(ExtensionField, BlobField, ImageFieldMixin):
    """ derivative of blobfield for extending schemas """
    implements(IBlobImageField)

    def set(self, instance, value, **kwargs):
        super(TCExtensionImageBlobField, self).set(instance, value, **kwargs)
        if hasattr(aq_base(instance), blobScalesAttr):
            delattr(aq_base(instance), blobScalesAttr)

##/code-section module-header

schema = Schema((

    TextField('text',
      required=False,
      searchable=True,
      primary=True,
      storage = AnnotationStorage(migrate=True),
      default_output_type = 'text/html',
      widget = RichWidget(
                description = '',
                label = _(u'Text', default=u'Text'),
                rows = 25,
                allow_file_upload = False,
        ),
    ),

    TCExtensionImageBlobField('image',
        sizes = None,
        storage = AnnotationStorage(migrate=True),
        original_size = None,
        default_content_type = 'image/png',
        allowable_content_types = ('image/gif', 'image/jpeg', 'image/png'),
        swallowResizeExceptions = zconf.swallowImageResizeExceptions.enable,
        pil_quality = zconf.pil_config.quality,
        pil_resize_algo = zconf.pil_config.resize_algo,
        widget = ImageWidget(
            label = _(u'label_preview_image', default=u'Preview image'),
            description=_(u''),
            show_content_type = False,
        ),
    ),

))

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TCNews_schema = ATFolder.schema.copy()+schema.copy()

##code-section after-schema #fill in your manual code here
TCNews_schema['creation_date'].widget.visible={'edit':'visible', 'view':'invisible'}
##/code-section after-schema

class ITCNews(Interface):
    """Marker interface for IDuweEvent
    """


class TCNews(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(ITCNews)

    meta_type = 'TCNews'
    _at_rename_after_creation = True

    schema = TCNews_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return ATFolder.__bobo_traverse__(self, REQUEST, name)

    security.declareProtected('View', 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)


registerType(TCNews, PROJECTNAME)

##code-section module-footer #fill in your manual code here
##/code-section module-footer