import frappe

from frappe import _
from toolz import first, compose, pluck, partial


def validate(doc, method):
    doc.disabled = doc.vc_deceased

    _validate_default_customer(doc)
    doc.customer = _get_default_customer(doc)


def _validate_default_customer(doc):
    validate_customer = compose(
        any,
        partial(map, lambda x: x.default)
    )(doc.vc_pet_relation)

    if not validate_customer:
        frappe.throw(_('Please set default customer under Pet Relation'))


def _get_default_customer(doc):
    return compose(
        first,
        partial(map, lambda x: x.customer),
        partial(filter, lambda x: x.default)
    )(doc.vc_pet_relation)
