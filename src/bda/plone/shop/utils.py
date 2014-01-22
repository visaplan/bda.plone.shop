from bda.plone.orders.interfaces import ISubShop
from bda.plone.shop.interfaces import IShopArticleSettings
from bda.plone.shop.interfaces import IShopCartSettings
from bda.plone.shop.interfaces import IShopSettings
from bda.plone.shop.interfaces import IShopShippingSettings
from bda.plone.shop.interfaces import IShopTaxSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import plone.api as ploneapi


def get_shop_settings():
    return getUtility(IRegistry).forInterface(IShopSettings)


def get_shop_tax_settings():
    return getUtility(IRegistry).forInterface(IShopTaxSettings)


def get_shop_article_settings():
    return getUtility(IRegistry).forInterface(IShopArticleSettings)


def get_shop_cart_settings():
    return getUtility(IRegistry).forInterface(IShopCartSettings)


def get_shop_shipping_settings():
    return getUtility(IRegistry).forInterface(IShopShippingSettings)


def get_all_shops():
    cat = ploneapi.portal.get_tool('portal_catalog')
    query = {}
    query['object_provides'] = ISubShop.__identifier__
    res = cat.searchResults(query)
    res = [it.getObject() for it in res]
    root = ploneapi.portal.get()
    if not ISubShop.providedBy(root):
        res.append(root)
    return res


def get_vendor_shops(vendor=None):
    if not vendor:
        vendor = ploneapi.user.get_current()
    all_shops = get_all_shops()
    try:
        vendor_shops = [
            shop for shop in all_shops
            if ploneapi.user.get_permissions(user=vendor, obj=shop).get(
                'bda.plone.shop: View vendor orders')
        ]
    except ploneapi.exc.UserNotFoundError:
        # might be Zope root user
        return []
    return vendor_shops
